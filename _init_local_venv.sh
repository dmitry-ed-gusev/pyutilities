#!/usr/bin/env bash

####################################################################################################
#
#   Python virtual environment (venv) initialization script for bash (MinGW)/Linux. Script does
#   the following:
#       - check/show the machine architecture and python/pip/poetry, if no installed
#           python/pip/poetry found - exit (no further execution in the invalid environment)
#       - upgrade global pip (if there are updates)
#       - remove the current virtual environment (if exists) - delete environment folder
#       - cleanup the project folder: remove tmp dirs - see variable _TEMPORARY_DIRS
#       - create new virtual environment and activate it
#       - upgrade pip in the virtual environment and install dependencies into the newly created
#            virtual environment
#
#   Warning! Must-have pre-requisites for this script:
#       - python version 3.14.x (3.14+ is a must)
#       - the commands python/pip must exist in the bash (environment)
#       - poetry must be installed
#
#   Created:  Dmitrii Gusev, 21.07.2025
#   Modified: Dmitrii Gusev, 20.03.2026
#
# ##################################################################################################

# -- safe bash scripting
set -euf -o pipefail
export LANG='en_US.UTF-8'

# -- some useful script defaults
export _VERBOSE="--verbose"
export _VERBOSE_REMOVAL="--verbose"
export _TEMPORARY_DIRS=('.venv/' 'dist/' '.coverage/' '.pytest_cache/' '.mypy_cache/' '.hypothesis/')
export _STEP_DELAY=1

# -- script error messages
export _MSG_END_OF_STEP="= ========= done."
export _MSG_ERR_DATETIME_CALC="= [ERROR] Calculating system date/time issue!"
export _MSG_ERR_NO_APP="= [ERROR] Installed application doesn't found in the system: "
export _MSG_ERR_TMP_FOLDER_REMOVE="= [ERROR] There are issues during removing the temporary folder!"

# -- get current date/time (we don't need export it), clear screen and print title
_CURR_DATETIME="[$(date +"%d-%m-%Y %H:%M:%S")]" || { printf "\n%s\n" "${_MSG_ERR_DATETIME_CALC}"; exit 1; }
clear; printf "=== %s Python Virtual Env init :: starting. ===\n\n" "${_CURR_DATETIME}";

# -- Step I. Check the machine and determine the python/pip versions
printf "\n= [INFO] Step I: checking the architecture/python/pip/poetry versions.\n"
unameOut="$(uname -s)" # get machine name (short)
# - debug output I - machine/python/pip
printf "\n= [INFO] Machine type: [%s].\n" "${unameOut}"
# - debug output II - python/pip/poetry versions
printf "\n= [INFO] Using python/pip/poetry versions:\n"
printf "\t"; python --version 2>/dev/null || \
    { printf "\n%s[python]\n" "${_MSG_ERR_NO_APP}"; sleep 5; exit 1; }
printf "\t"; python -m pip --version 2>/dev/null || \
    { printf "\n%s[pip]\n" "${_MSG_ERR_NO_APP}"; sleep 5; exit 1; }
printf "\t"; poetry --version 2>/dev/null || \
    { printf "\n%s[poetry]\n" "${_MSG_ERR_NO_APP}"; sleep 5; exit 1; }
# -- debug output III - show python paths
printf "\n= [INFO] \n"; python -m site; printf "\n"
# - show python packages dirs (global+user) <- python code
python - << END
import site
global_pkg = site.getsitepackages()
users_pkg = site.getusersitepackages()
print(f"global packages path: [{global_pkg}].\nuser packages path: [{users_pkg}].")
END
printf "\n%s\n" "${_MSG_END_OF_STEP}"; sleep "${_STEP_DELAY}"

# -- Step II. Upgrade pip to the latest version (on the current python).
printf "\n= [INFO] Step II. Upgrading PIP in the global python environment.\n\n"
# shellcheck disable=SC2086
python -m pip ${_VERBOSE} --no-cache-dir install --upgrade pip
printf "\n%s\n" "${_MSG_END_OF_STEP}"; sleep "${_STEP_DELAY}"

# -- Step III. Remove existing virtual environment + other temporary folders
printf "\n= [INFO] Step III. Removing virtual environment + cleanup.\n"
# - remove temporary directories
for folder in "${_TEMPORARY_DIRS[@]}"; do
    printf "\n=        Removing the temporary dir [%s].\n\n" "$folder"
    rm -rf "${_VERBOSE_REMOVAL}" "$folder" || printf "\n=        %s\n" "${_MSG_ERR_TMP_FOLDER_REMOVE}"
    sleep 2
done
# - remove cashes, pre-compiled files, coverage, etc.
printf "\n=        Removing python caches and pre-compiled files\n"
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$|\.py,cover$)" | xargs rm -rf "${_VERBOSE_REMOVAL}" || \
{ printf "\n=        Nothing to remove, project is clean.\n"; }
printf "\n%s\n" "${_MSG_END_OF_STEP}"; sleep "${_STEP_DELAY}"

# -- Step IV. Some setup for the poetry utility
printf "\n= [INFO] Step IV. Updating the poetry configuration.\n\n"
# - update poetry configuration settings and show it
poetry ${_VERBOSE} config virtualenvs.in-project true
printf "\n=        Poetry current configuration:\n\n"
poetry ${_VERBOSE} config --list
printf "\n%s\n" "${_MSG_END_OF_STEP}"; sleep "${_STEP_DELAY}"

# -- Step V. Update dependencies, create virtual environment, install project
printf "\n= [INFO] Step V. Upgrade pip, lock + install/update dependencies (virtual env will be created).\n\n"
# - upgrade pip in the virtual environment
printf "\n=        Upgrading pip in the virtual environment:\n\n"
poetry ${_VERBOSE} run python -m pip install --upgrade pip
# - sync 'poetry.lock' with 'pyproject.toml' if the latter was changed since the last build
printf "\n=        Executing [poetry lock] command:\n\n"
poetry ${_VERBOSE} lock
# - install the project dependencies and update the project environment according to config (sync)
printf "\n=        Executing [poetry install] command:\n\n"
# poetry ${_VERBOSE} install --with extras
poetry ${_VERBOSE} install
printf "\n=        Executing [poetry sync] command in the virtual environment:\n\n"
poetry ${_VERBOSE} sync
# - update dependencies in the virtual environment
printf "\n=        Executing [poetry update] command:\n\n"
poetry ${_VERBOSE} update
printf "\n%s\n" "${_MSG_END_OF_STEP}"; sleep "${_STEP_DELAY}"

# -- Step VI. Show list of the outdated dependencies in the virtual environment
printf "\n= [INFO] Step VI. List of outdated dependencies in the virtual environment.\n\n"
poetry ${_VERBOSE} run pip list --outdated
printf "\n%s\n" "${_MSG_END_OF_STEP}"; sleep "${_STEP_DELAY}"

# -- print end-script message (with the current datetime)
_CURR_DATETIME="[$(date +"%d-%m-%Y %H:%M:%S")]" || { printf "\n%s\n" "${_MSG_ERR_DATETIME_CALC}"; exit 1; }
printf "\n === %s - Python Virtual Env init :: done. ===\n\n" "${_CURR_DATETIME}"; sleep 2
