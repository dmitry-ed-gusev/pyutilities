#!/usr/bin/env bash

###############################################################################
#
#   Build script for [pyutilities] project (library).
#   Script can be run from outside of virtual (pipenv) environment (from the
#   system shell) and from the pipenv environment as well (pipenv shell).
#
#   Created:  Dmitrii Gusev, 30.11.2021
#   Modified: Dmitrii Gusev, 06.05.2024
#
#   cspell:ignore pyutilities, isort
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

# -- I. Clean build and distribution folders
printf "\n\n *** Clearing temporary directories *** \n\n"
printf "\nDeleting [%s]...\n" ${BUILD_DIR}
rm -r ${BUILD_DIR} || printf "%s doesn't exist!\n" ${BUILD_DIR}
printf "\nDeleting [%s]...\n" ${DIST_DIR}
rm -r ${DIST_DIR} || printf "%s doesn't exist!\n" ${DIST_DIR}
sleep 2

# -- II. Clean caches and sync + lock pipenv dependencies
printf "\n\n *** Cleaning pipenv cache and update/upgrade dependencies ***\n\n"
pipenv clean ${VERBOSE}
pipenv update --outdated ${VERBOSE} || printf "Packages check is done!\n\n"  # list of outdated packages
pipenv update --dev --clear ${VERBOSE} # run lock, then sync
sleep 2

# -- Step 8. Clear local python cache. Remove python caches and pre-compiled files (*.pyc) -
# --         starting from the current dir. We won't copy cache into distribution folder.
# printf "\n\n ***** Removing python caches and pre-compiled files\n"
# find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf || printf "Nothing to remove!\n\n"
# sleep 2

# -- III. Executing [black] code formatter
printf "\n\n *** Executing [black] automatic code formatter *** \n\n"
pipenv run black src/ ${VERBOSE} --config .black
pipenv run black tests/ ${VERBOSE} --config .black
sleep 2

# -- IV. Executing [mypy] types checker
printf "\n\n *** Executing [mypy] types checker *** \n\n"
pipenv run mypy src/
pipenv run mypy tests/
sleep 2

# -- V. Executing [flake8] for checking code formatting
printf "\n\n *** Executing [flake8] code format checker *** \n\n"
pipenv run flake8 src/
pipenv run flake8 tests/
sleep 2

# -- VI. Executing [isort] utility (imports sorting)
printf "\n\n *** Executing [isort] utility *** \n\n"
pipenv run isort --atomic .
sleep 2

# -- VII. Executing pytest with pytest-cov (see config - pytest.ini/setup.cfg)
printf "\n\n *** Executing tests *** \n\n"
pipenv run pytest tests/
sleep 2

# -- VIII. Building library distribution: binary whl and source archive (tar.gz),
# --      see options: -s -> tar.gz, -w -> whl (binary distribution)
printf "\n\n *** Building distribution for [PyUtilities] library *** \n\n"
pipenv run python -m build -s -w

printf "\nBuild finished.\n\n"
sleep 5
