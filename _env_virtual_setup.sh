#!/usr/bin/env bash

#############################################################################################################
#
#   Development environment setup script. Script can be used to re-create development virtual environment
#   from 'scratch'. Also sets up the local ipykernel for jupyter notebooks (with local dependencies).
#
#   Warning: script must be executed from shell, not from the virtual environment (pipenv or similar).
#
#   Created:  Dmitrii Gusev, 09.10.2022
#   Modified: Dmitrii Gusev, 19.02.2025
#
#############################################################################################################

# -- load bash library
source _bash_lib.sh

# -- starting the script
print_title "Python Dev Virtual Env (PIPENV) setup is starting..." "clear"
printf "We are here: [%s]\n" "$(pwd)"

# -- check system/python + upgrading pip/setuptools
check_system_and_pip

# -- setup pipenv virtual environment
pipenv_setup "pyutilities-ipykernel"

print_title "INFO: done creating virtual environments!"
