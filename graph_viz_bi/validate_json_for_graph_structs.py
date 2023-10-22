# graph_structs.py

"""
    Mark Middendorf
    9/29/2022
    Description: preliminary work to use various json file structures with
    networkx graphs and pydantic
    References:
        https://networkx.org/documentation/stable/index.html
        https://pydantic-docs.helpmanual.io/

"""

# import libraries
import json
from pydantic import BaseModel, ValidationError
from typing import Optional, Type


class NodeProfile(BaseModel):
    """Schema for nodes"""
    label: str
    index: int
    description: str
    sources: Optional[list]
    depends_on: Optional[list]


class FileContainer(BaseModel):
    """Container for nodes"""
    node_class: Type[NodeProfile]


def main():

    with open('./etl_process_1.json', 'r') as f:
        json_str = f.read()
        scope = json.loads(json_str)

    validation_error_count = 0
    for f in scope:
        for node in scope[f]:
            try:
                NodeProfile.model_validate(scope[f][node])
            except ValidationError as e:
                validation_error_count += 1
                print(f"Error found in file: {f}", e.json())

    print(f"Validation error count: {validation_error_count}")


if __name__ == '__main__':
    main()
