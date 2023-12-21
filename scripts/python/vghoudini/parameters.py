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
        **kwargs) -> hou.ParmTemplate:
    group = node.parmTemplateGroup()
    parm = parm_constructors[subtype](name, label, **kwargs)
    group.append(parm)
    node.setParmTemplateGroup(group)
