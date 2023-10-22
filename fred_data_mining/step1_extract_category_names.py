from fred_data_mining import fred as f
import json
import pandas as pd
import time

# file names
INPUT0 = r'./json/api_keys/mcm_api_keys.json'
INPUT1 = r'./json/fred_category_extract_2023_08_02.json'
OUTPUT0 = r'./json/fred_category_names_2023_08_02.json'
OUTPUT1 = r'./csv/fred_cat_nodes.csv'

# load api_key
p = open(INPUT0)
api_key = json.load(p)


def main():

    # load category data from step0_extract_category_tree.py
    with open(INPUT1) as json_file:
        cat_dict = json.load(json_file)

    # process data
    categories = []
    for key, value in cat_dict.items():
        categories.append(value)

    # flatten lists
    categories_flat = [item for sublist in categories for item in sublist]
    cat_final = list(set(categories_flat))

    # use category ID to get category name
    api = f.FredAPI(api_key=str(api_key['fred']))
    cat_meta_df = pd.DataFrame(columns=['id', 'name', 'parent_id'])

    for c in cat_final:
        cat_loop_str = api.category_api_str(category_id=c)
        loop_content = api.api_request(cat_loop_str)

        try:
            method_df1 = pd.DataFrame.from_dict(loop_content)
            method_df2 = pd.json_normalize(method_df1['categories'])
            cat_meta_df = pd.concat([cat_meta_df, method_df2])
        except KeyError:
            pass

        time.sleep(0.2)  # 429 error possible

    # process category metadata; write to JSON and CSV
    cat_meta_df.drop_duplicates(subset=['id'],
                                keep='first',
                                inplace=True)
    cat_meta_df2 = cat_meta_df[['id', 'name', 'parent_id']].copy()
    cat_meta_df2.to_json(OUTPUT0, orient='records', indent=4)

    gephi_cols = {
        'id': 'Id',
        'name': 'Label'
    }
    csv_df = cat_meta_df[['id', 'name']].copy()
    csv_df.rename(columns=gephi_cols, inplace=True)
    csv_df.to_csv(path_or_buf=OUTPUT1,
                  sep=';',
                  header=True,
                  quoting=None,
                  index=False)


if __name__ == '__main__':
    main()
