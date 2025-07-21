#!/usr/bin/env bash

##############################################################################################################
#
#   Build script for [pyutilities] project (library). Script can be run from outside of the virtual
#   environment (from the system shell). This script perform the following:
#       - executing tests (with pytest)
#       - executing pylint checker
#
#   Created:  Dmitrii Gusev, 30.11.2021
#   Modified: Dmitrii Gusev, 21.07.2025
#
##############################################################################################################

#source _bash_lib.sh
set -euf -o pipefail
export LANG='en_US.UTF-8'

export DIST_DIR="dist/"
export VERBOSE="--verbose"
# export MYPY_FAILURE_SCORE="9.8"
export MYPY_FAILURE_SCORE="9.0"
export MYPY_THREADS_NUMBER="3"
export SRC_PATH="src/pyutilities/"

printf "=== Build the [PyUtilities] library :: starting. ===\n\n"

# -- Step 1. Run python tests with pytest and coverage (pytest-cov). See pyproject.toml for config.
# --         Fail if tests are not passed (even one simple test).
printf "\n = INFO: executing [pytest] with coverage.\n"
poetry run pytest tests/
sleep 1

# -- Step 2. Run [pylint] linter for the source code
printf "\n = INFO: executing [pylint] on the source code.\n"
poetry run pylint --output-format=colorized --fail-under="${MYPY_FAILURE_SCORE}" \
    -j "${MYPY_THREADS_NUMBER}" "${SRC_PATH}"
sleep 1

# -- Step 3. Run [mypy] on the source code
printf "\n = INFO: executing [mypy] on the source code.\n"
printf "\n   WARNING: skipped for now...\n"
# poetry run mypy "${SRC_PATH}"
sleep 1

# -- Step 4. Run [flake8] on the source code
printf "\n = INFO: executing [flake8] on the source code.\n"
printf "\n   WARNING: skipped for now...\n"
# poetry run flake8 "${SRC_PATH}"
sleep 1

# -- Step 5. Run [black] code formatter
printf "\n = INFO: executing [black] code formatter.\n"
poetry run black "${SRC_PATH}"
sleep 1

# -- Step 6. Run [isort] utility (imports sorting)
printf "\n = INFO: executing [isort] utility.\n"
poetry run isort --atomic "${SRC_PATH}"
sleep 1

# -- Step 7. Make [pyutilities] library distro
printf "\n = INFO: making [pyutilities] distro.\n"
# - cleanup before creating new distro
printf "\n = INFO: removing the temporary distribution directory.\n"
printf "\n\t - deleting [%s]... * \n" "${DIST_DIR}"
rm -r "${DIST_DIR}" || printf "%s doesn't exist!\n" "${DIST_DIR}"
# - remove python cache, precompiled python coverage files etc. - simple cleanup
printf "\n= INFO: removing python caches and pre-compiled files.\n"
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$|\,cover$)" | xargs rm -rf || \
    { printf "Nothing to remove!\n\n"; }
# - create tar.gz + whl files (distro)
poetry build
sleep 1

# - end of script and some output
printf "\n === Build the [PyUtilities] library :: done. ===\n\n"
