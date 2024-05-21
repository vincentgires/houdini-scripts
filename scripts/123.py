import hou
from vghoudini.networks import node_creation_callbacks
from vghoudini.networks import on_child_created as on_network_child_created
from vghoudini.networks import on_child_deleted as on_network_child_deleted

for network_name in node_creation_callbacks:
    network = hou.node(network_name)
    network.addEventCallback(
        (hou.nodeEventType.ChildCreated,), on_network_child_created)
    network.addEventCallback(
        (hou.nodeEventType.ChildDeleted,), on_network_child_deleted)
