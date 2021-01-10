#!/usr/bin/env bash

###############################################################################
#
#   Execute unit tests for pyutilities module with generating coverage report.
#   Unit tests for linux/unix OS.
#
#   Created:  Dmitrii Gusev, 17.05.2019
#   Modified: Dmitrii Gusev, 10.01.2020
#
###############################################################################


# install necessary requirements
pip install -r requirements.txt

# create virtual environment
virtualenv .venv

# activate environment
source .venv/bin/activate

# install necessary dependencies
pip install -r requirements.txt

# run unit tests with coverage
python3 -m nose2 -v -s pyutilities/tests --plugin nose2.plugins.junitxml -X --with-coverage --coverage pyutilities \
    --coverage-report xml --coverage-report html

# deactivate virtual environment (exit)
deactivate
