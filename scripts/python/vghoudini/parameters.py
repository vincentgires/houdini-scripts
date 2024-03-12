import hou

parm_constructors = {
    'float': hou.FloatParmTemplate,
    'int': hou.IntParmTemplate,
    'label': hou.LabelParmTemplate,
    'string': hou.StringParmTemplate,
    'toggle': hou.ToggleParmTemplate}


def add_parameter(
        node: hou.Node,
        name: str,
        label: str,
        subtype: str,
        **kwargs) -> hou.Parm:
    if subtype == 'string' and 'num_components' not in kwargs:
        kwargs['num_components'] = 1
    group = node.parmTemplateGroup()
    parm = parm_constructors[subtype](name, label, **kwargs)
    group.append(parm)
    node.setParmTemplateGroup(group)
    return node.parm(name)
