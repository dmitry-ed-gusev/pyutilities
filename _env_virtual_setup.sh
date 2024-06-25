#!/usr/bin/env bash

#############################################################################################################
#
#   Development environment setup script. Script can be used to re-create development virtual environment
#   from 'scratch'. Also sets up the local ipykernel for jupyter notebooks (with local dependencies).
#
#   Warning: script must be executed from shell, not from the virtual environment (pipenv or similar).
#
#   Created:  Dmitrii Gusev, 09.10.2022
#   Modified: Dmitrii Gusev, 05.05.2024
#
#   cspell:ignore ipykernel, ipykernels, ipython, pyutilities, kernelspec
#
#############################################################################################################

# -- safe bash scripting
set -euf -o pipefail

# -- verbose output mode
VERBOSE="--verbose"

# -- set up encoding/language
export LANG='en_US.UTF-8'
BUILD_DIR='build/'
DIST_DIR='dist/'

# -- local ipykernel name
IPYKERNEL_NAME='pyutilities_project_ipykernel'

# -- starting the script - clear screen, show title and go ahead...
clear
printf "Python Development Virtual Environment setup is starting...\n"

# -- setup some commands aliases, depending on the machine type
unameOut="$(uname -s)" # get machine name (short)
# - based on the machine type - setup aliases
case "${unameOut}" in
    Linux*)     MACHINE=Linux; CMD_PYTHON=python3; CMD_PIP=pip3;;
    Darwin*)    MACHINE=Mac; CMD_PYTHON=python3; CMD_PIP=pip3;;
    CYGWIN*)    MACHINE=Cygwin; CMD_PYTHON=python; CMD_PIP=pip;;
    MINGW*)     MACHINE=MinGW; CMD_PYTHON=python; CMD_PIP=pip;;
    *)          MACHINE="UNKNOWN:${unameOut}"; printf "Unknown machine: %s" "${MACHINE}"; exit 1
esac
# - just a debug output
printf "Machine type: [%s], using python: [%s], using pip: [%s].\n\n" \
    "${MACHINE}" "${CMD_PYTHON}" "${CMD_PIP}"
sleep 3

# -- I. Upgrading pip (just for the case)
printf "\n\n *** Upgrading PIP *** \n\n"
${CMD_PYTHON} -m pip --no-cache-dir install --upgrade pip # works in mingw/gitbash

# -- II. Upgrading pipenv (just for the case)
printf "\n\n *** Upgrading PIPENV *** \n\n"
${CMD_PIP} --no-cache-dir install --upgrade pipenv

# -- III. Remove existing virtual environment, clear pipenv caches
printf "\n\n *** Deleting virtual environment and clearing pipenv caches *** \n\n"
pipenv --rm ${VERBOSE} || printf "No virtual environment found for the project!\n"
pipenv --clear ${VERBOSE} # clearing pipenv caches

# -- IV. Cleaning build and distribution folders (deleting them)
printf "\n\n *** Clearing temporary directories. *** \n\n"
printf "\t\nDeleting [%s]...\n" ${BUILD_DIR}
rm -r ${BUILD_DIR} || printf "%s doesn't exist!\n" ${BUILD_DIR}
printf "\t\nDeleting [%s]...\n" ${DIST_DIR}
rm -r ${DIST_DIR} || printf "%s doesn't exist!\n" ${DIST_DIR}

# -- V. Removing Pipfile.lock (in order to re-generate it)
printf "\n\n *** Removing Pipfile.lock *** \n\n"
rm Pipfile.lock || printf "Pipfile.lock doesn't exist!\n"
sleep 3

# -- VI. Install all packages from Pipfile (default + dev packages). In case the installation failed (for
# --      example if hash is wrong/invalid) - we remove Pipfile.lock and execute installation cmd once more.
# --      Note: both command in {} (curly braces) are executed together in case first command fails!
printf "\n\n *** Installing and updating all dependencies. *** \n\n"
pipenv install --dev --clear ${VERBOSE} || { rm Pipfile.lock && pipenv install --dev --clear "${VERBOSE}"; }
pipenv update --outdated ${VERBOSE} || printf "Packages check is done!\n\n"  # list of outdated packages
pipenv update --dev --clear ${VERBOSE} # runs lock, then sync
sleep 3

# -- VII. Run pipenv clean
printf "\n\n *** Performing clean for pipenv environment. *** \n\n"
pipenv clean ${VERBOSE} # uninstalls all packages not specified in Pipfile.lock

# -- VIII. Install local ipykernel
printf "\n\n *** Installing local ipykernel + check it. *** \n\n"
pipenv run ipython kernel install --user --name=${IPYKERNEL_NAME}

# -- IX. List installed ipykernels
printf "\n\n *** Here is a list of locally installed ipykernels: *** \n\n"
jupyter kernelspec list
sleep 5

# -- X. Check for vulnerabilities and show dependencies graph
printf "\n\n *** Checking virtual environment for vulnerabilities. *** \n\n"
{ pipenv check; sleep 5; } || printf "There are some issues, check logs...\n"
pipenv graph
sleep 5

# -- XI. Shows outdated packages report
printf "\n\n *** Outdated packages list (pip list) *** \n\n"
pipenv run pip list --outdated
sleep 5

printf "\n\n"
