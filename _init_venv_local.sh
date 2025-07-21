#!/usr/bin/env bash

##############################################################################################################
#
#   Python virtual environment initialization script for the project [pyutilities].
#
#   Created:  Dmitrii Gusev, 21.07.2025
#   Modified:
#
# ###################################################################################################

# -- safe bash scripting
set -euf -o pipefail
export LANG='en_US.UTF-8'

# -- get current date and time
_CURRENT_DATE=$(date +"%d-%m-%Y") || { printf "\nError while calculating system date!\n"; sleep 3; exit 1; }
export _CURRENT_DATE
_CURRENT_TIME=$(date +"%H:%M:%S") || { printf "\nError while calculating system time!\n"; sleep 3; exit 1; }
export _CURRENT_TIME

# # -- some useful script defaults
# export _VERBOSE="--verbose"
# export _VIRTUAL_ENV_NAME=".venv--3.10"
# export _PIP_TRUSTED_HOST="--trusted-host pypi.org"
# export _REQUIREMENTS_FILE='requirements.txt' # prod file
# export _REQUIREMENTS_DEV_FILE='requirements-dev.txt' # dev file
# export _MSG_NO_SYS_PYTHON="ERROR: no installed python/python3 found in the system!"
# export _MSG_NO_SYS_PIP="ERROR: no installed pip/pip3 found in the system!"

# -- clear screen and print title
clear
printf "=== %s %s - Python Virtual Env initializing... ===\n\n" "${_CURRENT_DATE}" "${_CURRENT_TIME}"

# # -- check the machine and determine the python/pip versions
# printf "\n= INFO: checking the machine architecture and python/pip versions.\n"
# unameOut="$(uname -s)" # get machine name (short)
# # - based on the machine type - setup aliases (env variables)
# case "${unameOut}" in
#     Linux*)     export _MACHINE_TYPE=Linux;  export _CMD_PYTHON=python3; export _CMD_PIP=pip3;;
#     Darwin*)    export _MACHINE_TYPE=Mac;    export _CMD_PYTHON=python3; export _CMD_PIP=pip3;;
#     CYGWIN*)    export _MACHINE_TYPE=Cygwin; export _CMD_PYTHON=python;  export _CMD_PIP=pip;; # win emu
#     MINGW*)     export _MACHINE_TYPE=MinGW;  export _CMD_PYTHON=python;  export _CMD_PIP=pip;; # win emu
#     *)          printf "Unknown machine: [%s]!" "${unameOut}"; exit 1;;
# esac
# # - debug output I - machine/python/pip
# printf "\n= INFO: Machine type: [%s], using python: [%s], using pip: [%s].\n" \
#     "${_MACHINE_TYPE}" "${_CMD_PYTHON}" "${_CMD_PIP}"
# # - debug output II - python/pip versions
# printf "\n= INFO: Using python 3/pip 3 versions:\n"
# printf "\t"; "${_CMD_PYTHON}" --version || { printf "\n%s\n" "${_MSG_NO_SYS_PYTHON}"; sleep 5; exit 1; }
# printf "\t"; "${_CMD_PIP}" --version || { printf "\n%s\n" "${_MSG_NO_SYS_PIP}"; sleep 5; exit 1; }

# # -- show python paths
# printf "\n= INFO: "; $_CMD_PYTHON -m site; printf "\n"
# # - show python packages dirs (global+user) <- python code
# $_CMD_PYTHON - << END
# import site
# global_pkg = site.getsitepackages()
# users_pkg = site.getusersitepackages()
# print(f"global packages path: [{global_pkg}].\nuser packages path: [{users_pkg}].")
# END
# printf "\n========== done.\n"

# # -- upgrade pip + setuptools to the latest versions
# printf "\n= INFO: Upgrading PIP + SETUPTOOLS in the global python environment.\n"
# # shellcheck disable=SC2086
# ${_CMD_PYTHON} -m pip ${_VERBOSE} --no-cache-dir install --upgrade pip
# # shellcheck disable=SC2086
# ${_CMD_PIP} ${_VERBOSE} --no-cache-dir install --upgrade setuptools
# printf "\n========== done.\n"

# # -- remove existing virtual environment
# printf "\n= INFO: removing existing virtual environment at [%s].\n" "${_VIRTUAL_ENV_NAME}"
# rm -rf "${_VIRTUAL_ENV_NAME}" || { printf "\tError removing the virtual environment!\n"; }
# printf "\n========== done.\n"

# # -- create new virtual environment and activate it
# printf "\n= INFO: creating new virtual environment: [%s].\n" "${_VIRTUAL_ENV_NAME}"
# ${_CMD_PYTHON} -m venv "${_VIRTUAL_ENV_NAME}" --prompt "${_VIRTUAL_ENV_NAME}"
# printf "\n========== done.\n"

# # -- activate the newly created virtual environment
# # printf "\n= INFO: activating created virtual environment [%s].\n" "${_VIRTUAL_ENV_NAME}"
# if [[ ${_MACHINE_TYPE} == 'Cygwin' || ${_MACHINE_TYPE} == 'MinGW' ]]; then
#     printf "\n= INFO: MINGW/CYGWIN -> activating virtual environment: [%s].\n" "${_VIRTUAL_ENV_NAME}"
#     # shellcheck disable=SC1091
#     source "${_VIRTUAL_ENV_NAME}/Scripts/activate"
# else # linux/macos
#     printf "\n= INFO: Linux/MacOS -> activating virtual environment: [%s].\n" "${_VIRTUAL_ENV_NAME}"
#     # shellcheck disable=SC1091
#     source "${_VIRTUAL_ENV_NAME}/bin/activate"
# fi
# printf "\n========== done.\n"

# # - upgrade pip + setuptools to the latest versions
# printf "\n= INFO: Upgrading PIP + SETUPTOOLS in the virtual environment.\n"
# # shellcheck disable=SC2086
# ${_CMD_PYTHON} -m pip ${_VERBOSE} ${_PIP_TRUSTED_HOST} --no-cache-dir install --upgrade pip
# # shellcheck disable=SC2086
# ${_CMD_PIP} ${_VERBOSE} ${_PIP_TRUSTED_HOST} --no-cache-dir install --upgrade setuptools
# printf "\n========== done.\n"

# # -- installing all dependencies (runtime + develop time) into the activate virtual environment
# printf "\n= INFO: installing dependencies into the virtual environment.\n"
# ${_CMD_PIP} ${_VERBOSE} --no-cache-dir install -r ${_REQUIREMENTS_FILE}
# ${_CMD_PIP} ${_VERBOSE} --no-cache-dir install -r ${_REQUIREMENTS_DEV_FILE}
# printf "\n========== done.\n"

# # -- show outdated dependencies in the virtual environment
# printf "\n= INFO: virtual environment outdated dependencies list:\n\n"
# ${_CMD_PIP} list --outdated
# printf "\n========== done.\n"

# # -- print end-script message
# printf "\n=== %s %s - Python Virtual Env initialized. ===\n\n" "${_CURRENT_DATE}" "${_CURRENT_TIME}"

# # ###################################################################################################
# # #
# # #   Python virtual environment (venv) initialization script for git bash (MinGW)/Linux. Script does
# # #   the following:
# # #       - check the machine and select python/pip
# # #       - upgrade global pip + setuptools
# # #       - remove the current virtual environment (if exists - delete folder)
# # #       - create new virtual environment and activate it
# # #       - upgrade pip + setuptools and install dependencies into the newly created virtual
# # #         environment (requirements.txt/requirements-dev.txt)
# # #
# # #   Created:  Dmitrii Gusev, 11.11.2024
# # #   Modified: Dmitrii Gusev, 18.04.2025
# # #
# # ###################################################################################################

# # # -- safe bash scripting
# # set -euf -o pipefail
# # # -- default encoding for scripts and utilities
# # export LANG='en_US.UTF-8'

# # # -- get current date and time
# # _CURRENT_DATE=$(date +"%d-%m-%Y") || { printf "\nError while calculating system date!\n"; sleep 3; exit 1; }
# # export _CURRENT_DATE
# # _CURRENT_TIME=$(date +"%H:%M:%S") || { printf "\nError while calculating system time!\n"; sleep 3; exit 1; }
# # export _CURRENT_TIME

# # # -- some useful script defaults
# # export _VERBOSE="--verbose"
# # export _VIRTUAL_ENV_NAME=".venv-pyutils-3.10"
# # export _PIP_TRUSTED_HOST="--trusted-host pypi.org"
# # export _REQUIREMENTS_FILE='requirements.txt' # prod file
# # export _REQUIREMENTS_DEV_FILE='requirements-dev.txt' # dev file
# # export _MSG_NO_SYS_PYTHON="ERROR: no installed python/python3 found in the system!"
# # export _MSG_NO_SYS_PIP="ERROR: no installed pip/pip3 found in the system!"

# # # -- clear screen and print title
# # clear
# # printf "=== %s %s - Python Virtual Env initializing... ===\n\n" "${_CURRENT_DATE}" "${_CURRENT_TIME}"

# # # -- check the machine and determine the python/pip versions
# # printf "\n= INFO: checking the machine architecture and python/pip versions.\n"
# # unameOut="$(uname -s)" # get machine name (short)
# # # - based on the machine type - setup aliases (env variables)
# # case "${unameOut}" in
# #     Linux*)     export _MACHINE_TYPE=Linux;  export _CMD_PYTHON=python3; export _CMD_PIP=pip3;;
# #     Darwin*)    export _MACHINE_TYPE=Mac;    export _CMD_PYTHON=python3; export _CMD_PIP=pip3;;
# #     CYGWIN*)    export _MACHINE_TYPE=Cygwin; export _CMD_PYTHON=python;  export _CMD_PIP=pip;; # win emu
# #     MINGW*)     export _MACHINE_TYPE=MinGW;  export _CMD_PYTHON=python;  export _CMD_PIP=pip;; # win emu
# #     *)          printf "Unknown machine: [%s]!" "${unameOut}"; exit 1;;
# # esac
# # # - debug output I - machine/python/pip
# # printf "\n= INFO: Machine type: [%s], using python: [%s], using pip: [%s].\n" \
# #     "${_MACHINE_TYPE}" "${_CMD_PYTHON}" "${_CMD_PIP}"
# # # - debug output II - python/pip versions
# # printf "\n= INFO: Using python 3/pip 3 versions:\n"
# # printf "\t"; "${_CMD_PYTHON}" --version || { printf "\n%s\n" "${_MSG_NO_SYS_PYTHON}"; sleep 5; exit 1; }
# # printf "\t"; "${_CMD_PIP}" --version || { printf "\n%s\n" "${_MSG_NO_SYS_PIP}"; sleep 5; exit 1; }

# # # -- show python paths
# # printf "\n= INFO: "; $_CMD_PYTHON -m site; printf "\n"
# # # - show python packages dirs (global+user) <- python code
# # $_CMD_PYTHON - << END
# # import site
# # global_pkg = site.getsitepackages()
# # users_pkg = site.getusersitepackages()
# # print(f"global packages path: [{global_pkg}].\nuser packages path: [{users_pkg}].")
# # END
# # printf "\n========== done.\n"

# # # -- upgrade pip + setuptools to the latest versions
# # printf "\n= INFO: Upgrading PIP + SETUPTOOLS in the global python environment.\n"
# # # shellcheck disable=SC2086
# # ${_CMD_PYTHON} -m pip ${_VERBOSE} --no-cache-dir install --upgrade pip
# # # shellcheck disable=SC2086
# # ${_CMD_PIP} ${_VERBOSE} --no-cache-dir install --upgrade setuptools
# # printf "\n========== done.\n"

# # # -- remove existing virtual environment
# # printf "\n= INFO: removing existing virtual environment at [%s].\n" "${_VIRTUAL_ENV_NAME}"
# # rm -rf "${_VIRTUAL_ENV_NAME}" || { printf "\tError removing the virtual environment!\n"; }
# # printf "\n========== done.\n"

# # # -- create new virtual environment and activate it
# # printf "\n= INFO: creating new virtual environment: [%s].\n" "${_VIRTUAL_ENV_NAME}"
# # ${_CMD_PYTHON} -m venv "${_VIRTUAL_ENV_NAME}" --prompt "${_VIRTUAL_ENV_NAME}"
# # printf "\n========== done.\n"

# # # -- activate the newly created virtual environment
# # # printf "\n= INFO: activating created virtual environment [%s].\n" "${_VIRTUAL_ENV_NAME}"
# # if [[ ${_MACHINE_TYPE} == 'Cygwin' || ${_MACHINE_TYPE} == 'MinGW' ]]; then
# #     printf "\n= INFO: MINGW/CYGWIN -> activating virtual environment: [%s].\n" "${_VIRTUAL_ENV_NAME}"
# #     # shellcheck disable=SC1091
# #     source "${_VIRTUAL_ENV_NAME}/Scripts/activate"
# # else # linux/macos
# #     printf "\n= INFO: Linux/MacOS -> activating virtual environment: [%s].\n" "${_VIRTUAL_ENV_NAME}"
# #     # shellcheck disable=SC1091
# #     source "${_VIRTUAL_ENV_NAME}/bin/activate"
# # fi
# # printf "\n========== done.\n"

# # # - upgrade pip + setuptools to the latest versions
# # printf "\n= INFO: Upgrading PIP + SETUPTOOLS in the virtual environment.\n"
# # # shellcheck disable=SC2086
# # ${_CMD_PYTHON} -m pip ${_VERBOSE} ${_PIP_TRUSTED_HOST} --no-cache-dir install --upgrade pip
# # # shellcheck disable=SC2086
# # ${_CMD_PIP} ${_VERBOSE} ${_PIP_TRUSTED_HOST} --no-cache-dir install --upgrade setuptools
# # printf "\n========== done.\n"

# # # -- installing all dependencies (runtime + develop time) into the activate virtual environment
# # printf "\n= INFO: installing dependencies into the virtual environment.\n"
# # ${_CMD_PIP} ${_VERBOSE} --no-cache-dir install -r ${_REQUIREMENTS_FILE}
# # ${_CMD_PIP} ${_VERBOSE} --no-cache-dir install -r ${_REQUIREMENTS_DEV_FILE}
# # printf "\n========== done.\n"

# # # -- show outdated dependencies in the virtual environment
# # printf "\n= INFO: virtual environment outdated dependencies list:\n\n"
# # ${_CMD_PIP} list --outdated
# # printf "\n========== done.\n"

# # # -- print end-script message
# # printf "\n=== %s %s - Python Virtual Env initialized. ===\n\n" "${_CURRENT_DATE}" "${_CURRENT_TIME}"
