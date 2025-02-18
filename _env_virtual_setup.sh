#!/usr/bin/env bash

# cSpell: disable

#############################################################################################################
#
#   Development environment setup script. Script can be used to re-create development virtual environment
#   from 'scratch'. Also sets up the local ipykernel for jupyter notebooks (with local dependencies).
#
#   Warning: script must be executed from shell, not from the virtual environment (pipenv or similar).
#
#   Created:  Dmitrii Gusev, 09.10.2022
#   Modified: Dmitrii Gusev, 10.12.2024
#
#############################################################################################################

# -- safe bash scripting + encoding
set -euf -o pipefail
export LANG='en_US.UTF-8'

# -- verbose output mode, distro dirs
VERBOSE="--verbose"
BUILD_DIR='build/'
DIST_DIR='dist/'

# -- local ipykernel name
IPYKERNEL_NAME='pyutilities_project_ipykernel'

# -- starting the script - clear screen, show title and go ahead...
clear
printf "Python Development Virtual Environment (PIPENV) setup is starting...\n"

# -- PRE-CHECK I. Setup some commands aliases, depending on the machine type
unameOut="$(uname -s)" # get machine name (short)
# - based on the machine type - setup aliases
case "${unameOut}" in
    Linux*)     export MACHINE=Linux; CMD_PYTHON=python3; CMD_PIP=pip3;;
    Darwin*)    export MACHINE=Mac; CMD_PYTHON=python3; CMD_PIP=pip3;;
    CYGWIN*)    export MACHINE=Cygwin; CMD_PYTHON=python; CMD_PIP=pip;;
    MINGW*)     export MACHINE=MinGW; CMD_PYTHON=python; CMD_PIP=pip;;
    *)          export MACHINE="UNKNOWN:${unameOut}"; printf "Unknown machine: %s" "${MACHINE}"; exit 1
esac
# - just a debug output
printf "Machine type: [%s], using python: [%s], using pip: [%s].\n" \
    "${MACHINE}" "${CMD_PYTHON}" "${CMD_PIP}"

# -- PRE-CHECK II. Python presence (and version) on the machine.
printf "\nUsing python 3/pip 3 versions:\n"
${CMD_PYTHON} --version || { printf "%s" "${MSG_NO_PYTHON}" ; sleep 5 ; exit ; }
${CMD_PIP} --version || { printf "%s" "${MSG_NO_PIP}" ; sleep 5 ; exit ; }
sleep 3

# -- STEP I. Upgrading pip + setuptools (just for the case)
printf "\n--- Upgrading PIP + SETUPTOOLS (if there are updates) ---\n\n"
${CMD_PYTHON} -m pip --no-cache-dir install --upgrade pip setuptools  # works in mingw/gitbash
printf "\t - done.\n"
sleep 2

# -- STEP II. Upgrading pipenv (just for the case)
printf "\n--- Upgrading PIPENV ---\n\n"
${CMD_PIP} --no-cache-dir install --upgrade pipenv
printf "\t - done.\n"
sleep 2

# -- STEP III. Remove existing virtual environment, clear pipenv caches
printf "\n--- Deleting virtual environment and clearing pipenv caches ---\n\n"
pipenv --rm ${VERBOSE} || printf "No virtual environment found for the project!\n"
pipenv --clear ${VERBOSE} # clearing pipenv caches
printf "\t - done.\n"
sleep 2

# -- STEP IV. Cleaning build and distribution folders (deleting them) + Pipfile.lock
printf "\n--- Clearing temporary directories. ---\n\n"
printf "\t\nDeleting [%s]...\n" ${BUILD_DIR}
rm -r ${BUILD_DIR} || printf "%s doesn't exist!\n" ${BUILD_DIR}
printf "\t\nDeleting [%s]...\n" ${DIST_DIR}
rm -r ${DIST_DIR} || printf "%s doesn't exist!\n" ${DIST_DIR}
# - removing Pipfile.lock (in order to re-generate it)
printf "\t\nRemoving Pipfile.lock \n"
rm Pipfile.lock || printf "Pipfile.lock doesn't exist!\n"
printf "\t - done.\n"
sleep 3

# -- STEP V. Install all packages from Pipfile (default + dev packages). In case the installation failed (for
# --      example if hash is wrong/invalid) - we remove Pipfile.lock and execute installation cmd once more.
# --      Note: both command in {} (curly braces) are executed together in case first command fails!
printf "\n--- Installing and updating all dependencies. ---\n\n"
pipenv install --dev --clear ${VERBOSE} || { rm Pipfile.lock && pipenv install --dev --clear "${VERBOSE}"; }
pipenv update --outdated ${VERBOSE} || printf "Packages check is done!\n\n"  # list of outdated packages
pipenv update --dev --clear ${VERBOSE} # runs lock, then sync
printf "\t - done.\n"
sleep 3

# -- STEP VI. Run pipenv clean
printf "\n--- Performing clean for pipenv environment. ---\n\n"
pipenv clean ${VERBOSE} # uninstalls all packages not specified in Pipfile.lock
printf "\t - done.\n"
sleep 3

# -- STEP VII. Install local ipykernel
printf "\n--- Installing local ipykernel + check it. ---\n\n"
pipenv run ipython kernel install --user --name=${IPYKERNEL_NAME}
printf "\t - done.\n"
sleep 3

# -- STEP VIII. List installed ipykernels
printf "\n--- Here is a list of locally installed ipykernels: ---\n\n"
jupyter kernelspec list
printf "\t - done.\n"
sleep 5

# -- STEP IX. Check for vulnerabilities and show dependencies graph
printf "\n--- Checking virtual environment for vulnerabilities. ---\n\n"
{ pipenv check; sleep 5; } || printf "There are some issues, check logs...\n"
pipenv graph
printf "\t - done.\n"
sleep 5

# -- STEP X. Shows outdated packages report
printf "\n--- Outdated packages list (pip list) ---\n\n"
pipenv run pip list --outdated
printf "\t - done.\n"
sleep 5

# -- end of the script
printf "\n\nPython Development Virtual Environment (PIPENV) setup is done.\n\n\n"
