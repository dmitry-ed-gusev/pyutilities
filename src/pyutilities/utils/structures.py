# -*- coding: utf-8 -*-

"""
Structures module.

Created:  Dmitrii Gusev, 21.05.2026
Modified: Dmitrii Gusev, 21.05.2026
"""

from typing import Any


def defaultdict_factory(key) -> Any:
    """Return different default types for the defaultdict based on the key prefix.
    Usage example:
            dynamic_dict = defaultdict(lambda: None)
            dynamic_dict.defaultdict_factory = defaultdict_factory
    """

    if key.startswith('count_'):  # int type
        return 0
    elif key.startswith('str_'):  # string type
        return ''
    elif key.startswith('items_'):  # list type
        return []
    elif key.startswith('set_'):  # set type
        return set()
    elif key.startswith('dict_'):  # dictionary type
        return {}
    else:  # unknown type
        return None  # fallback for unknown keys
