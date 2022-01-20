#!/usr/bin/env bash

#########################################################################################
#
#   General setup/update script for the main python environment.
#
#   Warning: script must be used (run) from shell, not from the virtual
#            environment (pipenv shell).
#
#   Created:  Dmitrii Gusev, 18.01.2022
#   Modified:
#
#########################################################################################

TMP_FILE="req.txt"

clear
printf "Python Environment RESET Starting\n\n"

# freeze current pip depende
pip freeze > "${TMP_FILE}"
echo "- environment freeze -> done"

# delete everything + auto "yes" answer
pip uninstall -r "${TMP_FILE}" -y
echo "- uninstall -> done"

# list clean python environment and wait for 5sec
printf "\n--- Clean environment ---\n\n"
pip list 
printf "\n\n"
sleep 5

# update pip
pip install --upgrade pip
echo "- pip update -> done"

# install necessary common dependencies
# todo: do we need pytest installed globally?
pip install pipenv pytest jupyter
echo "- common dependencies install -> done"

# remove tmp file
rm "${TMP_FILE}"
echo "- temporary file ${TMP_FILE} remove -> done"

# list all installed things
pip list

printf "\n\nPython Environment RESET is done.\n"
