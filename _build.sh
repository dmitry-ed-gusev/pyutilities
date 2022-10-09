#!/usr/bin/env bash

###############################################################################
#
#   Build and test script for [pyutilities] project.
#   Script can be run from outside of virtual (pipenv) environment (from the
#   system shell) and from the pipenv environment as well (pipenv shell).
#
#   Created:  Dmitrii Gusev, 30.11.2021
#   Modified: Dmitrii Gusev, 06.02.2022
#
###############################################################################

# todo: implement providing user/password via cmd line
# todo: implement different upload modes
# todo: implement fail upload on failing tests/checks
# todo: 


# -- set up encoding/language
export LANG="en_US.UTF-8"
# -- verbose output mode (on/off)
VERBOSE="--verbose"
# -- build directories
BUILD_DIR='build/'
DIST_DIR='dist/'
# -- pypi user/password
PYPI_USER="<specify PyPi user>"
PYPI_PASSWORD="<specify PyPi password>"
# -- upload mode: PROD (pypi.org), TEST (test.pypi.org), DRY-RUN (no upload, default)
UPLOAD_MODE="DRY-RUN"
# -- setup proxy for twine (comment/uncomment - if needed)
#export ALL_PROXY=<proxy host>:<port>

clear
printf "\nBuild is starting...\n"

# -- clean build/distribution/temporary folders
echo "Clearing temporary directories."
echo "Deleting ${BUILD_DIR}..."
rm -rf "${BUILD_DIR}"
echo "Deleting ${DIST_DIR}..."
rm -rf "${DIST_DIR}"

# -- clean caches and sync + lock pipenv dependencies (update from the file Pipfile.lock)
#pipenv clean ${VERBOSE}
#pipenv --clear ${VERBOSE}
#pipenv update --outdated ${VERBOSE}

# -- run pytest with pytest-cov (see pytest.ini/setup.cfg - additional parameters)
pipenv run pytest tests/

# -- run mypy - types checker
pipenv run mypy src/
pipenv run mypy tests/

# -- run black code formatter
pipenv run black src/ ${VERBOSE} --line-length 110
pipenv run black tests/ ${VERBOSE} --line-length 110

# -- run flake8 for checking code formatting
pipenv run flake8 src/
pipenv run flake8 tests/

# -- build two distributions: binary (whl) and source (tar.gz)
pipenv run python -m build

# -- upgrade versions of setuptools/wheel/twine
#pip install --user --upgrade setuptools wheel twine $1 $2  # install for the current user
#pip install --upgrade setuptools wheel twine $1 $2  # install globally

# create distribution for library in /dist catalog
#python3 setup.py sdist bdist_wheel

# -- upload new library to Test PyPi (TEST)
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# -- upload new library dist to real PyPi (PROD)
# twine upload -u vinnypuhh dist/*
