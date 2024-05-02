import hou
import loputils
from ..parameters import add_parameter


def create_tree(
        items: list[str],
        network: hou.NetworkItem | str = '/stage',
        start_item: hou.NetworkItem | str | None = None,
        start_position: tuple[int, int] | None = None
        ) -> list[hou.NetworkItem]:
    """
    Create tree network setup

    Keyword arguments:
        items -- list of nodes or dot. Example:
            [{'type': 'dot',
              'name': 'dotidentifier'  # Optional
             },
             {'type': 'node_type',
              'name': 'name',  # Optional
              'bypass: False,  # Optional
              'input_index': 0,  # Optional
              'parms': {'parm': 'value'}  # Optional
              'add_parms': [  # Optional
                  {'name': 'value',
                   'label': 'name',
                   'subtype': 'name',
                   'value': 'value'}],
              'set_all_controls': 'value',  # Optional
             }]
        network -- network where to create the tree
        start_item -- network item where to start from
        start_position -- x, y position to start from
    """
    def set_positon(item, position):
        x, y = position
        if isinstance(item, hou.OpNetworkDot):  # Offset dot alignement
            x += 0.5
        item.setPosition((x, y - 1))

    if isinstance(network, str):
        network = hou.node(network)
    previous_item = None
    if start_item is not None:
        if isinstance(start_item, str):
            previous_item = network.node(start_item)
        else:
            previous_item = start_item
    network_items = []
    for item_index, data in enumerate(items):
        is_dot = data['type'] == 'dot'
        # Item creation
        if is_dot:
            item = network.createNetworkDot()
            if dot_name := data.get('name'):
                item.setName(dot_name)
        else:
            item = network.createNode(
                node_type_name=data['type'], node_name=data.get('name'))
            # Set bypass
            if bypass := data.get('bypass'):
                item.bypass(bypass)
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
            if set_all_controls := data.get('set_all_controls'):
                loputils.setAllControlParameters(item, set_all_controls)
        network_items.append(item)
        set_pos = None  # Item position
        if previous_item is not None:
            x, y = previous_item.position()
            # Item connection
            if is_dot:
                item.setInput(previous_item)
            else:
                if isinstance(previous_item, hou.OpNetworkDot):
                    x -= 0.5  # Compensate dot offset alignement
                if index := data.get('input_index'):
                    item.setInput(index, previous_item)
                else:
                    item.setFirstInput(previous_item)
            set_pos = (x, y)
        if start_position is not None and item_index == 0:  # Match first item
            set_pos = start_position
        if set_pos is not None:
            set_positon(item, set_pos)
        previous_item = item
    return network_items
