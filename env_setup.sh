#!/usr/bin/env bash

###############################################################################
#
#   Development environment setup script. Script can be used to re-create
#   development environment from 'scratch'.
#
#   Warning: script must be used (run) from shell, not from the virtual
#            environment (pipenv shell).
#
#   Created:  Dmitrii Gusev, 30.11.2021
#   Modified:
#
###############################################################################

# - some variables setup
export LANG='en_US.UTF-8'
BUILD_DIR='build/'
DIST_DIR='dist/'

echo "Development Environment setup started..."

# - remove unnecessary build/dist directories
echo "Deleting directory ${BUILD_DIR}"
rm -r ${BUILD_DIR}
echo "Deleting directory ${DIST_DIR}"
rm -r ${DIST_DIR}

# - upgrade pip (pip3)
echo "Upgrading pip/pip3..."
pip install --upgrade pip

# - remove existing virtual environment, clear caches
echo "Deleting virtual environment and clearing caches..."
pipenv --rm
pipenv --clear
pipenv clean

# - install all dependencies, including development + update
echo "Installing pipenv dependencies, updating outdated..."
pipenv install --dev

# - update dependencies + update outdated
pipenv update
pipenv update --outdated

# - check for vulnerabilities and show dependencies graph
echo "Checking virtual environment for vulnerabilities..."
pipenv check
pipenv graph
