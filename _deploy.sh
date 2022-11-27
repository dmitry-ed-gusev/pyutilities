#!/usr/bin/env bash

###############################################################################
#
#   Deployment script for [pyutilities] project.
#   Script can be run from outside of virtual (pipenv) environment (from the
#   system shell) and from the pipenv environment as well (pipenv shell).
#
#   Created:  Dmitrii Gusev, 27.11.2022
#   Modified: Dmitrii Gusev, 27.11.2022
#
###############################################################################

# -- safe bash scripting - fail-fast pattern (google for more info)
set -euf -o pipefail

# -- set up encoding/language
export LANG="en_US.UTF-8"

# -- upload new library to Test PyPi (TEST)
# printf "\n\nUploading new library dist to test pypi repo\n\n"
# pipenv run twine upload --repository-url https://test.pypi.org/legacy/ -u "$1" -p "$2" dist/*
# pipenv run twine upload --non-interactive --config-file .pypirc --repository pypitest dist/*

# -- upload new library dist to real PyPi (PROD)
printf "\n\nUploading library [pyutilities] to PyPi repository\n\n"
# todo: need to specify user/password via cmd line
# pipenv run twine upload -u "$1" -p "$2" dist/*
pipenv run twine upload --non-interactive --config-file .pypirc --repository pypi dist/*
