#!/usr/bin/env bash

###################################################################################################
#
#   General python environment setup/reset script. Script can be used to re-create python
#   general/global environment from 'scratch' or to get rid of some 'garbage' packages - unnecessary
#   installed modules. After the cleanup, script installs the following basic libraries: virtualenv,
#   pipenv, pipx, poetry, jupyter, jupyterlab, notebook
#
#   This script works under following environments:
#       - MacOS, 10.14+
#       - Windows GitBash/MinGW
#       - linux debian/red hat -> TBD
#
#   Warning: script must be used (run) from shell, not from the virtual environment (pipenv shell)!
#
#   Created:  Dmitrii Gusev, 10.01.2025
#   Modified: Dmitrii Gusev, 19.02.2025
#
###################################################################################################

# -- load bash library
source _bash_lib.sh

print_title "Python Dev Environment setup is starting..." "clear"

# -- python setup
python_setup

print_title "Python Dev Environment setup is done!"
