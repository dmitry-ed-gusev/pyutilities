#!/bin/bash
#
# =======================================================================================
#
#   Install library [pyutilities] locally.
#
#   Created:  Dmitrii Gusev, 25.09.2018
#   Modified: Dmitrii Gusev, 19.05.2019
#
# =======================================================================================

# execute unit tests with coverage
./test_with_coverage.sh

# install library locally
pip install .
