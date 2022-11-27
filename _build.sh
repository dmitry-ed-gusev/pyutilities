#!/usr/bin/env bash

###############################################################################
#
#   Build and test script for [pyutilities] project.
#   Script can be run from outside of virtual (pipenv) environment (from the
#   system shell) and from the pipenv environment as well (pipenv shell).
#
#   Created:  Dmitrii Gusev, 30.11.2021
#   Modified: Dmitrii Gusev, 27.11.2022
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
# todo: make this update optional - by cmd line key
printf "\n\nCleaning pipenv cache and update dependencies.\n\n"
pipenv clean ${VERBOSE}
pipenv update --outdated ${VERBOSE}
pipenv update ${VERBOSE}

# -- run black code formatter
printf "\n\nExecuting [black] automatic code formatter.\n"
pipenv run black src/ ${VERBOSE} --line-length 110
pipenv run black tests/ ${VERBOSE} --line-length 110

# -- run pytest with pytest-cov (see pytest.ini/setup.cfg - additional parameters)
printf "\n\nExecuting tests.\n\n"
pipenv run pytest tests/

# -- run mypy - types checker
printf "\n\nExecuting [mypy] types checker\n\n"
pipenv run mypy src/
pipenv run mypy tests/

# -- run flake8 for checking code formatting
printf "\n\nExecuting [flake8] code format checker\n\n"
pipenv run flake8 src/
pipenv run flake8 tests/

# -- build library distribution (binary whl and source (tar.gz)
# -- (option -s -> tar.gz, option -w -> whl (binary) distribution)
printf "\n\nBuilding distribution for [PyUtilities] library.\n\n"
pipenv run python -m build -s -w

printf "\nBuild finished.\n\n"
