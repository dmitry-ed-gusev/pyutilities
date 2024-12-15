#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Examples of using logging with the [pyutilities] library.

    Created:  Dmitrii Gusev, 13.12.2024
    Modified: Dmitrii Gusev, 14.12.2024

    cSpell:ignore mylog levelname
"""

import logging

from importlib import reload
from pyutilities.utils.string_utils import trim2none

print("\n")

# -------------------------------------------------------------------------------------------------

# 0. -- no configured logger at all - no log output from the library
print(f"#0 -> trim result: [{trim2none('  string ', debug=True)}].")
print("\n")

# -------------------------------------------------------------------------------------------------

# 1. -- the simplest case - standard configuration with 'root' logger (this statement initializes the 'root' #       logger with the standard configuration - console output (level = NOTSET), warning level for the
#       logger itself, etc.). In this case the [pyutilities] library won't log anything (same as case #0).
logging.warning("Unformatted output with logging module (using 'root' logger)!")
print(f"#1 -> trim result: [{trim2none('  string ', debug=True)}].")
# 'reset' the logging module - to avoid 'side effects' on further examples
logging.shutdown()
# reload(logging)
print("\n")

# 2. -- simple case - standard configuration with the 'named' logger (this doesn't initializes the 'root' #       logger and uses the standard config for the 'named' logger). No logging from the [pyutilities]
#       library.
log = logging.getLogger("simple_logger")
log.setLevel(logging.DEBUG)
log.debug("DEBUG -> Logging output with logger!")
log.info("INFO -> Logging output with logger!")
log.warning("WARNING -> Logging output with logger!")
log.error("ERROR -> Logging output with logger!")
log.critical("CRITICAL -> Logging output with logger!")
print(f"#2 -> trim result: [{trim2none('  string ', debug=True)}].")
print("\n")

# 3. -- adding configuration to the named logger (not [pyutilities] logger!). Same as the previous case -
#       no logging output from the [pyutilities] library.
mylog = logging.getLogger("my_logger")
mylog.setLevel(logging.DEBUG)
# formatter for messages
standard_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
# err handler for logger - stream handler for console output
stream_handler_err = logging.StreamHandler()
stream_handler_err.setFormatter(standard_formatter)
stream_handler_err.setLevel(logging.ERROR)
# std handler for logger - stream handler for console output
stream_handler_std = logging.StreamHandler()
stream_handler_std.setFormatter(standard_formatter)
stream_handler_std.setLevel(logging.DEBUG)
# add handlers for logger
mylog.addHandler(stream_handler_err)
mylog.addHandler(stream_handler_std)
# some logging output
mylog.debug("Logging output with configured logger - set level DEBUG.")
mylog.info("Logging output with configured logger - set level INFO.")
mylog.warning("Logging output with configured logger - set level WARN.")
mylog.error("Logging output with configured logger - set level ERROR.")
mylog.critical("Logging output with configured logger - set level CRITICAL.")
print(f"#3 -> trim result: [{trim2none('  string ', debug=True)}].")
print("\n")

# 4. -- the case for initializing logger for the [pyutilities] library. Use it as an example, it's better
#       to initialize library's 'root' logger - 'pyutilities'. Some functions log only debug messages, some -
#       info/warn/error. Use appropriate level for your application.
mylog = logging.getLogger("pyutilities")
mylog.setLevel(logging.DEBUG)
mylog.propagate = False
standard_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(standard_formatter)
stream_handler.setLevel(logging.DEBUG)
mylog.addHandler(stream_handler)

print(mylog, mylog.handlers)

# some logging output
mylog.debug("Logging output with configured logger - set level DEBUG.")
mylog.info("Logging output with configured logger - set level INFO.")
mylog.warning("Logging output with configured logger - set level WARN.")
mylog.error("Logging output with configured logger - set level ERROR.")
mylog.critical("Logging output with configured logger - set level CRITICAL.")
print(f"#4 -> trim result: [{trim2none('  string ', debug=True)}].")
print("\n")
