#!/usr/bin/env bash

#############################################################################################################
#
#   Bash (shell) scripts library - list of functions/procedures for other scripts. Most of functions are
#   idempotent - check it before usage. Environment variables named starting with _xxx (underscore) are
#   intended for internal script usage.
#
#   Created:  Dmitrii Gusev, 04.01.2025
#   Modified: Dmitrii Gusev, 19.02.2025
#
#############################################################################################################

# TODO: finalize function for setting env variables from cmd line parameters.
# TODO: function for installing core python modules updates PATH multiple times (on mingw/gitbash) - fix it!
# TODO: implement several extended scenarios (see end of this script).

# -- safe bash scripting
set -euf -o pipefail
# -- default encoding for scripts and utilities
export LANG='en_US.UTF-8'

# -- default messages for the functions
export _MSG_NO_TITLE_PROVIDED="ERROR: no title provided!"
export _MSG_NO_SYS_PYTHON="ERROR: no installed python3 found in the system!"
export _MSG_NO_PROVIDED_PYTHON="ERROR: not provided python3 cmd!"
export _MSG_NO_SYS_PIP="ERROR: no installed pip/pip3 found in the system!"
export _MSG_NO_PROVIDED_PIP="ERROR: not provided pip/pip3 cmd!"
export _MSG_NO_PROVIDED_MACHINE_TYPE="ERROR: no machine type provided!"
export _MSG_NO_PROVIDED_IPYKERNEL_NAME="ERROR: no provided ipykernel name!"
export _MSG_RUN_AGAIN="WARNING: close the terminal and run script once again!"
export _MSG_NO_PROVIDED_VENV_FOLDER="ERROR: not provided venv folder name!"

# -- default python version
export _PYTHON_VERSION="3.10"
# -- default requirements files
export _REQUIREMENTS_FILE='requirements.txt' # prod file
export _REQUIREMENTS_DEV_FILE='requirements-dev.txt' # dev file
# -- verbose output mode (-v/-vv/-vvv - but may happens - not supported by some utils)
export _VERBOSE="--verbose"
# -- default distribution dirs
export _BUILD_DIR="build/"
export _DIST_DIR="dist/"

# -- date and time (for logging purpose)
_CURRENT_DATE=$(date +"%d-%m-%Y") || { printf "\nError while calculating system date!\n"; sleep 3; exit 1; }
export _CURRENT_DATE
_CURRENT_TIME=$(date +"%H:%M:%S") || { printf "\nError while calculating system time!\n"; sleep 3; exit 1; }
export _CURRENT_TIME


# ============================== Basic Procedures (building blocks) ==============================


process_cmd_line_args() { # ver. 1.0.0, 06.01.2025
    #
    # Processing cmd line arguments and setting the appropriate env variables.
    # TODO: finalize implementation
    #

    for arg in "$@"
    do
        case "$arg" in
        # - help/usage screen
        --help) echo "!!!" ;;
        # - system update
        -update)  UPDATE_SYSTEM=YES
                ;;
        # - no reboot after system update
        -no-reboot) REBOOT_AFTER_UPDATE=NO
                ;;
        # - set on debug mode
        -no-debug) DEBUG_MODE=false
                ;;
        # - print system statistics
        -stat) SHOW_STAT=YES
                ;;
        # - install base software
        -install-base) INSTALL_BASE=YES
                ;;
        # - install Java (Oracle JDK)
        -install-java) INSTALL_JAVA=YES
                ;;
        # - install Jenkins server
        -install-jenkins) INSTALL_JENKINS=YES
                ;;
        # - install Sonar server
        -install-sonar) INSTALL_SONAR=YES
                ;;
        # - install Hadoop
        -install-hadoop) INSTALL_HADOOP=YES
                ;;
        # - install Hive
        -install-hive) INSTALL_HIVE=YES
                ;;
        # - install MySql
        -install-mysql) INSTALL_MYSQL=YES
                ;;
        # - set proxy server value (implemented getting value from the option)
        -set-proxy)
                shift
                if test $# -gt 0; then
                    PROXY=$1
                    SET_PROXY=YES
                    echo "${PROXY}"
                else
                    echo "Error: no proxy server value specified!"
                    cat "${USAGE_FILE}"
                    exit 1
                fi
                shift
                ;;
        # - remove proxy (system and for APT)
        -unset-proxy) UNSET_PROXY=YES
                ;;
        esac
    done
}

print_title() { # ver. 2.1.0, 12.01.2025
    #
    # Prints title for script with date/time, clears the screen before.
    #
    # $1 - title to print, mandatory parameter
    # $2 - clear screen before (value = 'clear') or not (any other value or no value at all), optional

    # check title - fail fast
    [[ -z ${1-} ]] && { printf "\n%s\n" "${_MSG_NO_TITLE_PROVIDED}"; sleep 5; exit 1; }

    # print two new lines - if we won't clear screen, they will remain
    printf "\n\n"

    # should we clear the screen before
    { [[ -n ${2-} ]] && [[ ${2-} == 'clear' ]]; } && { clear; }

    # - clear screen and print the provided title
    printf "=== %s %s - ${1} ===\n\n" "${_CURRENT_DATE}" "${_CURRENT_TIME}"
}

check_system_environment() { # ver. 1.3.0, 11.01.2025
    #
    # Check the system environment and setup some environment variables (depending on the environment).
    # After check - perform some debug output - show env info. No expected arguments/parameters.
    # Setup variables: MACHINE, CMD_PYTHON, CMD_PIP (after successful execution)

    unameOut="$(uname -s)" # get machine name (short)
    # - based on the machine type - setup aliases (env variables)
    case "${unameOut}" in
        Linux*)     export _MACHINE_TYPE=Linux;  export _CMD_PYTHON=python3; export _CMD_PIP=pip3;;
        Darwin*)    export _MACHINE_TYPE=Mac;    export _CMD_PYTHON=python3; export _CMD_PIP=pip3;;
        CYGWIN*)    export _MACHINE_TYPE=Cygwin; export _CMD_PYTHON=python;  export _CMD_PIP=pip;; # win emu
        MINGW*)     export _MACHINE_TYPE=MinGW;  export _CMD_PYTHON=python;  export _CMD_PIP=pip;; # win emu
        *)          printf "Unknown machine: [%s]!" "${unameOut}"; exit 1;;
    esac

    # - debug output I - machine/python/pip
    printf "\nINFO: Machine type: [%s], using python: [%s], using pip: [%s].\n" \
        "${_MACHINE_TYPE}" "${_CMD_PYTHON}" "${_CMD_PIP}"
    # - debug output II - python/pip versions
    printf "\nINFO: Using python 3/pip 3 versions:\n"
    printf "\t"; "${_CMD_PYTHON}" --version || { printf "\n%s\n" "${_MSG_NO_SYS_PYTHON}"; sleep 5; exit 1; }
    printf "\t"; "${_CMD_PIP}" --version || { printf "\n%s\n" "${_MSG_NO_SYS_PIP}"; sleep 5; exit 1; }
    printf "\n"
}

check_system_python() { # ver. 2.2.0, 11.01.2025
    #
    # Checks and prints the system python 'site-packages' directories. Uses python's module 'site' and
    # simple python script (embedded in bash).
    #
    # $1 - expected python command (python/python3) as a first parameter, if not provided - tries to use
    #      env variable _CMD_PYTHON, that should be setup by procedure check_system_environment() (see above).

    # - fail-fast check and value selection - _LOCAL_PYTHON
    [[ -n ${1-} ]] && { _LOCAL_PYTHON=${1}; }
    { [[ -z ${_LOCAL_PYTHON-} ]] && [[ -n ${_CMD_PYTHON-} ]]; } && { _LOCAL_PYTHON=${_CMD_PYTHON}; }
    [[ -z ${_LOCAL_PYTHON-} ]] && { printf "\n%s\n" "${_MSG_NO_PROVIDED_PYTHON}"; sleep 5; exit 1; }
    printf "\nDEBUG: using python: [%s]\n" "$(which "${_LOCAL_PYTHON}")"

    # - show python paths
    printf "\nINFO: "; $_LOCAL_PYTHON -m site; printf "\n"
    # - show python packages dirs (global+user) <- python code
    $_LOCAL_PYTHON - << END
import site
global_pkg = site.getsitepackages()
users_pkg = site.getusersitepackages()
print(f"INFO:\nglobal packages path: [{global_pkg}].\nuser packages path: [{users_pkg}].")
END
}

clean_global_python() { # ver. 2.2.0, 11.01.2025
    #
    # In a global python environment cleans up the unnecessary modules: puts list to the file, removes
    # all modules from the file, shows empty environment.
    #
    # WARNING! Works only for mingw/gitbash!
    #
    # $1 - expected machine type (determined externally), if not provided - tries to use env variable
    #      _MACHINE_TYPE set up by check_system() procedure.
    # $2 - expected the pip/pip3 command, if not provided - tries to use env variable _CMD_PIP set up by
    #      check_system() procedure.

    # - fail-fast check and value selection - _LOCAL_MACHINE_TYPE
    [[ -n ${1-} ]] && { _LOCAL_MACHINE_TYPE=${1}; }
    { [[ -z ${_LOCAL_MACHINE_TYPE-} ]] && [[ -n ${_MACHINE_TYPE-} ]]; } \
        && { _LOCAL_MACHINE_TYPE=${_MACHINE_TYPE}; }
    [[ -z ${_LOCAL_MACHINE_TYPE-} ]] \
        && { printf "\n%s\n" "${_MSG_NO_PROVIDED_MACHINE_TYPE}"; sleep 5; exit 1; }
    printf "\nDEBUG: using machine type: [%s]\n" "${_LOCAL_MACHINE_TYPE}"

    # - fail-fast check and value selection - _LOCAL_PIP
    [[ -n ${2-} ]] && { _LOCAL_PIP=${1}; }
    { [[ -z ${_LOCAL_PIP-} ]] && [[ -n ${_CMD_PIP-} ]]; } && { _LOCAL_PIP=${_CMD_PIP}; }
    [[ -z ${_LOCAL_PIP-} ]] && { printf "\n%s\n" "${_MSG_NO_PROVIDED_PIP}"; sleep 5; exit 1; }
    printf "\nDEBUG: using pip: [%s]\n" "$(which "${_LOCAL_PIP}")"

    # - script itself
    printf "\nINFO: cleanup python dependencies.\n"
    if [[ ${_LOCAL_MACHINE_TYPE} == 'Cygwin' || ${_LOCAL_MACHINE_TYPE} == 'MinGW' ]]; then # <-- cygwin/mingw

        _TMP_FILE="req.txt" # <- temporary file for storing requirements
        # - freeze env to the tmp file
        printf "\nDEBUG: freezing dependencies to the [%s] file.\n" ${_TMP_FILE}
        ${_LOCAL_PIP} ${_VERBOSE} freeze > ${_TMP_FILE}
        # - remove (uninstall) all global dependencies, freezed in the tmp file
        printf "\nDEBUG: uninstalling dependencies freezed to the [%s] file\n" "${_TMP_FILE}"
        ${_LOCAL_PIP} ${_VERBOSE} uninstall -r ${_TMP_FILE} -y \
            || { printf "Nothing to uninstall (empty dependencies file)!"; }
        # - list the current empty global environment
        printf "\nDEBUG: the current empty environment (no dependencies):\n"
        ${_LOCAL_PIP} ${_VERBOSE} list; sleep 5
        # -- remove temporary file
        rm ${_TMP_FILE}

    elif [[ ${_LOCAL_MACHINE_TYPE} == 'Linux' ]]; then # <-- linux system

        printf "\nWARNING: linux system - processing TBD...\n" # TODO: implement for linux!

    else # <-- macos/unknown system

        printf "\nWARNING: macos/unknown system - processing TBD...\n" # TODO: implement for macos (???)

    fi

    printf "\n\t - done.\n"
}

upgrade_pip() { # ver. 3.2.1, 14.01.2025
    #
    # Upgrading pip + setuptools (core modules).
    #
    # $1 - expected python command, if not provided - tries to use env variable _CMD_PYTHON, that should be
    #      setup by procedure call check_system().
    # $2 - expected pip command, if not provided - tries to use env variable _CMD_PIP set up by
    #      check_system() procedure.
    # $3 - expected trusted host name (in order to skip cert check for pypi and same resources, this may
    #      be needed in the case, when procedure is called from inside the virtual environment).

    # - fail-fast check and value selection - _LOCAL_PYTHON
    [[ -n ${1-} ]] && { _LOCAL_PYTHON=${1}; }
    { [[ -z ${_LOCAL_PYTHON-} ]] && [[ -n ${_CMD_PYTHON-} ]]; } && { _LOCAL_PYTHON=${_CMD_PYTHON}; }
    [[ -z ${_LOCAL_PYTHON-} ]] && { printf "\n%s\n" "${_MSG_NO_PROVIDED_PYTHON}"; sleep 5; exit 1; }
    printf "\nDEBUG: using python: [%s]\n" "$(which "${_LOCAL_PYTHON}")"

    # - fail-fast check and value selection - _LOCAL_PIP
    [[ -n ${2-} ]] && { _LOCAL_PIP=${2}; }
    { [[ -z ${_LOCAL_PIP-} ]] && [[ -n ${_CMD_PIP-} ]]; } && { _LOCAL_PIP=${_CMD_PIP}; }
    [[ -z ${_LOCAL_PIP-} ]] && { printf "\n%s\n" "${_MSG_NO_PROVIDED_PIP}"; sleep 5; exit 1; }
    printf "\nDEBUG: using pip: [%s]\n" "$(which "${_LOCAL_PIP}")"

    # - check and value selection for 'trusted hosts'
    _TRUSTED_HOST=""
    [[ -n ${3-} ]] && { _TRUSTED_HOST="--trusted-host ${3}"; }

    # - upgrade pip + setuptools to the latest versions
    printf "\nINFO: Upgrading PIP + SETUPTOOLS\n"
    # shellcheck disable=SC2086
    ${_LOCAL_PYTHON} -m pip ${_VERBOSE} ${_TRUSTED_HOST} --no-cache-dir install --upgrade pip
    # shellcheck disable=SC2086
    ${_LOCAL_PIP} ${_VERBOSE} ${_TRUSTED_HOST} --no-cache-dir install --upgrade setuptools

    printf "\n\t - done.\n"
}

upgrade_core_python_dependencies() { # ver. 2.2.0, 11.01.2025
    #
    # Installing + upgrading (if installed) the core python global modules. List - see in the procedure
    # text itself. Also installing additional stuff: shell autocompletion, etc.
    #
    # $1 - expected machine type, if not provided - tries to use env variable
    #      _MACHINE_TYPE set up by check_system() procedure.
    # $2 - expected pip command, if not provided - tries to use env variable _CMD_PIP set up by
    #      check_system() procedure.

    # - fail-fast check and value selection - _LOCAL_MACHINE_TYPE
    [[ -n ${1-} ]] && { _LOCAL_MACHINE_TYPE=${1}; }
    { [[ -z ${_LOCAL_MACHINE_TYPE-} ]] && [[ -n ${_MACHINE_TYPE-} ]]; } \
        && { _LOCAL_MACHINE_TYPE=${_MACHINE_TYPE}; }
    [[ -z ${_LOCAL_MACHINE_TYPE-} ]] \
        && { printf "\n%s\n" "${_MSG_NO_PROVIDED_MACHINE_TYPE}"; sleep 5; exit 1; }
    printf "\nDEBUG: using machine type: [%s]\n" "${_LOCAL_MACHINE_TYPE}"

    # - fail-fast check and value selection - _LOCAL_PIP
    [[ -n ${2-} ]] && { _LOCAL_PIP=${1}; }
    { [[ -z ${_LOCAL_PIP-} ]] && [[ -n ${_CMD_PIP-} ]]; } && { _LOCAL_PIP=${_CMD_PIP}; }
    [[ -z ${_LOCAL_PIP-} ]] && { printf "\n%s\n" "${_MSG_NO_PROVIDED_PIP}"; sleep 5; exit 1; }
    printf "\nDEBUG: using pip: [%s]\n" "$(which "${_LOCAL_PIP}")"

    _PIPX_INSTALLED="yes"
    _POETRY_INSTALLED="yes"
    # check - were pipx and poetry installed before execution of this procedure
    printf "\nINFO: checking pipx installation...\n"
    pipx --version || { printf "\n!!! no pipx installed !!!\n"; _PIPX_INSTALLED="no"; }
    printf "\nINFO: checking poetry installation...\n"
    poetry --version || { printf "\n!!! no poetry installed !!!\n"; _POETRY_INSTALLED="no"; }

    # - install + upgrade core dependencies to the global python environment
    printf "\nINFO: Installing (if not installed) and upgrading core dependencies to the global env.\n"
    ${_LOCAL_PIP} ${_VERBOSE} --no-cache-dir install virtualenv pipenv pipx jupyter jupyterlab notebook
    ${_LOCAL_PIP} ${_VERBOSE} --no-cache-dir install --upgrade virtualenv pipenv pipx jupyter \
        jupyterlab notebook
    printf "\n\t - done.\n"

    if [[ $_PIPX_INSTALLED == "no" ]]; then # no pipx installed
        # - execute [pipx ensurepath] + [pipx upgrade-all] - all pipx binaries to be on PATH + upgrade
        printf "\nINFO: executing [pipx ensurepath].\n"
        pipx ensurepath --force || { printf "\n%s\n" "${_MSG_RUN_AGAIN}"; sleep 5; exit 1; }
    else # pipx was installed before - we don't need to execute
        printf "\nINFO: pipx already were installed - no need for [pipx ensurepath] execution!\n"
    fi

    # - execute [pipx upgrade-all]
    printf "\nINFO: executing [pipx upgrade-all].\n"
    pipx upgrade-all
    # - install pipx shell autocomplete
    printf "\nINFO: installing pipx shell completions.\n"
    eval "$(register-python-argcomplete pipx)" || { printf "\nnot for bash/zsh!\n" ; }

    # - install pythonXXX-venv package - only for linux/macos machines
    if [[ ${_MACHINE_TYPE} != 'Cygwin' && ${_MACHINE_TYPE} != 'MinGW' ]]; then
        printf "\nINFO: enabling pipx global operations.\n"
        sudo pipx ensurepath --global || { printf "\n%s\n" "${_MSG_RUN_AGAIN}"; sleep 5; exit 1; }
        printf "\nINFO: trying to install [pythonXXX-venv] package...\n"
        sudo apt install python"${_PYTHON_VERSION}"-venv \
            || { printf "\nUnable to install pythonXXX-venv!\n" ; }
    fi

    # - installing poetry and initial setup for it
    printf "\nINFO: installing [poetry] with [pipx].\n"
    pipx install poetry --force # install/re-install poetry with pipx
    pipx ensurepath --force # update PATH with installed binaries
    # - setup poetry to store virtual environments with virtualenv
    poetry config virtualenvs.path ~/.virtualenvs || { printf "\n%s\n" "${_MSG_RUN_AGAIN}"; sleep 5; exit 1; }
    # - installing poetry shell autocomplete - for cygwin/mingw only
    if [[ ${_MACHINE_TYPE} == 'Cygwin' || ${_MACHINE_TYPE} == 'MinGW' ]]; then
        printf "\nINFO: MINGW/CYGWIN -> installing terminal autocomplete.\n\n"
        poetry completions bash >> ~/.bash_completion
    else # linux/macos
        printf "\n\n--- We're on linux - autocomplete TBD... ---\n\n"
    fi

    # - show poetry config - debug output
    printf "\nDEBUG: showing poetry configuration:\n"
    poetry config --list

    printf "\n\t - done.\n"
}

clean_distro_folders() { # ver. 3.0.0, 19.02.2025
    #
    # Removing (recursively) distribution directories (build + dist) in the current directory. Also cleanup
    # python cache and precompiled files, coverage files, etc.

    # - deleting standard distribution directories
    printf "\nINFO: removing the temporary distribution directories.\n"
    printf "\n\t - deleting [%s]... * \n" ${_BUILD_DIR}
    rm -r ${_BUILD_DIR} || printf "%s doesn't exist!\n" "${_BUILD_DIR}"
    printf "\n\t - deleting [%s]... * \n" ${_DIST_DIR}
    rm -r ${_DIST_DIR} || printf "%s doesn't exist!\n" "${_DIST_DIR}"

    # - remove python cache, precompiled python. coverage files etc.
    printf "\nINFO: removing python caches and pre-compiled files.\n"
    find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$|\,cover$)" | xargs rm -rf || \
        { printf "Nothing to remove!\n\n"; }

    printf "\n\t - done.\n"
}

venv_recreate() { # ver. 1.3.0, 12.01.2025
    #
    # Creates/re-creates python virtual environment with virtualenv. Removes (if exists) the venv folder and
    # creates new one. After creation - activate the virtual environment and installs dependencies from
    # two requirements file: requirements.txt (prod dependencies) and requirements-dev.txt (dev dependencies).
    #
    # $1 - expected virtual environment folder name; mandatory parameter
    # $2 - expected python command, if not provided - tries to use env variable _CMD_PYTHON, that should be
    #      setup by procedure call check_system(); optional parameter
    # $3 - expected virtual environment name (prompt); optional parameter

    # - fail-fast check for virtual environment name
    [[ -z ${1-} ]] && { printf "\n%s\n" "${_MSG_NO_PROVIDED_VENV_FOLDER}"; sleep 5; exit 1; }
    printf "\nDEBUG: using venv folder name: [%s].\n" "${1}"

    # - fail-fast check and value selection - _LOCAL_PYTHON
    [[ -n ${2-} ]] && { _LOCAL_PYTHON=${2}; }
    { [[ -z ${_LOCAL_PYTHON-} ]] && [[ -n ${_CMD_PYTHON-} ]]; } && { _LOCAL_PYTHON=${_CMD_PYTHON}; }
    [[ -z ${_LOCAL_PYTHON-} ]] && { printf "\n%s\n" "${_MSG_NO_PROVIDED_PYTHON}"; sleep 5; exit 1; }
    printf "\nDEBUG: using python: [%s].\n" "$(which "${_LOCAL_PYTHON}")"

    # - check for the virtual environment prompt, if not provided - use folder name
    [[ -n ${3-} ]] && { _LOCAL_VENV_PROMPT=${3}; }
    [[ -z ${_LOCAL_VENV_PROMPT-} ]] && { _LOCAL_VENV_PROMPT="${1}"; }
    printf "\nDEBUG: using venv prompt: [%s].\n" "${_LOCAL_VENV_PROMPT}"

    # -- remove existing virtual environment
    printf "\nINFO: removing existing virtual environment at [%s].\n" "${1}"
    rm -rf "${1}" || { printf "\tError removing the virtual environment!\n"; }

    # -- create new virtual environment and activate it
    printf "\nINFO: creating new virtual environment."
    ${_LOCAL_PYTHON} -m venv "${1}" --prompt "${_LOCAL_VENV_PROMPT}"
    printf "'nINFO: activating created virtual environment [%s]." "${1}"
    # shellcheck disable=SC1091
    source "${1}/Scripts/activate"

    # -- upgrading pip in the virtual environment
    printf "\nINFO: upgrade pip  + setuptools into the activated virtual env.\n"
    upgrade_pip "python" "pip" "pypi.org"

    # -- installing all dependencies (runtime + develop time)
    pip ${_VERBOSE} --no-cache-dir install -r ${_REQUIREMENTS_FILE}
    pip ${_VERBOSE} --no-cache-dir install -r ${_REQUIREMENTS_DEV_FILE}
    printf "\n\t - done.\n"

    # -- show outdated dependencies in the virtual environment
    printf "\nINFO: virtual environment outdated dependencies list:\n\n"
    pip list --outdated
    printf "\n\t - done.\n"
}

pipenv_venv_prepare() { # ver. 1.2.0, 12.01.2025
    #
    # Preparing pipenv virtual env for re-generating from Pipfile (clears caches, removes Pipfile.lock, etc.)

    # - clearing pipenv/pip caches + removing existing virtual environment
    printf "\nINFO: deleting virtual environment and clearing pipenv caches.\n"
    pipenv --clear ${_VERBOSE} # clearing pipenv caches
    pipenv --rm ${_VERBOSE} || printf "\nWARNING: no virtual environment found for the project!\n"
    # - removing Pipfile.lock (in order to re-generate it)
    printf "\nINFO: removing Pipfile.lock.\n"
    rm Pipfile.lock || printf "\nWARNING: Pipfile.lock doesn't exist!\n"

    printf "\n\t - done.\n"
}

pipenv_venv_create() { # ver. 1.2.0, 19.02.2025
    #
    # Creating virtual environment after cleanup.

    printf "\nINFO: installing dependencies into pipenv virtual environment.\n"
    # - create the virtual environment - installing all dependencies
    pipenv install --dev --clear ${_VERBOSE}

    printf "\nINFO: list an outdated packages and update them (if possible).\n"
    # - list outdated packages
    pipenv update --outdated ${_VERBOSE} || printf "Packages check is done!\n\n"
    # - update outdated packages (run lock, then sync)
    pipenv update --dev --clear ${_VERBOSE}

    printf "\n\t - done.\n"
}

pipenv_venv_clean_and_update() { # ver. 1.0.0, 19.02.2025
    #
    # Cleaning the pipenv virtual environment and updating packages (if possible).

    # - print info
    printf "\nINFO: Cleaning pipenv cache and updating / upgrading dependencies."
    # - perform actions
    pipenv clean ${_VERBOSE}
    pipenv update --outdated ${_VERBOSE} || printf "Packages check is done!\n\n"  # list of outdated packages
    pipenv update --dev --clear ${_VERBOSE} # run lock, then sync
}

pipenv_venv_jupyter_kernel_install() { # ver. 1.1.0, 20.01.2025
    #
    # Install jupyter kernel locally for the current pipenv environment.
    #
    # $1 - expected ipykernel name

    # - if no ipykernel name provided - exit
    [[ -z ${1-} ]] && { printf "%s" "${_MSG_NO_PROVIDED_IPYKERNEL_NAME}"; sleep 5; exit 1; }

    # -- install local ipykernel for current module
    printf "\nINFO: installing local ipykernel + check.\n"
    pipenv run ipython kernel install --user --name="${1}"
    # -- list of installed kernels - just a debug
    jupyter kernelspec list

    printf "\n\t - done.\n"
}

pipenv_venv_check() { # ver. 1.1.0, 10.01.2025
    #
    # Checks the pipenv virtual environment for vulnerabilities and outdated packages.

    # - check for vulnerabilities
    printf "\nINFO: checking virtual environment for vulnerabilities.\n"
    pipenv check || printf "There are some issues with [pipenv check], check logs...\n"
    # - show outdated packages report
    printf "\nINFO: outdated packages list (pip list):\n"
    pipenv run pip list --outdated

    printf "\n\t - done.\n"
}

poetry_prepare_environment() { # ver. 1.0.0, 01.01.2025
    #
    # TBD

    true; # no-op for the procedure...

}

poetry_create_virtual_environment() { # ver. 1.0.0, 01.01.2025
    #
    # TBD

    true; # no-op for the procedure...

}

src_code_check() { # ver. 1.0.0, 19.02.2025
    #
    # Execute various python code checks before building the project.

    true;

}

build_project() { # ver. 1.0.0, 19.02.2025
    #
    # Building the project's distro with building tool.

    true;

}


pypi_publish() { # ver. 1.0.0, 01.01.2025
    #
    # Publishing project to pypi with twine.

    true;

}


# ============================== Extended Actions/Scenarios ==============================


check_system_and_pip() { # ver 2.0.0, 20.01.2025
    #
    # This procedure is just a shortcut for calling two checking env procedures and
    # upgrading pip + setuptools

    check_system_environment # <- check system env
    check_system_python "" # <- check system python
    upgrade_pip ""
}

python_setup() { # ver. 2.0.0, 20.01.2025
    #
    # Simple scenario for updating the system (global) python installation.

    check_system_and_pip
    clean_global_python ""
    upgrade_core_python_dependencies ""

}

venv_setup() { # ver. 2.1.0, 20.01.2025
    #
    # Scenario for creating/re-creating python virtual environment (with virtualenv).
    #
    # $1 - virtual environment name, if not provided - error occurs on the internal call venv_recreate().

    check_system_and_pip
    venv_recreate "${1}"

}

pipenv_setup() { # ver. 2.0.0, 20.01.2025
    #
    # Scenario for creating/re-creating python virtual environment (with pipenv).
    #
    # $1 - expected ipykernel name, if not provided - error occurs on the internal call.

    clean_distro_folders
    pipenv_venv_prepare
    pipenv_venv_create
    pipenv_venv_jupyter_kernel_install "${1}"
    pipenv_venv_check

}
