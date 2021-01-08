#!/bin/bash
#
# =======================================================================================
#
#   Create distribution for [pyutilities] library.
#   See more info here: https://packaging.python.org/tutorials/packaging-projects/#
#
#   Created:  Gusev Dmitrii, 25.09.2018
#   Modified: Dmitrii Gusev, 19.05.2019
#
# =======================================================================================

# execute unit tests with coverage
./test_with_coverage.sh

# setup proxy for twine (comment/uncomment - if necessary)
export ALL_PROXY=webproxy.merck.com:8080

# clean previous version(s) distributions
rm -rf dist
rm -rf build
rm -rf pyutilities.egg-info

# upgrade versions of setuptools/wheel/twine
pip install --user --upgrade setuptools wheel twine $1 $2

# create distribution for library in /dist catalog
python setup.py sdist bdist_wheel

# upload new library to Test PyPi (TEST)
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# upload new library dist to real PyPi (PROD)
twine upload -u vinnypuhh dist/*

# upgrade version of library from PyPi
pip install --upgrade pyutilities
