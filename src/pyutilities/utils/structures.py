# -*- coding: utf-8 -*-

"""
Structures module.

Created:  Dmitrii Gusev, 21.05.2026
Modified: Dmitrii Gusev, 24.05.2026
"""

from collections import defaultdict

from pyutilities.utils.string_utils import is_empty


def _defaultdict_factory(key: str):
    """Return different default types for the defaultdict based on the key prefix.
    This function is used a s a default factory for the class KeyAwareDefaultDict - see below.
    """

    if isinstance(key, str) and not is_empty(key):

        if key.startswith("count_"):  # int type
            return 0

        if key.startswith("str_"):  # string type
            return ""

        if key.startswith("items_"):  # list type
            return []

        if key.startswith("set_"):  # set type
            return set()

        if key.startswith("dict_"):  # dictionary type
            return {}

    # unknown type - fallback for unknown keys
    return None


class KeyAwareDefaultDict(defaultdict):  # type: ignore[type-arg]
    """Extension of the default dictionary in python - 'key aware default dictionary', implementing
    different types of the dictionary values, depending on the dictionary keys prefixes.
    Prefixes are:
        - count_* - int type
        - str_*   - str type
        - items_* - list type
        - set_*   - set type
        - dict_*  - dict type
    Usage example:
        dynamic_dict = KeyAwareDefaultDict()  # option I - default factory (see above)
        dynamic_dict = KeyAwareDefaultDict(default_factory)  # option II - use your custom factory function
    """

    def __init__(self, default_factory=_defaultdict_factory):
        super().__init__(default_factory)

    def __missing__(self, key):
        # call the factory with a key and save the result
        result = self.default_factory(key)  # type: ignore[call-arg, misc]
        self[key] = result
        return result
