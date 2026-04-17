# -*- coding: utf-8 -*-

# This code should be put in <your_package_name>/__init__.py or <your_package_name>/_version.py
# The library version now is programmatically accessible (from code).

import importlib.metadata

try:
    __version__ = importlib.metadata.version("pyutilities")
except importlib.metadata.PackageNotFoundError:
    # Handle the case where the package is not installed (e.g., during development)
    __version__ = "0.0.0+unknown"
