#!/usr/bin/env bash

#############################################################################################################
#
#   Build script for [pyutilities] project (library). Script can be run from outside of the virtual
#   environment (from the system shell). This script perform the following:
#       - executing tests (with pytest)
#       - executing pylint checker
#
#   Created:  Dmitrii Gusev, 30.11.2021
#   Modified: Dmitrii Gusev, 19.04.2026
#
#############################################################################################################

# - safe scripting and encoding
set -euf -o pipefail
export LANG='en_US.UTF-8'

# - some useful setup (quality utilities, code paths, etc.)
export _APP_NAME="[PyUtilities library]"
export _DIST_DIR="dist/"
export _VERBOSE="--verbose"
export _PYLINT_FAILURE_SCORE="9.8"
export _WORKER_THREADS_NUMBER="4"
export _PYTEST_VERBOSITY=3
export _STEP_DELAY=1
export _SRC_PATH="src/pyutilities/"
export _TESTS_PATH="tests/"

clear; printf "=== Build the %s :: starting. ===\n\n" "${_APP_NAME}"; sleep "${_STEP_DELAY}"

# -- Step 1. Run python tests with pytest and coverage (pytest-cov). See pyproject.toml for config.
# --         Fail if tests are not passed (even one simple test).
printf "\n = INFO: executing [pytest] with coverage.\n"
pytest --verbosity "${_PYTEST_VERBOSITY}" "${_VERBOSE}" "${_TESTS_PATH}"; sleep "${_STEP_DELAY}"

# -- Step 2. Run [pylint] linter for the source code
printf "\n = INFO: executing [pylint] on the source code.\n"
pylint --output-format=colorized --fail-under="${_PYLINT_FAILURE_SCORE}" \
    --jobs "${_WORKER_THREADS_NUMBER}" "${_VERBOSE}" "${_SRC_PATH}"
sleep "${_STEP_DELAY}"

# -- Step 3. Run [mypy] on the source code
printf "\n = INFO: executing [mypy] on the source code.\n"
mypy "${_SRC_PATH}"; sleep "${_STEP_DELAY}"

# -- Step 4. Run [flake8] on the source code
printf "\n = INFO: executing [flake8] on the source code.\n"
flake8 "${_VERBOSE}" "${_SRC_PATH}"; sleep "${_STEP_DELAY}"

# -- Step 5. Run [black] code formatter
printf "\n = INFO: executing [black] code formatter.\n"
black --workers "${_WORKER_THREADS_NUMBER}" "${_VERBOSE}" "${_SRC_PATH}"; sleep "${_STEP_DELAY}"

# -- Step 6. Run [isort] utility (imports sorting)
printf "\n = INFO: executing [isort] utility.\n"
isort "${_VERBOSE}" --atomic "${_SRC_PATH}"; sleep "${_STEP_DELAY}"

# -- Step 7. Make [PyUtilities library] distro
printf "\n = INFO: making [pyutilities] distro.\n"

# - cleanup+distro step 1: before creating new distro, remove folder with the previous one
printf "\n = INFO: removing the temporary distribution directory.\n"
printf "\n\t - deleting [%s] directory...\n" "${_DIST_DIR}"
rm -rf "${_DIST_DIR}" || printf "%s doesn't exist!\n" "${_DIST_DIR}"; sleep "${_STEP_DELAY}"

# - cleanup+distro step 2: remove python cache, precompiled python coverage files etc.
printf "\n = INFO: removing python caches and pre-compiled files.\n\n"
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$|\,cover$)" | xargs rm -rf || \
    { printf "Nothing to remove!\n\n"; }; sleep "${_STEP_DELAY}"

# - cleanup+distro step 3: create tar.gz + whl files (distro)
printf "\n = INFO: creating tar.gz + whl distributions.\n\n"
poetry build; sleep "${_STEP_DELAY}"

# - end of script and some output
printf "\n === Build the %s :: done. ===\n\n" "${_APP_NAME}"; sleep "${_STEP_DELAY}"
