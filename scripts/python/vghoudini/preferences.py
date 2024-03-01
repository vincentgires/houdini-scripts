import hou


def preference(
        name: str,
        value: bool | int | float | str | None = None,
        remove: bool = False,
        expect_boolean: bool = False) -> bool | None:
    """Get or set preference state

    Keyword Arguments:
        name -- preference name
        value -- value to set (default None)
        remove -- remove preference from houdini.prefs (default False)
        expect_boolean -- return False|True instead of 0|1
    """
    hou.refreshPreferences()
    if remove:
        hou.removePreference(name)
    if value is None:
        if name in hou.getPreferenceNames():
            value_ = hou.getPreference(name)
            if value_.isdecimal():
                value_int = int(value_)
                if expect_boolean:
                    if any(x == value_int for x in (0, 1)):
                        return bool(value_)
                return value_int
            elif value_.replace('.', '').isdecimal():
                return float(value_)
            return value_
        return
    if isinstance(value, (int, bool)):
        value_ = str(int(value))
    elif isinstance(value, float):
        value_ = str(float(value))
    value_ = str(value)
    if name not in hou.getPreferenceNames():
        hou.addPreference(name, value_)
    else:
        hou.setPreference(name, value_)
