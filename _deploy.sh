#!/usr/bin/env bash

###############################################################################
#
#   Deployment script for [pyutilities] project.
#   Script can be run from outside of virtual (pipenv) environment (from the
#   system shell) and from the pipenv environment as well (pipenv shell).
#
#   Created:  Dmitrii Gusev, 27.11.2022
#   Modified: Dmitrii Gusev, 27.11.2025
#
###############################################################################

# -- safe bash scripting + encoding
set -euf -o pipefail
export LANG="en_US.UTF-8"

printf "=== Deploy the [PyUtilities] library :: starting. ===\n\n"

# -- Step I. Select .env* config file - by default we use the local config
export ENV_FILE=".env.deploy"
printf "\n = INFO: using deploy env file: [%s]\n" "${ENV_FILE}"

# -- Step II. Loading env variables from file to shell - get lines <name=value> not starting with #
# shellcheck disable=SC2046
[ ! -f "${ENV_FILE}" ] || export $(grep -v '^#' "${ENV_FILE}" | xargs)
printf "\n = INFO: all environment variables from file [%s] were loaded.\n" "${ENV_FILE}"
# - adding loaded token to poetry
poetry config pypi-token.pypi "${PYUTILITIES_TOKEN}"
printf "\n = INFO: added pypi token from the file [%s]\n" "${ENV_FILE}"
sleep 2

# -- Step III. Reload the local virtual environment
source ./_init_local_venv.sh
sleep 2

# -- Step IV. Build the project
source ./_build.sh
sleep 2

# -- Step V. Publishing the library to pypi.org
printf "\n = INFO: publishing the library to [pypi.org]\n\n"

# - key press before the actual publishing (deploy)
printf "\t"; read -r -p "Press any key before the deploy..."
# poetry publish --build --verbose --dry-run
poetry publish --verbose
sleep 2

printf "\n === Deploy the [PyUtilities] library :: done. ===\n\n"
