#!/usr/bin/env bash

###############################################################################
#
#   Deployment script for [pyutilities] project.
#   Script can be run from outside of virtual (pipenv) environment (from the
#   system shell) and from the pipenv environment as well (pipenv shell).
#
#   Created:  Dmitrii Gusev, 27.11.2022
#   Modified: Dmitrii Gusev, 25.11.2025
#
###############################################################################

# -- safe bash scripting + encoding
set -euf -o pipefail
export LANG="en_US.UTF-8"

printf "=== Deploy the [PyUtilities] library :: starting. ===\n\n"

# -- select .env* config file - by default we use the local config
export ENV_FILE=".env.local"
# -- if provided cmd line option - use its value
[[ -n ${2-} ]] && { export ENV_FILE=${2}; }
printf "\nINFO: using env file: [%s]\n" "${ENV_FILE}"

# -- loading environment variables from file to shell: if file exists - get lines <name=value> not starting
#    with # and execute <export name=value>
# shellcheck disable=SC2046
[ ! -f "${ENV_FILE}" ] || export $(grep -v '^#' "${ENV_FILE}" | xargs)
printf "\nINFO: all environment variables from file [%s] were loaded.\n" "${ENV_FILE}"


# -- upload new library to Test PyPi (TEST)
# printf "\n\nUploading new library dist to test pypi repo\n\n"
# pipenv run twine upload --repository-url https://test.pypi.org/legacy/ -u "$1" -p "$2" dist/*
# pipenv run twine upload --non-interactive --config-file .pypirc --repository pypitest dist/*

# -- upload new library dist to real PyPi (PROD)
printf "\n\nUploading library [pyutilities] to PyPi repository\n\n"
# todo: need to specify user/password via cmd line
# pipenv run twine upload -u "$1" -p "$2" dist/*
pipenv run twine upload --non-interactive --config-file .pypirc --repository pypi dist/*

printf "\n === Deploy the [PyUtilities] library :: done. ===\n\n"
