import hou
from typing import Optional, Union, List

CategoryName = Union[str, hou.NodeTypeCategory]


def get_categories(
        name: Optional[CategoryName] = None) -> List[hou.NodeTypeCategory]:
    if name is None:
        categories = hou.nodeTypeCategories().values()
    else:
        if isinstance(name, str):
            categories = [hou.nodeTypeCategories()[name]]
        else:
            categories = [name]
    return categories


def get_nodes_from_type(
        type_name: str,
        category_name: Optional[CategoryName] = None) -> List[hou.Node]:
    nodes = []
    for category in get_categories(category_name):
        node_type = category.nodeType(type_name)
        if node_type is None:
            continue
        nodes.extend(list(node_type.instances()))
    return nodes
