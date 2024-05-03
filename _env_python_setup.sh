#!/usr/bin/env bash

#############################################################################################################
#
#   General python environment setup/reset script. Script can be used to re-create python general/global
#   environment from 'scratch' or to get rid of some 'garbage' packages - unnecessary installed modules.
#   After the cleanup, script installs the following basic libraries: virtualenv, pipenv, jupyter, pytest,
#   pipx, poetry (using pipx).
#
#   This script works under following environments:
#       - MacOS, 10.14+ (ok, tested)
#       - Windows GitBash/MinGW (ok, tested)
#       - TBD -> linux debian/red hat (run on your own risk! not tested!)
#
#   Warning: script MUST be executed from shell, not from the virtual environment (pipenv or any other).
#
#   Created:  Dmitrii Gusev, 30.01.2022
#   Modified: Dmitrii Gusev, 03.05.2024
#
#   cspell:ignore pipx, virtualenv, virtualenvs, ensurepath, argcomplete
#
#############################################################################################################

# -- safe bash scripting
set -euf -o pipefail

# -- general setup - some variables
export LANG='en_US.UTF-8'
TMP_FILE="req.txt" # for cygwin/mingw

# -- some useful constants
MSG_RUN_AGAIN="\nWARNING: close the terminal and run script once again!\n"
MSG_NO_PYTHON="\nWARNING: no installed python 3 in the system!\n"
MSG_NO_PIP="\nWARNING: no installed pip/pip3 in the system!\n"
PYTHON_VERSION="3.10"

clear
printf "Python Development Environment setup is starting...\n\n"

# -- PRE-CHECK I. Machine type - setup some commands aliases, depending on the machine type
unameOut="$(uname -s)" # get machine name (short)
# - based on the machine type - setup aliases for python/pip
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

# -- PRE-CHECK II. Python presence on the machine.
printf "\nUsing python 3/pip 3 versions:\n"
${CMD_PYTHON} --version || { printf "%s" "${MSG_NO_PYTHON}" ; sleep 5 ; exit ; }
${CMD_PIP} --version || { printf "%s" "${MSG_NO_PIP}" ; sleep 5 ; exit ; }
sleep 3

# -- STEP I. Upgrading pip + setuptools (main tools, just for the case)
printf "\n--- Upgrading PIP+SETUPTOOLS (if there are updates) ---\n\n"
# pip --no-cache-dir install --upgrade pip # option I: working but not in a mingw/gitbash
${CMD_PYTHON} -m pip --no-cache-dir install --upgrade pip setuptools # option II: works in mingw/gitbash
printf "\n\n ** upgrading PIP+SETUPTOOLS - done **\n"
sleep 2

# -- freeze current global dependencies and re-install. Now works only for gitbash/mingw.
# --   TODO: do we need it for macos/linux?
if [[ $MACHINE == 'Cygwin' || $MACHINE == 'MinGW' ]]; then # cygwin/mingw

    printf "\n\n--- CYGWIN/MINGW: cleanup dependencies + re-install ---\n"
    printf "\n\n--- Freezing dependencies to the [%s] file ---\n" ${TMP_FILE}
    ${CMD_PIP} freeze > ${TMP_FILE}
    printf "\n\n ** freezing the current dependencies to the [%s] file - done **\n\n" ${TMP_FILE}
    # -- remove (uninstall) all global dependencies, freezed in the file
    printf "\n--- Uninstalling dependencies freezed to the [%s] file ---\n\n" ${TMP_FILE}
    ${CMD_PIP} uninstall -r ${TMP_FILE} -y || printf "Nothing to uninstall!"
    printf "\n\n ** uninstalling the current dependencies - done **\n"
    # -- list the current empty environment
    printf "\n\n--- The Current Empty Environment (no dependencies) ---\n\n"
    ${CMD_PIP} list
    sleep 5
    # -- remove temporary file
    rm ${TMP_FILE}
    printf "\n\n ** removing tmp file %s - done **\n\n" ${TMP_FILE}

elif [[ $MACHINE == 'Linux' ]]; then # linux system
    printf "\n\n--- We're on linux system - processing TBD... ---\n"
else # macos/unknown system
    printf "\n\n--- We're on macos or unknown system - processing TBD... ---\n"
fi

# -- STEP II. Installing necessary core dependencies/libraries/modules
printf "\n--- Installing (if not installed) and upgrading core dependencies to the global env ---\n\n"
${CMD_PIP} --no-cache-dir install virtualenv pipenv pytest jupyter pipx
${CMD_PIP} --no-cache-dir install --upgrade virtualenv pipenv pytest jupyter pipx
printf "\nInstallation is done!\n"
# -- execute [pipx ensurepath] + [pipx upgrade-all] - all pipx binaries to be on PATH + upgrade
printf "\nExecuting [pipx ensurepath]...\n"
pipx ensurepath --force || { printf "%s" "${MSG_RUN_AGAIN}" ; sleep 5 ; exit ; }
pipx upgrade-all
# -- install pipx shell autocomplete
printf "\nInstalling pipx shell completions...\n"
eval "$(register-python-argcomplete pipx)" || { printf "\nnot for bash/zsh\n" ; }
# -- install pythonXXX-venv package - only for linux/macos machines
if [[ $MACHINE != 'Cygwin' && $MACHINE != 'MinGW' ]]; then
    printf "\nInstalling [pythonXXX-venv] package...\n"
    sudo apt install python"${PYTHON_VERSION}"-venv || { printf "\nUnable to install pythonXXX-venv!\n" ; }
fi
printf "\n\n ** installing core dependencies - done **\n"

# -- STEP III. Installing poetry and initial setup --
printf "\n--- Installing [poetry] with [pipx] ---\n"
pipx install poetry --force
pipx ensurepath --force # update PATH with installed binaries
# -- setup poetry to store virtual environments with virtualenv
poetry config virtualenvs.path ~/.virtualenvs || { printf "%s" "${MSG_RUN_AGAIN}" ; sleep 5 ; exit ; }

# -- installing poetry shell autocomplete - for cygwin/mingw
if [[ $MACHINE == 'Cygwin' || $MACHINE == 'MinGW' ]]; then
    printf "\n--- MINGW/CYGWIN: installing terminal autocomplete ---\n\n"
    poetry completions bash >> ~/.bash_completion
    printf "\n** Autocomplete for poetry installed. **\n\n"
else # linux/macos
    printf "\n\n--- We're on linux - autocomplete TBD... ---\n\n"
    # TODO: pipx autocomplete for linux - ???
fi

# -- show poetry config
poetry config --list
sleep 5
printf "\n\n ** installing poetry - done **\n"

# -- end of the script
printf "\n\nPython Development Environment setup is done.\n\n\n"
