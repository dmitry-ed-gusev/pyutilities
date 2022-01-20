#!/usr/bin/env bash

#########################################################################################
#
#   Scriba Project development virtual environment setup script (for pipenv).
#
#   Warning: script must be used (run) from shell, not from the virtual
#            environment (pipenv shell).
#
#   Created:  Dmitrii Gusev, 12.11.2021
#   Modified: Dmitrii Gusev, 18.01.2022
#
#########################################################################################

# set up verbose mode (uncomment this line to enable it)
VERBOSE="--verbose"
# set up language (see all available - <locale -a>)
export LANG="en_US.UTF-8"
# set up build directories
BUILD_DIR='build/'
DIST_DIR='dist/'
# set up some additional parameters
IPYKERNEL_NAME='myscripts_scriba'

clear
printf "Virtual Python Environment RESET Starting\n\n"

# - upgrade existing pipenv installation
echo "Upgrading pipenv."
pip install --upgrade pipenv

# - remove existing virtual environment, clear caches
echo "Deleting virtual environment and clearing caches."
pipenv --rm "${VERBOSE}"
pipenv --clear "${VERBOSE}"

# - clean build and distribution folders
echo "Deleting ${BUILD_DIR}..."
rm -r "${BUILD_DIR}"
echo "Deleting ${DIST_DIR}..."
rm -r "${DIST_DIR}"

# install all pipenv dependencies (incl. dev)
pipenv install --dev "${VERBOSE}"

# install local ipykernel kernel
pipenv run ipython kernel install --user --name="${IPYKERNEL_NAME}"
# list installed ipykernels (simple check)
jupyter kernelspec list

# - update + update outdated dependencies
pipenv update --clear "${VERBOSE}"
pipenv update --outdated --clear "${VERBOSE}"

# clean pipenv environment (optional) + check for issues + show the current dependencies
#pipenv clean
pipenv check
pipenv graph

# we are done
echo "Environment set up is done. Please check dependencies..."
