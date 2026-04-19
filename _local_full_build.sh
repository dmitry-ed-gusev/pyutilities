#!/usr/bin/env bash

#############################################################################################################
#
#   Local (developer's machine) full build script for the project [PyUtilities library].
#
#   Script does the following (in the specified order):
#       - call <./_local_init_venv.sh> script - rebuild the virtual environment and update dependencies to
#         the allowed upper versions
#       - activate the created virtual environment
#       - call <./_local_build.sh> script in the activated virtual environment for running unit tests
#         and various quality checks (see the script itself)
#
#   By default, all options are ON and all above mentioned actions will be performed. In order to cancel
#   (switch OFF) any action - use the appropriate cmd line boolean option (see below).
#
#   Script cmd line parameters and options with values:
#       * -nvb|--no-venv-build - turn OFF - cancel (skip) the virtual environment rebuilding (script call)
#       * -nb|--no-build - turn OFF - cancel (skip) the project build (activating venv, calling the build
#                          script, deactivating the venv)
#       * -h|--help - show this script usage message and exit (no actions)
#
#   Created:  Dmitrii Gusev, 19.04.2026
#   Modified: Dmitrii Gusev, 19.04.2026
#
###################################################################################################

# -- safe bash scripting / default encoding
set -euf -o pipefail
export _STEP_SLEEP=2

# -- script internal updatable defaults
OPTION_VENV_REBUILD=1 # ON -> rebuild virtual environment, update dependencies
OPTION_PROJECT_BUILD=1 # ON -> build project: unit tests, quality control, make distro

export _APP_NAME="[PyUtilities library]"

# -- parse cmd line arguments with values and init execution environment
while [[ $# -gt 0 ]]; do
    case $1 in

        # --- help screen/usage instructions
        -h|--help)
        printf "\nUsage: ./_local_full_build.sh [OPTIONS]\n"
        printf "\n[PyUtilities library] build. Dmitrii Gusev, 2026."
        printf "\nScript does the full build of the project [PyUtilities library]: venv rebuild, build."
        printf "\nScript OPTIONS:"
        printf "\n\t-nvb|--no-venv-build    - turn OFF - cancel the virtual environment rebuilding"
        printf "\n\t-nb|--no-build          - turn OFF - cancel the project build"
        exit 0
        ;;

        # --- turn OFF -> don't rebuild virtual environment
        -nvb|--no-venv-build)
        OPTION_VENV_REBUILD=0
        shift
        ;;

        # --- turn OFF -> don't build the project
        -nb|--no-build)
        OPTION_PROJECT_BUILD=0
        shift
        ;;

        *)
        # Handle positional arguments
        shift
        ;;

    esac
done

printf "\n=== %s project full build :: start. ===" "${_APP_NAME}"; sleep "${_STEP_SLEEP}"

# -- call script for virtual environment initialization/rebuilding
if (( OPTION_VENV_REBUILD )); then # <- ON by default
    printf "\n\n = [INFO] Rebuilding the virtual environment.\n"
    source ./_local_init_venv.sh
else
    printf "\n\n = [WARNING] SKIPPED: rebuilding the virtual environment.\n"
fi
sleep "${_STEP_SLEEP}"

# -- activating the virtual environment, building the project, deactivating environment
if (( OPTION_PROJECT_BUILD )); then # <- ON by default
    # - activate virtual environment
    printf "\n = [INFO] Activating the virtual environment...\n"
    source ./.venv/Scripts/activate
    printf "\n = [INFO] OK: the virtual environment activated.\n"; sleep "${_STEP_SLEEP}"
    # - build the project
    printf "\n = [INFO] Building the %s project.\n" "${_APP_NAME}"; source ./_local_build.sh
    # - deactivate virtual environment
    printf "\n = [INFO] Deactivating the virtual environment...\n"
    deactivate
    printf "\n = [INFO] OK: the virtual environment deactivated.\n"
else
    printf "\n = [WARNING] SKIPPED: building the project.\n"
fi
sleep "${_STEP_SLEEP}"

printf "\n=== %s project full build :: done. ===\n\n" "${_APP_NAME}"; sleep "${_STEP_SLEEP}"
