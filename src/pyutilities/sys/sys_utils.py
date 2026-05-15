# -*- coding: utf-8 -*-

"""
System Utilities module.

Created:  Dmitrii Gusev, 18.07.2025
Modified: Dmitrii Gusev, 15.05.2026
"""

import logging
import os

from pyutilities.defaults import MSG_MODULE_ISNT_RUNNABLE
from pyutilities.utils.string_utils import is_empty, str_2_bool, str_2_float, str_2_int

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def get_str_from_env(key: str, default: str = "") -> str:
    """TBD"""

    return default if is_empty(key) else (os.environ.get(key) or default)


def get_int_from_env(key: str, default: int = 0) -> int:
    """TBD"""

    if not key or not key.strip():
        return default

    env_value = os.environ.get(key)
    return str_2_int(env_value) if env_value else default


def get_float_from_env(key: str, default: float = 0.0) -> float:
    """TBD"""

    if not key or not key.strip():
        return default

    env_value = os.environ.get(key)
    return str_2_float(env_value) if env_value else default


def get_bool_from_env(key: str, default: bool = False) -> bool:
    """TBD"""

    if not key or not key.strip():
        return default

    env_value = os.environ.get(key)
    return str_2_bool(env_value) if env_value else default


# # show all env variables sorted by name:
# # print('\n'.join(f'{k}={v}' for k, v in sorted(os.environ.items())))


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
