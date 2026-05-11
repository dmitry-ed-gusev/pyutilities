# -*- coding: utf-8 -*-

"""
Application logging init/managing module. For logging used loguru library. Provides flexible logging
with console and file output, rotation, retention, and compression.

Created:  Dmitrii Gusev, 06.04.2026
Modified: Dmitrii Gusev, 11.05.2026
"""

import logging
import sys
from pathlib import Path
from types import FrameType

from loguru import logger

# Log format and coloring constants (application + intercepted) - for more info see loguru details
DEFAULT_LOG_FORMAT = (
    "<b><green>{time:DD-MM-YYYY HH:mm:ss}</green></b> | "
    "<level>{level: <8}</level> | "
    "<cyan>{extra[name]}</cyan>:<cyan>{function}</cyan>:"
    "<cyan>{line}</cyan> - <level>{message}</level>\n"
)

INTERCEPTED_LOG_FORMAT = (
    "<b><green>{time:DD-MM-YYYY HH:mm:ss}</green></b> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:"
    "<cyan>{line}</cyan> - <level>{message}</level>\n"
)


class InterceptHandler(logging.Handler):
    """Intercept standard logging messages and redirect them to loguru. This allows Flask and other
    libraries using standard logging to use loguru. This class instance should be added to the logger
    as a handler - and all logging messages will be intercepted by loguru and printed/showed in the
    loguru output (console, log files).
    """

    def emit(self, record: logging.LogRecord) -> None:

        # Get corresponding Loguru level if it exists (for external captured message)
        try:
            level = logger.level(record.levelname).name  # matched log level for external message
        except ValueError:
            level = record.levelno  # fallback default

        # Find caller from where originated the logged message
        frame: FrameType | None = logging.currentframe()
        depth = 6  # in some examples this is set to = 6 (six), originally here was = 2 (two)
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        # emit the external captured log message
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class LoggerManager:  # pylint: disable=too-few-public-methods
    """Manages application logging using loguru. Some LoggerManager implementation features are:
    - Console and/or file logging
    - Logs files rotation (default 100MB) + retention (default 7 days)
    - Logs compression (zip) + configurable log level
    - Contextual logging with class/function/line information
    - Intercepts Flask and standard library logging
    """

    def __init__(self, level: str = "INFO", console: bool = True, file: str | None = None,
                 rotation: str = "100 MB", retention: str = "7 days", compression: str = "zip",
                 additional_loggers: dict[str, str] = None) -> None:
        """
        Initialize the logger manager class instance.
        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            console: Enable console logging (stdout)
            file: Log file path (None to disable file logging)
            rotation: Log rotation size (e.g., "10 MB", "100 MB", "1 GB")
            retention: Log retention period (e.g., "7 days", "1 week", "1 month")
            compression: Compression format for rotated logs ("zip", "gz", "bz2", "xz")
            additional_loggers: 
        """

        # internal state initialization
        self.level = level.upper()
        self.console = console
        self.file = file
        self.rotation = rotation
        self.retention = retention
        self.compression = compression
        self.additional_loggers = additional_loggers

        logger.remove()  # Remove default logger (in order to avoid duplicate messages)
        self._configure_logger()  # Configure logger (call internal method)
        self._intercept_standard_logging()  # Intercept standard logging (call internal method)

    def _configure_logger(self) -> None:
        """INTERNAL. Configure loguru logger based on settings. Internal method for class LoggerManager.
        This method configure the records formatting, creating and adding the necessary handlers to the
        loguru logger, some additional logger setup ().
        """

        # Custom formatter that handles both application logs (with extra[name]) and intercepted logs
        def format_record(record) -> str:
            # Map format based on whether 'name' exists in extra
            format_map: dict[bool, str] = {
                True: DEFAULT_LOG_FORMAT,  # Application logs with extra[name]
                False: INTERCEPTED_LOG_FORMAT,  # Intercepted logs from standard library
            }
            return format_map["name" in record["extra"]]

        # ! change some coloring of the log messages
        logger.level("DEBUG", color="<green>")

        # Define handlers configuration
        handlers = []  # handlers storage array

        if self.console:
            handlers.append(  # add console handler (write to console)
                {
                    "sink": sys.stdout,
                    "format": format_record,  # use the method above to format log record
                    "level": self.level,
                    "colorize": True,
                }
            )

        if self.file:
            # Ensure log directory exists (where logs should be stored)
            log_path: Path = Path(self.file)
            log_path.parent.mkdir(parents=True, exist_ok=True)  # create all necessary dirs (intermediate)

            handlers.append(  # add file handler (write to file specified)
                {
                    "sink": self.file,
                    "format": format_record,  # use the method above to format log record
                    "level": self.level,
                    "rotation": self.rotation,
                    "retention": self.retention,
                    "compression": self.compression,
                    "enqueue": True,  # Thread-safe logging
                }
            )

        # Add all configured handlers
        for handler_config in handlers:
            logger.add(**handler_config)

    def _intercept_standard_logging(self) -> None:
        """INTERNAL. Intercept standard library logging, used by external libraries and by the flask
        application itself (flask.app, werkzeug) and redirect to loguru. Also set level for some used
        libraries - for development/debug purposes. Internal method for class LoggerManager."""

        # Intercept werkzeug (Flask) logging (MUST: level=0, force=True -> intercept ALL!)
        logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

        # Intercept specific loggers (they are using python logging mechanism)
        for logger_name in ["werkzeug", "flask.app"]:
            log = logging.getLogger(name=logger_name)
            log.handlers = [InterceptHandler()]
            log.propagate = False

        # ! set the appropriate level for some libraries (reduce logging output amount, just a brevity)
        # logging.getLogger("zabbix_utils").setLevel("DEBUG")
        logging.getLogger("zabbix_utils").setLevel(Config.AZIM_ZABBIX_UTIL_LOGGING_LEVEL)

    @staticmethod
    def get_logger(name: str):
        """CLASS METHOD. Get a logger instance with a specific name (typically class name). Factory method,
        binds the specific name to the loguru logger and return the loguru logger.
        Args:
            name: Logger name (usually __name__ or class name)
        Returns:
            Logger instance bound with the name
        Usage:
            class MyService:
                def __init__(self):
                    self.logger = LoggerManager.get_logger(self.__class__.__name__)

                def my_method(self):
                    self.logger.info("Processing data")
        """
        return logger.bind(name=name)


def setup_logging(level: str = "INFO", console: bool = True, file: str | None = None,
                  rotation: str = "100 MB", retention: str = "7 days", compression: str = "zip",
                  ) -> LoggerManager:
    """MODULE METHOD. Setup application logging. This is the MAIN ENTRY POINT FOR configuring LOGGING
    in the application. Should be called once at application startup - this method creates and initializes
    the only  instance of the LoggerManager class.
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        console: Enable console logging (stdout)
        file: Log file path (None to disable file logging)
        rotation: Log rotation size (e.g., "10 MB", "100 MB", "1 GB")
        retention: Log retention period (e.g., "7 days", "1 week", "1 month")
        compression: Compression format for rotated logs ("zip", "gz", "bz2", "xz")
    Returns:
        LoggerManager instance
    Usage:
        from app.core.log import setup_logging

        # Console only (default)
        setup_logging(level="INFO")

        # File only
        setup_logging(console=False, file="logs/app.log")

        # Both console and file
        setup_logging(console=True, file="logs/app.log")
    """

    return LoggerManager(level=level, console=console, file=file, rotation=rotation,
                         retention=retention, compression=compression, )
