import hou
from ..parameters import add_parameter


def create_tree(
        items: list[str],
        network: hou.NetworkItem | str = '/stage',
        start: hou.NetworkItem | str | None = None) -> list[hou.NetworkItem]:
    """
    Create tree network setup

    Keyword arguments:
        items -- list of nodes or dot. Example:
            [{'type': 'dot',
              'name': 'dotidentifier'  # Optional
             },
             {'type': 'node_type',
              'name': 'name',
              'input_index': 0,  # Optional
              'parms': {'parm': 'value'}  # Optional
              'add_parms': [  # Optional
                  {'name': 'value',
                   'label': 'name',
                   'subtype': 'name',
                   'value': 'value'}]
             }]
        network -- network where to create the tree
        start -- network item where to start from
    """
    if isinstance(network, str):
        network = hou.node(network)
    previous_item = None
    if start is not None:
        if isinstance(start, str):
            previous_item = network.node(start)
        else:
            previous_item = start
    network_items = []
    for data in items:
        is_dot = data['type'] == 'dot'
        # Item creation
        if is_dot:
            item = network.createNetworkDot()
            if dot_name := data.get('name'):
                item.setName(dot_name)
        else:
            item = network.createNode(
                node_type_name=data['type'], node_name=data['name'])
            # Set parms
            if parms := data.get('parms'):
                for parm, value in parms.items():
                    item.parm(parm).set(value)
            if add_parms := data.get('add_parms'):
                for new_parm in add_parms:
                    parm_item = add_parameter(
                        node=item,
                        name=new_parm['name'],
                        label=new_parm['label'],
                        subtype=new_parm['subtype'])
                    parm_item.set(new_parm['value'])
        network_items.append(item)
        if previous_item is not None:
            # Item position
            x, y = previous_item.position()
            # Item connection
            if is_dot:
                x += 0.5  # Offset dot alignement
                item.setInput(previous_item)
            else:
                if isinstance(previous_item, hou.OpNetworkDot):
                    x -= 0.5  # Offset dot alignement
                if index := data.get('input_index'):
                    item.setInput(index, previous_item)
                else:
                    item.setFirstInput(previous_item)
            item.setPosition((x, y - 1))
        previous_item = item
    return network_items
