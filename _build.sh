#!/usr/bin/env bash

###############################################################################
#
#   Build script for [pyutilities] project (library).
#   Script can be run from outside of virtual (pipenv) environment (from the
#   system shell) and from the pipenv environment as well (pipenv shell).
#
#   Created:  Dmitrii Gusev, 30.11.2021
#   Modified: Dmitrii Gusev, 19.02.2025
#
###############################################################################

source _bash_lib.sh

print_title "Build of [PyUtilities] library is starting..." "clear"

# -- I. Clean build and distribution folders
clean_distro_folders
sleep 2

# -- II. Clean caches and sync + lock pipenv dependencies
pipenv_venv_clean_and_update
sleep 2

# -- III. Executing [black] code formatter
printf "\n\n *** Executing [black] automatic code formatter *** \n\n"
pipenv run black ${VERBOSE} --line-length=110 --target-version=py310  src/
pipenv run black ${VERBOSE} --line-length=110 --target-version=py310  tests/
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
