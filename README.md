# Python Utilities Library

(C) 2018 - 2025, Dmitrii Gusev  
*Last update 17.07.2025*

## Project Description

Useful utilities/experimental modules/researches in python 3.10+. Contains a lot of useful python functions and scripts.
Some of the modules/scripts are just a research or experiments.
Project documentation is 'in progress' state :)

## CMD Line Integrations

- fedit
- echo-server
- ???

## Useful tech info and links

- [regex for floating number](https://stackoverflow.com/questions/12643009/regular-expression-for-floating-point-numbers)
- [string is a number](https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-represents-a-number-float-or-int)
- [download file](https://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3)
- [pypi - urllib3](https://pypi.org/project/urllib3/)
- [urllib3 - docs](https://urllib3.readthedocs.io/en/stable/)
- [docs from python](https://docs.python.org/3/howto/urllib2.html)
- [fake User Agent](https://github.com/hellysmile/fake-useragent)
- [HTTP status codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes)

## Versions history

### 2.0.0

Major release after a long time :) It includes a lot of changes and updates. Refactored most of the methods, added a lot of tests, improved documentation and modules/methods descriptions.

- removed all unnecessary modules or obsolete methods
- added several modules and methods from various projects
- fixed a lot of grammar issues ;)
- added socket-based echo-server (can be run from the cmd line)
- added powerful http client module
- all tests are on pytest library

### 1.0.1

- Minor fixes for the major release 1.0.0

### 1.0.0

- total refactoring of existing modules and scripts
- added convenient web client for various purposes (scraping)
- added pipenv for development
- reworked setup with setup.cfg
- added several automation scripts

### 0.13.3

- updated build mechanism with pipenv, instead of virtualenv and requirements.txt file

### 0.13.1

Updated library dependencies. Added openpyxl as support of xlsx format was removed from
xlrd library. Updated unit tests. Minor fixes and several code refactors. Doc updates. Removed windows batch script.

### 0.12.0

Significant update for library. Many changes were done and sometimes tested :).

Changes that were done:

- added pylog.py module, for logging purposes (convenience mostly). Method setup_logging() was moved here
  (from utils.py).
- method setup_logging() now is able to initialize logger by name and return it
- added deprecation of direct execution to utils.py
- added module strings.py for various convenient methods for strings (with unit tests)
- added unit tests modules for strings.py and pylog.py
- added pysftp.py module for working with SFTP protocol (currently - empty DRAFT!)
- added pyssh.py module for working with SSH protocol (currently - DRAFT!)
- added pymaven.py module for representing Maven functionality (not tested yet!)
- added pygit.py module for representing Git functionality (PyGit class)
- methods git_clean_global_proxy()/git_set_global_proxy() moved to pygit module
- added internal exception class PyUtilsException (module pyexception.py)
- added type hints for some classes methods/functions
- added shell script for executing unit tests with creating coverage report

### 0.5.5

Added compatibility with Python 3.7. Should also still work on Python 2.7. Let me know if it's not the case :)

### 0.5.4

Added method contains_key() to Configuration class.

### 0.5.3

Added one utility method - write_report_to_file(). Minor fixes, comments improvements.

### 0.5.0

Added ability for ConfigurationXls class to merge provided list of dictionaries on init. Added more unit test cases for ConfigurationXls class (initialization, dictionaries merge).

### 0.4.0

Added ability for Configuration class to merge list of dictionaries on init. Minor improvements,
added several unit test cases. Minor refactoring.

### 0.3.0

Added ConfigurationXls class. It extends (inherits) Configuration class with ability of loading configuration from XLS files, from specified sheet, as name=value pairs. Added some unit tests for new class. Added dependencies list: requirements.txt file.

### 0.2.0

Added tests and some new methods.

### 0.1.0

Initial version/release. Just draft of utilities library.
