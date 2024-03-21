import hou
from typing import Union

CategoryName = Union[str, hou.NodeTypeCategory]


def get_categories(*categories: CategoryName) -> list[hou.NodeTypeCategory]:
    if not categories:
        result = set(hou.nodeTypeCategories().values())
    else:
        result = set()
        for category in categories:
            if isinstance(category, str):
                if item := hou.nodeTypeCategories().get(category):
                    result.add(item)
            else:
                result.add(category)
    return list(result)


def get_nodes_from_type(
        types: str | list[str],
        categories: tuple[CategoryName] | str = (),
        all_versions=True) -> list[hou.Node]:
    nodes = []
    if isinstance(categories, str):
        categories = [categories]
    for category in get_categories(*categories):
        if isinstance(types, str):
            types = [types]
        for type_name in types:
            if not all_versions:
                node_type = category.nodeType(type_name)
                if node_type is None:
                    continue
                nodes.extend(list(node_type.instances()))
            else:
                for type_name_, node_type in category.nodeTypes().items():
                    raw_type_name = hou.hda.componentsFromFullNodeTypeName(
                        type_name_)[2]
                    if type_name == raw_type_name:
                        nodes.extend(list(node_type.instances()))
    return nodes
