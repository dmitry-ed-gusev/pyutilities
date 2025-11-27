#!/usr/bin/env bash

####################################################################################################
#
#   Python virtual environment initialization script for the project [pyutilities].
#
#   Script notes:
#       - script is intended for the Windows environment and should be used in GitBash/Cygwin/MinGW
#       - this project uses poetry for dependency management - be sure the utility is installed
#
#   Created:  Dmitrii Gusev, 21.07.2025
#   Modified: Dmitrii Gusev, 27.11.2025
#
# ##################################################################################################

# -- safe bash scripting
set -euf -o pipefail
export LANG='en_US.UTF-8'

# -- get current date and time
_CURRENT_DATE=$(date +"%d-%m-%Y") || { printf "\nError while calculating system date!\n"; sleep 3; exit 1; }
export _CURRENT_DATE
_CURRENT_TIME=$(date +"%H:%M:%S") || { printf "\nError while calculating system time!\n"; sleep 3; exit 1; }
export _CURRENT_TIME

# -- some useful script defaults
export _VERBOSE="--verbose"
export _MSG_END_OF_STEP="========== done."
export _CMD_PYTHON="-"
export _CMD_PIP="-"
export _MSG_NO_SYS_PYTHON="ERROR: no installed python/python3 found in the system!"
export _MSG_NO_SYS_PIP="ERROR: no installed pip/pip3 found in the system!"
export _MSG_NO_SYS_POETRY="ERROR: no installed poetry utility found in the system!"

# -- clear screen and print title
clear
printf "\n === %s %s - Python Virtual Env initializing :: starting ===\n\n" \
    "${_CURRENT_DATE}" "${_CURRENT_TIME}"
sleep 2

# -- Step I. Check the machine and determine the python/pip versions, print them.
printf "\n= INFO: Step I. Checking the machine architecture and python/pip/poetry versions.\n"
unameOut="$(uname -s)" # get machine name (short)
# - based on the machine type - setup aliases (env variables)
case "${unameOut}" in
    Linux*)     export _MACHINE_TYPE=Linux;  export _CMD_PYTHON=python3; export _CMD_PIP=pip3;;
    Darwin*)    export _MACHINE_TYPE=Mac;    export _CMD_PYTHON=python3; export _CMD_PIP=pip3;;
    CYGWIN*)    export _MACHINE_TYPE=Cygwin; export _CMD_PYTHON=python;  export _CMD_PIP=pip;; # win emu
    MINGW*)     export _MACHINE_TYPE=MinGW;  export _CMD_PYTHON=python;  export _CMD_PIP=pip;; # win emu
    *)          printf "Unknown machine: [%s]!" "${unameOut}"; exit 1;;
esac
# - debug output I - machine type/python cmd/pip cmd
printf "\n=       Machine type: [%s], using python: [%s], using pip: [%s].\n" \
    "${_MACHINE_TYPE}" "${_CMD_PYTHON}" "${_CMD_PIP}"

# - debug output II - python version/pip version/poetry version
printf "\n=       Using python 3/pip 3 versions:\n\n"
printf "\t"; "${_CMD_PYTHON}" --version || { printf "\n%s\n" "${_MSG_NO_SYS_PYTHON}"; sleep 5; exit 1; }
printf "\t"; "${_CMD_PIP}" --version || { printf "\n%s\n" "${_MSG_NO_SYS_PIP}"; sleep 5; exit 1; }
printf "\t"; poetry --verbose --version || { printf "\n%s\n" "${_MSG_NO_SYS_POETRY}"; sleep 5; exit 1; }
printf "\n========== done.\n"

# - debug output III - show python paths
printf "\n= INFO: \n"; $_CMD_PYTHON -m site; printf "\n"
# - show python packages dirs (global+user) <- python code
$_CMD_PYTHON - << END
import site
global_pkg = site.getsitepackages()
users_pkg = site.getusersitepackages()
print(f"\n= INFO:\nglobal packages path: [{global_pkg}].\nuser packages path: [{users_pkg}].")
END
printf "\n%s\n" "${_MSG_END_OF_STEP}"

# -- Step II. Upgrade pip to the latest version (on the current python).
printf "\n= INFO: Step II. Upgrading PIP in the global python environment.\n\n"
# shellcheck disable=SC2086
${_CMD_PYTHON} -m pip ${_VERBOSE} --no-cache-dir install --upgrade pip
printf "\n%s\n" "${_MSG_END_OF_STEP}"

# -- Step III. Remove existing virtual environment
printf "\n= INFO: Step III. Removing existing virtual environment - [.venv].\n\n"
rm -rf .venv || { printf "\tError removing the virtual environment!\n"; }
sleep 2
printf "\n========== done.\n"

# -- Step IV. Some setup for the poetry utility
printf "\n= INFO: Step IV. Updating the poetry configuration.\n\n"
# - list configuration
# poetry --verbose config --list; sleep 3
# - update configuration settings
poetry --verbose config virtualenvs.in-project true
# - list updated configuration
printf "\n=       Updated configuration:\n\n"
poetry --verbose config --list
printf "\n========== done.\n"; sleep 3

# -- Step V. Update dependencies, create virtual environment, install project
printf "\n= INFO: Step V. Updating dependencies, creating virtual env, installing editable project.\n\n"

printf "\n=       Executing [poetry update] command:\n\n"
poetry --verbose update

printf "\n=       Upgrading pip in the virtual environment:\n\n"
poetry --verbose run python -m pip install --upgrade pip

printf "\n=       Executing [poetry install] command:\n\n"
poetry --verbose install

printf "\n=       Executing [poetry sync] command in the virtual environment:\n\n"
poetry --verbose sync

printf "\n========== done.\n"

# -- Step VI. Show outdated dependencies list in the virtual environment
printf "\n= INFO: Step VI. Showing list of outdated dependencies in the project virtual environment.\n\n"
poetry run pip list --outdated
printf "\n========== done.\n"

# -- update the current date and time
_CURRENT_DATE=$(date +"%d-%m-%Y") || { printf "\nError while calculating system date!\n"; sleep 3; exit 1; }
export _CURRENT_DATE
_CURRENT_TIME=$(date +"%H:%M:%S") || { printf "\nError while calculating system time!\n"; sleep 3; exit 1; }
export _CURRENT_TIME
# -- print end-script message
printf "\n === %s %s - Python Virtual Env initializing :: done. ===\n\n" \
    "${_CURRENT_DATE}" "${_CURRENT_TIME}"
