# -*- coding: utf-8 -*-

"""
System Utilities module.

Created:  Dmitrii Gusev, 18.07.2025
Modified: Dmitrii Gusev, 21.07.2025
"""

import logging
import os

from pyutilities.utils.string_utils import str_2_bool, str_2_float, str_2_int

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def get_str_from_env(key: str, default: str = "") -> str:

    if not key or not key.strip():
        return default

    return os.environ.get(key) or default


def get_int_from_env(key: str, default: int = 0) -> int:

    if not key or not key.strip():
        return default

    env_value = os.environ.get(key)
    return str_2_int(env_value) if env_value else default


def get_float_from_env(key: str, default: float = 0.0) -> float:

    if not key or not key.strip():
        return default

    env_value = os.environ.get(key)
    return str_2_float(env_value) if env_value else default


def get_bool_from_env(key: str, default: bool = False) -> bool:

    if not key or not key.strip():
        return default

    env_value = os.environ.get(key)
    return str_2_bool(env_value) if env_value else default
