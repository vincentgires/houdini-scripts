import json
from typing import Optional, Union, List
import hou


def get_config(name: str) -> dict:
    config = hou.contextOptionConfig(name)
    if not config:
        # HACK: context options panel has to be opened a first time to get
        # default context config. If not available, here is a default config.
        _default_config = (
            '{"label": "", "type": "text", "order": 1, "comment": "", '
            '"menu_items": [], "autovalues": false, "menu_source": "", '
            '"minimum": 0.0, "maximum": 10.0, "min_locked": false, '
            '"max_locked": false}')
        config = _default_config
    return json.loads(config)


def set_config(
        name: str,
        label: Optional[str] = None,
        type_: Optional[str] = None,
        tooltip: Optional[str] = None,
        items: Optional[List] = None,  # Optional[list[list[str, str]]]
        autovalues: Optional[bool] = None,
        minimum: Optional[int] = None,
        maximum: Optional[int] = None,
        min_locked: Optional[bool] = None,
        max_locked: Optional[bool] = None,
        order: Optional[int] = None) -> None:
    config = get_config(name)
    if config is None:
        return
    if label is not None:
        config['label'] = label
    if type_ is not None:
        config['type'] = type_
    if tooltip is not None:
        config['comment'] = tooltip
    if autovalues is not None:
        config['autovalues'] = autovalues
    if minimum is not None:
        config['minimum'] = minimum
    if maximum is not None:
        config['maximum'] = maximum
    if min_locked is not None:
        config['min_locked'] = min_locked
    if max_locked is not None:
        config['max_locked'] = max_locked
    if order is not None:
        config['order'] = order
    if items is not None:
        config['menu_items'] = items
    hou.setContextOptionConfig(name, json.dumps(config))


def add_item_menu(
        name: str,
        item: List[str],  # list[str, str]
        sort: bool = True) -> None:
    config = get_config(name)
    if config is None:
        return
    items = config['menu_items']
    if item in items:
        return
    items.append(item)
    if sort:
        items = sorted(items, key=lambda x: (x[0], x[1]))
    set_config(name, items=items)


def set_option(
        name: str,
        value: Optional[Union[str, int, float]] = None,
        **config) -> None:
    hou.setContextOption(name, '')
    set_config(name, **config)
    if value is not None:
        hou.setContextOption(name, value)


def remove_option(name: str) -> None:
    hou.setContextOption(name, None)


if __name__ == 'hou.session':
    set_option(
        'test',
        value='b',
        label='Test',
        type_='string_menu',
        items=[['A', 'a'], ['B', 'b'], ['C', 'c']])
