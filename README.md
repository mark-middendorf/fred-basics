# fred-basics
Review of FRED (Federal Reserve Economic Data) API

```mermaid
graph LR
    fred.py --> extract_category_tree.py 

```

**fred.py**
+ contains FredAPI class with multiple methods to query the
FRED API

**extract_category_tree.py**
+ select a root node (for the overall tree this node is 0); other
roots could be selected to extract a subtree
+ returns a dict where the key is a parent node and the value
is a list of children nodes
+ there are ~5k categories and a limit to request that can be made
per second - traversal algorithm includes a call to time.sleep to slow
down requests (i.e., this takes time to run for the entire tree)
+ see ./json/fred_category_extract_test_2023_08_02.json for subtree
+ see ./json/frec_category_extract_2023_08_02.json for full tree