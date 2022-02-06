#!/usr/bin/env bash
###############################################################################
#
#   Development environment setup script. Script can be used to re-create
#   development environment from 'scratch'.
#
#   Warning: script must be used (run) from shell, not from the virtual
#            environment (pipenv shell).
#
#   Created:  Dmitrii Gusev, 12.11.2021
#   Modified: Dmitrii Gusev, 06.02.2022
#
###############################################################################


# -- verbose output mode
VERBOSE="--verbose"
# -- set up encoding/language
export LANG='en_US.UTF-8'
BUILD_DIR='build/'
DIST_DIR='dist/'
# -- local ipykernel name
IPYKERNEL_NAME='python_template_ipkernel'

clear
printf "Development Virtual Environment setup is starting...\n\n"

# -- upgrade pip
echo "Upgrading pip."
pip install --upgrade pip

# -- upgrading pipenv (just for the case)
echo "Upgrading pipenv."
pip install --upgrade pipenv

# -- remove existing virtual environment, clear caches
echo "Deleting virtual environment and clearing caches."
pipenv --rm ${VERBOSE}
pipenv --clear ${VERBOSE}

# -- clean build and distribution folders
echo "Clearing temporary directories."
echo "Deleting ${BUILD_DIR}..."
rm -r "${BUILD_DIR}"
echo "Deleting ${DIST_DIR}..."
rm -r "${DIST_DIR}"

# -- removing Pipfile.lock (re-generate it)
echo "Removing Pipfile.lock"
rm Pipfile.lock

# -- install all dependencies, incl. development
echo "Installing dependencies, updating all + outdated."
pipenv install --dev ${VERBOSE}

# -- install local ipykernel
echo "Installing local ipykernel + check"
pipenv run ipython kernel install --user --name=${IPYKERNEL_NAME}
# -- list installed ipykernels
jupyter kernelspec list
sleep 5

# -- update all + outdated
# todo: do we need these updates?
#pipenv update --clear ${VERBOSE}
#pipenv update --outdated --clear ${VERBOSE}

# - check for vulnerabilities and show dependencies graph
echo "Checking virtual environment for vulnerabilities."
pipenv check
pipenv graph

# - outdated packages report
printf "\n\nOutdated packages list (pip list):\n"
pipenv run pip list --outdated