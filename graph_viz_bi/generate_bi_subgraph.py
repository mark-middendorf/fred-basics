# audit_graph_step_1_1.py

"""
    Mark Middendorf
    9/21/2022
    Description: preliminary work to integrate json and networkx graphs

"""

# import libraries
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import graph_structs as gs

plt.rcParams['figure.figsize'] = [15, 12]

# graph layouts: spring_layout, circular_layout, shell_layout,
# random_layout, spectral_layout, kamada_kawai_layout, spiral_layout
# seed used with random_layout and spring_layout
GRAPH = '0060_print_share_usage_unfiltered_agg_pass2_v2'
VERSION = 1
graph_params = {
    '0060_print_share_usage_unfiltered_agg_pass2_v2': {
        'sql_ext': False,
        'graph_type': 'shell_layout',
        'graph_iterations': 10,
        'graph_seed': 20022,
        'horizontalalignment': 'center',
        'verticalalignment': 'bottom',
        'cut': 1.4
    },
}


def main():

    # params
    json_file = r'./etl_process_1.json'

    if graph_params[GRAPH]['sql_ext']:
        graph_file = f"{GRAPH}.sql"
    else:
        graph_file = f"{GRAPH}"

    outfile = f"./png/graph_{GRAPH}_v{VERSION}"  # no extension

    graph_type = graph_params[GRAPH]['graph_type']
    graph_iterations = graph_params[GRAPH]['graph_iterations']
    graph_seed = graph_params[GRAPH]['graph_seed']
    horizonal_alignment = graph_params[GRAPH]['horizontalalignment']
    vertical_alignment = graph_params[GRAPH]['verticalalignment']
    cut = graph_params[GRAPH]['cut']

    ####################################
    # process json scope
    ####################################
    graph_class = gs.GraphScopeStruct(json_file, graph_file)
    graph_df = graph_class.depend_df()
    nodes_df = graph_class.nodes_idx_df(edge_df=graph_df, depcol='dependency')
    #print(nodes_df)

    ####################################
    # prep for graph
    ####################################
    # graph labels
    graph_labels = nodes_df['node'].to_dict()
    #print(graph_labels)

    # graph edges
    edges_df1 = pd.merge(graph_df, nodes_df, how='left', left_on='model',
                         right_on='node')
    edges_df1 = edges_df1[['model', 'idx', 'dependency']]
    edges_df1.columns = ['start_model', 'start_node', 'stop_model']

    edges_df2 = pd.merge(edges_df1, nodes_df, how='left', left_on='stop_model',
                         right_on='node')
    edges_df2 = edges_df2[['start_model', 'start_node', 'stop_model', 'idx']]
    edges_df2.columns = ['start_model', 'start_node', 'stop_model', 'stop_node']
    # print(edges_df2)

    # graph data structures
    node_list = nodes_df.idx.tolist()
    edges_list = list(zip(edges_df2.start_node, edges_df2.stop_node))
    edges_list = list(set(edges_list))
    #print(node_list)

    ####################################
    # networkx
    ####################################
    # setup and draw graph
    G = nx.DiGraph()
    G.add_nodes_from(node_list)
    G.add_edges_from(edges_list)
    G_rev = nx.DiGraph.reverse(G)

    if graph_type == 'spring_layout':
        pos = nx.spring_layout(G_rev, iterations=graph_iterations,
                               seed=graph_seed)
    elif graph_type == 'circular_layout':
        pos = nx.circular_layout(G_rev)
    elif graph_type == 'shell_layout':
        pos = nx.shell_layout(G_rev)
    elif graph_type == 'random_layout':
        pos = nx.random_layout(G_rev, seed=graph_seed)
    elif graph_type == 'spectral_layout':
        pos = nx.spectral_layout(G_rev)
    elif graph_type == 'kamada_kawai_layout':
        pos = nx.kamada_kawai_layout(G_rev, scale=1)
    elif graph_type == 'spiral_layout':
        pos = nx.spiral_layout(G_rev)

    # adjust the plot limits
    # cut = 1.2 :: added to params dict
    xmin = cut * min(xx for xx, yy in pos.values())
    ymin = cut * min(yy for xx, yy in pos.values())
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)

    cte_node_list = nodes_df[nodes_df.type == 'cte'][
        'idx'].drop_duplicates().to_list()
    src_node_list = nodes_df[nodes_df.type == 'src'][
        'idx'].drop_duplicates().to_list()

    nx.draw(G_rev, pos=pos, node_size=450, with_labels=False, arrowsize=14,
            nodelist=cte_node_list, node_color="tab:red", edge_color="gray",
            width=0.5)
    nx.draw(G_rev, pos=pos, node_size=450, with_labels=False, arrowsize=14,
            nodelist=src_node_list, node_color="tab:blue", edge_color="gray",
            width=0.5)
    nx.draw_networkx_labels(G_rev, pos, graph_labels,
                            horizontalalignment=horizonal_alignment,
                            verticalalignment=vertical_alignment,
                            font_color='k')

    # add descriptive data to graph as text
    order = f"Graph order (nodes): {G.order()}"
    size = f"Graph size (edges): {G.size()}"
    plt.text(xmin + 0.01, ymax - 0.05, graph_file, fontsize=12)
    plt.text(xmin + 0.01, ymax - 0.12, order, fontsize=12)
    plt.text(xmin + 0.01, ymax - 0.19, size, fontsize=12)

    plt.savefig(outfile, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    main()