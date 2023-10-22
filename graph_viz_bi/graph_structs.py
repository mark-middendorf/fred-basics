# graph_structs.py

"""
    Mark Middendorf
    9/22/2022
    Description: preliminary work to use various json file structures with
    networkx graphs
    Reference: https://networkx.org/documentation/stable/index.html

"""

# import libraries
import json
import pandas as pd


class GraphScopeStruct:

    def __init__(self, scope: json, file: str):

        with open(scope, 'r') as f:
            json_str = f.read()
            self.scope = json.loads(json_str)

        self.file = file

    def extract_depends_on(self) -> dict:
        """Iterate through manifest models to find depends_on key & value(s)
        :return: dictionary (node: list of dependencies)
        """

        node_dict = {}  # initialize a dictionary

        for node in self.scope[self.file]:

            try:
                source_list = \
                    self.scope[self.file][node]['depends_on']
                node_dict[node] = source_list

            except KeyError:
                pass

        return node_dict

    def extract_sources(self) -> dict:
        """Iterate through manifest models to find sources key & value(s)
        :return: dictionary (node: list of sources)
        """

        node_dict = {}  # initialize a dictionary

        for node in self.scope[self.file]:

            try:
                source_list = \
                    self.scope[self.file][node]['sources']
                node_dict[node] = source_list

            except KeyError:
                pass

        return node_dict

    def transform_dicts(self) -> list:
        """Transform sources and dependencies to a list of tuples (model,
        dependency)
        :return: list of tuples
        """
        source_dict = self.extract_sources()
        depend_dict = self.extract_depends_on()
        tuple_list = []

        for node in source_dict:
            for element in source_dict[node]:
                tuple_list.append((node, element))

        for node in depend_dict:
            for element in depend_dict[node]:
                tuple_list.append((node, element))

        tuple_list.sort(key=lambda tup: tup[0])

        return tuple_list

    def depend_df(self) -> pd.DataFrame:
        """Converts Python list of tuples to a Pandas DF
        :return: dataframe
        """
        tuple_list = self.transform_dicts()
        df = pd.DataFrame(tuple_list, columns=['model', 'dependency'])

        return df

    def nodes_idx_df(self, edge_df: pd.DataFrame, depcol: str) -> \
            pd.DataFrame:
        """ converts output from depend_df() to a node dataframe (node, idx)
        :param edge_df: return_graph() list-of-lists to pandas dataframe
        :param depcol: name of dependency column
        :return:
        """

        index_list = []
        node_list = []

        for node in self.scope[self.file]:

            try:
                index_list.append((node,
                                   self.scope[self.file][node]['index'],
                                   'cte',
                                   str(f"{self.scope[self.file][node]['label']}")))
                node_list.append(node)

            except KeyError:
                pass

        # process dependency column
        edge_list1 = edge_df[depcol].tolist()
        edge_list2 = list(dict.fromkeys(edge_list1))

        # grab nodes w/o an index
        s = set(node_list)
        edge_list3 = [x for x in edge_list2 if x not in s]
        edge_list3.sort()

        start_idx = len(node_list)

        for i in range(len(edge_list3)):
            index_list.append((edge_list3[i], start_idx + i, 'src',
                               f"rs_{i}"))

        df = pd.DataFrame(index_list, columns=['node', 'idx', 'type', 'label'])

        return df
