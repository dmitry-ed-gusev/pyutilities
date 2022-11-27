# Python Utilities Library

(C) 2018 - 2022, Dmitrii Gusev  
*Last update 27.11.2022*

## Project Description

Useful utilities/experimantal modules/research in python 3.10+. Contains a lot of useful python functions and scripts. Some of the modules/scripts are just a research or experiments...

## Versions history

### 1.0.1

- Minor fixes for the major release 1.0.0

### 1.0.0

- total refactpring of exisiting modules and scripts
- added convenient web client for various purposes (scraping)
- added pipenv for development
- reworked setup with setup.cfg
- added several automation scripts

### 0.13.3

- updated build mechanism with pipenv, instead of virtualenv and requirements.txt file

### 0.13.1

Updated library dependencies. Added openpyxl as support of xlsx format was removed from
xlrd library. Updated unit tests. Minor fixes / refactorings. Doc updates. Removed windows batch script.

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
- added pymaven.py module for representing Maven functionalitys (not tested yet!)
- added pygit.py module for representing Git functionality (PyGit class)
- methods git_clean_global_proxy()/git_set_global_proxy() moved to pygit module
- added internal exception class PyUtilsException (module pyexception.py)
- added type hints for some classes methods/functions
- added shell script for executing unit tests with creating coverage report

### 0.5.5

Added compatability with Python 3.7. Should also still work on Python 2.7. Let me know if it's not the case :)

### 0.5.4

Added method contains_key() to Configuration class.

### 0.5.3

Added one utility method - write_report_to_file(). Minor fixes, comments improvements.

### 0.5.0

Added ability for ConfigurationXls class to merge provided list of dictionaries on init. Added more 
unit test cases for ConfigurationXls class (initialization, dictionaries merge).

### 0.4.0

Added ability for Configuration class to merge list of dictionaries on init. Minor improvements,
added several unit test cases. Minor refactoring.

### 0.3.0

Added ConfigurationXls class. It extends (inherites) Configuration class with ability of
loading configuration from XLS files, from specified sheet, as name=value pairs. Added some
unit tests for new class.  
Added dependencies list: requirements.txt file.
  
### 0.2.0

Added tests and some new methods.  

### 0.1.0

Initial version. Just draft of utilities library.
