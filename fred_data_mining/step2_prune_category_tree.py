"""

    step2_prune_category_tree.py
    Mark Middendorf
    8/2/2023

    Intent: prune unwanted subtrees
    Output:
      - json of category_id and category_name of remaining tree
      - csv output to visualize final category subtree for use in the next step

    Subtrees to remove:
      - 3008 (U.S. Regional Data)
      - 32263 (International Data)
      - 33060 (Academic Data)

    Notes:
        Test that subtrees extracted are really subtrees of the tree

"""

import json
import pandas as pd
import sys
import time


# globals
SUBTREES_ROOTS = [3008, 32263, 33060]

# load data
INPUT0 = r'../json/fred_category_extract_2023_06_29.json'
INPUT1 = r'../json/fred_category_names_2023_07_10.json'

with open(INPUT0) as json_file:
    tree_dict = json.load(json_file)
with open(INPUT1) as json_file:
    names_dict = json.load(json_file)

category_name_df = pd.DataFrame.from_dict(names_dict)

# outfiles
OUTFILE0 = r'../csv/fred_category_tree_pruned_2023_07_21.csv'
OUTFILE1 = r'../json/fred_category_pruned_names_2023_07_21.json'


class Block(object):
    """class used solely as namespace for related functions"""
    @staticmethod
    def start(block_num: int, start_str: str) -> int:
        return sys.stdout.write('Start of Block {}: '.
                                format(block_num) + start_str)

    @staticmethod
    def end(block_num: int, end_str: str) -> int:
        return sys.stdout.write('End of Block {}: '.format(block_num) + end_str)


# UDFs
def subtree(parent, tree_list, edge_list, parent_list):
    """
    traverse a tree to collect subtree edges
    :param parent: root node of subtree
    :param tree_list: list of (parent, child) tuples
    :param edge_list: list to collect tuples
    :param parent_list: list to collect parents
    :return: col_list if a subtree exists
    """
    for tup in tree_list:
        if parent == tup[0]:
            edge_list.append(tup)
            parent_list.append(parent)
            subtree(tup[1], tree_list, edge_list, parent_list)


def main():

    start_time = time.time()
    sys.stdout.write('Program start ...\n')

    Block.start(1, 'convert tree_dict to list of tuples: (parent, child) ...\n')

    parent_child = list()
    for key, value in tree_dict.items():
        for v in value:
            parent_child.append((int(key), v))

    Block.end(1, 'json converted to dict ...\n')
    sys.stdout.write('End of Block 1: {} minutes (total elapsed time) ...\n\n'.
                     format(round((time.time() - start_time) / 60, 3)))

    Block.start(2, 'traverse tree and find subtrees ...\n')

    collect_subtrees = []
    collect_parents = []
    for s in SUBTREES_ROOTS:
        subtree(parent=s,
                tree_list=parent_child,
                edge_list=collect_subtrees,
                parent_list=collect_parents)

    Block.end(2, 'subtrees found ...\n')
    sys.stdout.write('End of Block 2: {} minutes (total elapsed time) ...\n\n'.
                     format(round((time.time() - start_time) / 60, 3)))

    Block.start(3, 'prune tree and generate gephi output ...\n')

    parent_child_pruned = tree_dict

    # convert keys from strings to ints; required for pop
    parent_child_pruned2 = {int(k): v for k, v in parent_child_pruned.items()}

    # remove dups in parents list
    collect_parents2 = list(set(collect_parents))

    for p in collect_parents2:
        parent_child_pruned2.pop(p)

    # generate list of tuples for gephi
    parent_child_updated = list()
    for key, value in parent_child_pruned2.items():
        for v in value:
            parent_child_updated.append((int(key), v))

    # json output for gephi viz
    df = pd.DataFrame(parent_child_updated, columns=['Source', 'Target'])
    df.to_csv(path_or_buf=OUTFILE0,
              sep=';',
              header=True,
              quoting=None,
              index=False)

    Block.end(3, 'tree pruned, gephi output generated ...\n')
    sys.stdout.write('End of Block 3: {} minutes (total elapsed time) ...\n\n'.
                     format(round((time.time() - start_time) / 60, 3)))

    Block.start(4, 'pruned tree category names ...\n')

    parent_child_updated_flat = [i for sub in parent_child_updated for i in sub]
    parent_child_updated_list = list(set(parent_child_updated_flat))

    pruned_category_df = pd.DataFrame(parent_child_updated_list, columns=['id'])
    final_df = pruned_category_df.merge(category_name_df, on=['id'])
    final_df.to_json(OUTFILE1, orient='records', indent=4)

    Block.end(4, 'pruned tree category names written to json ...\n')
    sys.stdout.write('End of Block 4: {} minutes (total elapsed time) ...\n\n'.
                     format(round((time.time() - start_time) / 60, 3)))

    sys.stdout.write('End of Program: {} minutes (total elapsed time)'.
                     format(round((time.time() - start_time) / 60, 3)))


if __name__ == '__main__':
    main()
