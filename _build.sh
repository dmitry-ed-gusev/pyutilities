#!/usr/bin/env bash

###############################################################################
#
#   Build and test script for [pyutilities] project.
#   Script can be run from outside of virtual (pipenv) environment (from the
#   system shell) and from the pipenv environment as well (pipenv shell).
#
#   Created:  Dmitrii Gusev, 30.11.2021
#   Modified: Dmitrii Gusev, 22.11.2022
#
###############################################################################

# -- safe bash scripting - fail-fast pattern (google for more info)
set -euf -o pipefail

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
printf "Build of [PyUtilities] library is starting...\n"
sleep 2

# -- clean build and distribution folders
printf "\nClearing temporary directories.\n"
printf "\nDeleting [%s]...\n" ${BUILD_DIR}
rm -r ${BUILD_DIR} || printf "%s doesn't exist!\n" ${BUILD_DIR}
printf "\nDeleting [%s]...\n" ${DIST_DIR}
rm -r ${DIST_DIR} || printf "%s doesn't exist!\n" ${DIST_DIR}

# -- clean caches and sync + lock pipenv dependencies (update from the file Pipfile.lock)
# todo: do we need this clean/update for build?
# todo: we can use key --outdated - ?
printf "\nCleaning pipenv cache and update dependencies.\n"
# todo: enable below lines
# pipenv clean ${VERBOSE}
# pipenv update ${VERBOSE}

# -- run pytest with pytest-cov (see pytest.ini/setup.cfg - additional parameters)
printf "\nExecuting tests.\n"
pipenv run pytest tests/

# -- run mypy - types checker
printf "\n\nExecuting [mypy] types checker\n\n"
pipenv run mypy src/
pipenv run mypy tests/

# -- run flake8 for checking code formatting
printf "\n\nExecuting [flake8] code format checker\n\n"
pipenv run flake8 src/
pipenv run flake8 tests/

# -- run black code formatter
printf "\n\nExecuting [black] automatic code formatter.\n"
pipenv run black src/ ${VERBOSE} --line-length 110
pipenv run black tests/ ${VERBOSE} --line-length 110

# -- build library distribution (binary whl and source (tar.gz)
printf "\nBuilding distribution for [PyUtilities] library.\n"
pipenv run python -m build -s -w

# -- upload new library to Test PyPi (TEST)
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# -- upload new library dist to real PyPi (PROD)
# twine upload -u vinnypuhh dist/*

printf "\nBuild finished.\n\n"
