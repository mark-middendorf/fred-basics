from fred_data_mining import fred as f
import json
import pandas as pd
import time


# file names
INPUT = r'./json/api_keys.json'
OUTPUT = r'./json/fred_category_extract_test_2023_08_02.json'
ROOT_NODE = 33839

# load api_key
p = open(INPUT)
api_key = json.load(p)


# UDFs
def proc_cat_child_payload(json_payload) -> list:
    """
    returns a list of child nodes for a given parent
    :param json_payload: FRED API payload
    :return: list of child IDs
    """
    method_df1 = pd.DataFrame.from_dict(json_payload)
    method_df2 = pd.json_normalize(method_df1['categories'])

    try:
        method_ids = method_df2['id'].to_list()
    except KeyError:
        method_ids = []

    return method_ids


def tree(api, parent: int, output_dict: dict):
    request_str = api.category_children_api_str(category_id=parent)
    request_content = api.api_request(request_str)
    request_list = proc_cat_child_payload(request_content)

    # review branch
    if len(request_list) > 0:
        print(f"{parent} :: {request_list}")
        output_dict[parent] = request_list

    for i in request_list:
        if len(request_list) == 0:
            pass  # leaf node found

        time.sleep(1)  # sleep to avoid 429 response
        tree(api, parent=i, output_dict=output_dict)


def main():
    """
    traverse the FRED category tree to extract parent/child nodes and
    edges

    :return:
    """

    api = f.FredAPI(api_key=str(api_key['fred']))

    cat_dict = {}
    tree(api=api, parent=ROOT_NODE, output_dict=cat_dict)

    # dict to json output
    out_file = open(OUTPUT, 'w')
    json.dump(cat_dict, out_file, indent=6)
    out_file.close()


if __name__ == '__main__':
    main()
