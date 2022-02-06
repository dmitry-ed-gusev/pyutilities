#!/usr/bin/env bash
###############################################################################
#
#   General python environment setup/reset script. Script can be used to 
#   re-create python general environment from 'scratch'.
#   Script installs basic libraries:
#       - pipenv
#       - jupyter
#       - pytest
#
#   Warning: script must be used (run) from shell, not from the virtual
#            environment (pipenv shell).
#
#   Created:  Dmitrii Gusev, 12.11.2021
#   Modified: Dmitrii Gusev, 06.02.2022
#
###############################################################################


export LANG='en_US.UTF-8'
TMP_FILE="req.txt"

clear
printf "Python Development Environment setup is starting...\n\n"

# -- upgrading pip (just for the case)
pip install --upgrade pip
echo "  - upgrading pip - done"

# -- freeze current global dependencies
pip freeze > ${TMP_FILE}

# -- remove all dependencies
pip uninstall -r ${TMP_FILE} -y
printf "\n\n  - uninstalled current dependencies - done\n"

# -- list the current empty environment
printf "\n\n--- Current Empty Environment ---\n\n"
pip list
sleep 5

# -- remove temporary file
rm ${TMP_FILE}
printf "\n\n  - removing tmp file %s - done\n" ${TMP_FILE}

# -- install necessary dependencies
pip install pipenv pytest jupyter
echo "  - installing dependencies - done"

printf "\n\nPython Development Environment setup is done.\n"