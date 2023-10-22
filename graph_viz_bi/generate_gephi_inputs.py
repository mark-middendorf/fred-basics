from itertools import cycle
import re
import pandas as pd
import graph_structs as gs


def main():

    # params
    json_file = r'./etl_process_1.json'
    subgraphs = ['0060_print_share_usage_unfiltered_agg_pass2_v2',
                 '0070_print_share_usage_agg', 'sira_extract_sql']

    # PROCESS USING EXISTING LIBRARY
    global_nodes_df = pd.DataFrame()
    global_edges_df = pd.DataFrame()

    for s in subgraphs:
        graph_class = gs.GraphScopeStruct(json_file, s)
        graph_df = graph_class.depend_df()
        nodes_df = graph_class.nodes_idx_df(edge_df=graph_df,
                                            depcol='dependency')

        # add additional edge to graph_df
        prep = list(set(graph_df['model']))
        r = re.compile("^.*main_select")
        prep2 = list(filter(r.match, prep))
        main_select_node = prep2[0]

        add_edge = pd.DataFrame.from_dict(
            {'row1': [s, main_select_node]},
            orient='index',
            columns=['model', 'dependency'])
        add_edge.reset_index(drop=True, inplace=True)
        graph_df = pd.concat([graph_df, add_edge])
        graph_df.reset_index(drop=True, inplace=True)
        global_edges_df = pd.concat([global_edges_df, graph_df])

        # add additional node to nodes_df
        add_node = pd.DataFrame.from_dict(
            {'row1': [s, 999, 'src', 'dbt_0']},
            orient='index',
            columns=['node', 'idx', 'type', 'label']
        )
        add_node.reset_index(drop=True, inplace=True)
        nodes_df = pd.concat([nodes_df, add_node])
        nodes_df.reset_index(drop=True, inplace=True)
        nodes_df2 = nodes_df[['node', 'type']]
        global_nodes_df = pd.concat([global_nodes_df, nodes_df2])

    # PREP FOR GEPHI - nodes
    global_nodes_df.reset_index(drop=True, inplace=True)
    global_nodes_df2 = global_nodes_df.drop_duplicates(subset=['node', 'type'])
    global_nodes_df2.reset_index(drop=True, inplace=True)

    global_nodes_df3 = global_nodes_df2.copy()
    global_nodes_df3['id'] = global_nodes_df3.index
    global_nodes_df4 = global_nodes_df3.copy()

    def attribute(global_nodes_df4):
        if global_nodes_df4['node'] in subgraphs:
            return 'ddl_or_extract'
        elif global_nodes_df4['type'] == 'src':
            return 'database'
        elif global_nodes_df4['type'] == 'cte':
            return 'logic'
        elif global_nodes_df4['type'] == 'dbt':
            return 'dbt_file'

    global_nodes_df4['attribute'] = global_nodes_df4.apply(attribute, axis=1)
    global_nodes_df5 = global_nodes_df4[['id', 'node', 'attribute']].copy()
    node_cols = {'id': 'Id', 'node': 'Label', 'attribute': 'Attribute'}
    global_nodes_df5.rename(columns=node_cols, inplace=True)
    # print(global_nodes_df5)

    # PREP FOR GEPHI - edges
    global_edges_df.reset_index(drop=True, inplace=True)

    global_edges_df2 = global_edges_df.merge(global_nodes_df4[['node', 'id']],
                                             left_on='model',
                                             right_on='node')
    global_edges_df3 = global_edges_df2.merge(global_nodes_df4[['node', 'id']],
                                              left_on='dependency',
                                              right_on='node')
    global_edges_df4 = global_edges_df3[['id_y', 'id_x']].copy()
    graph_cols = {'id_y': 'Source', 'id_x': 'Target'}
    global_edges_df4.rename(columns=graph_cols, inplace=True)
    # print(global_edges_df4)

    # OUTPUT
    global_nodes_df5.to_csv(path_or_buf=r'./csv/etl_process_nodes.csv',
                            sep=';',
                            header=True,
                            quoting=None,
                            index=False)
    global_edges_df4.to_csv(path_or_buf=r'./csv/etl_process_edges.csv',
                            sep=';',
                            header=True,
                            quoting=None,
                            index=False)


if __name__ == '__main__':
    main()
