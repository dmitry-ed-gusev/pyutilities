# -*- coding: utf-8 -*-

"""
Application logging init/managing module. For logging used loguru library. Provides flexible logging
with console and file output, rotation, retention, and compression.

This version offers great flexibility: it is possible, when the root logger level is set to one level,
to set up particular logger (by name) to the LOWER level (for example: root=INFO, my_logger=DEBUG).

Module usage example:

    With this setup:
        *setup_logging_flask(level="INFO", extra_loggers={"werkzeug": "DEBUG"})*

    result is:
        *logger.info("...") → ✅ allowed (INFO ≥ INFO)*
        *logger.debug("...") → ❌ filtered out (DEBUG < INFO)*
        *werkzeug.debug("...") intercepted → record["name"] = "werkzeug" or "werkzeug.debug" *
            *→ DEBUG allowed ✅*

⚠️ Note! Currently, if you pass:
            *extra_loggers={"werkzeug": "DEBUG", "werkzeug.debug": "WARNING"}*
          → only the first match (werkzeug) wins due to sorting by length ✅
          ! But that’s correct behavior: werkzeug.debug should inherit DEBUG unless
          !  explicitly overridden — so this is fine.

⚠️ Note! Werkzeug and flask.app are intercepted and set to INFO by default in setup_logging_flask(),
          but nested loggers like werkzeug.debug inherit the parent unless overridden explicitly
          in extra_loggers.

Created:  Dmitrii Gusev, 06.04.2026
Modified: Dmitrii Gusev, 21.07.2026
"""

import logging
import sys
from pathlib import Path
from types import FrameType
from typing import Optional

from loguru import logger

# - Default logger names for Flask (they needs special processing in case we are in Flask app)
FLASK_LOGGERS: list[str] = ["werkzeug", "flask.app"]

# - Log format and coloring constants (application + intercepted) - for more info see loguru details
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

# - File appender constants
FILE_APPENDER_ROTATION: str = "100MB"  # possible values: "1MB", "10MB", "1GB"
FILE_APPENDER_RETENTION: str = "7 days"  # possible values: "3 days", "1 week", "1 month"
FILE_APPENDER_COMPRESSION: str = "zip"  # possible values: "zip", "gz", "bz2", "xz"

# - guard flag - idempotency of the method _intercept_standard_logging()
_INTERCEPTED = False


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
            level = str(record.levelno)  # fallback default

        # Find caller from where originated the logged message
        frame: FrameType | None = logging.currentframe()
        depth = 6  # in some examples this is set to = 6 (six), originally here was = 2 (two)
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        # Bind original_name to clarify source logger in logs
        logger.opt(depth=depth, exception=record.exc_info).bind(original_name=record.name).log(
            level, record.getMessage()
        )


class LoggerFileAppenderConfig:  # pylint: disable=too-few-public-methods
    """Logger file appender configuration for the LoggerManager, if we need the file appender/handler.
    This class is needed only for configuration simplification. By default - the only console appender /
    handler will be added to the logger, no files logs.
    """

    def __init__(
        self,
        file: str | None = None,
        rotation: str = FILE_APPENDER_ROTATION,
        retention: str = FILE_APPENDER_RETENTION,
        compression: str = FILE_APPENDER_COMPRESSION,
    ):
        """Initialize the logger appenders config, with the necessary arguments/parameters.
        Args:
            file: Log file path (None to disable file logging)
            rotation: Log rotation size (e.g., "10 MB", "100 MB", "1 GB")
            retention: Log retention period (e.g., "7 days", "1 week", "1 month")
            compression: Compression format for rotated logs ("zip", "gz", "bz2", "xz")
        """

        self.file = file
        self.rotation = rotation
        self.retention = retention
        self.compression = compression


class LoggerManager:  # pylint: disable=too-few-public-methods, too-many-instance-attributes
    """Manages application logging using loguru. Some LoggerManager implementation features are:
    - Console and/or file logging
    - Logs files rotation (default 100MB) + retention (default 7 days)
    - Logs compression (zip) + configurable log level
    - Contextual logging with class/function/line information
    - Intercepts Flask and standard library logging
    """

    def __init__(
        self,
        level: str = "INFO",
        console: bool = True,
        log_file_config: Optional[LoggerFileAppenderConfig] = None,
        extra_loggers: Optional[dict[str, str]] = None,
    ) -> None:
        """Initialize the logger manager class instance.
        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL), default = INFO
            console: Enable/disable console logging (stdout), True/False, default = True
            log_file_config: LoggerFileAppenderConfig - appenders configuration class
            extra_loggers: dict[str, str] - <logger_name>: <logging_level> for additional loggers to be
                configured with the setup, default = None
        """

        # - init file appender state self fields, below will be assigned values, if any
        self.file: Optional[str] = None
        self.rotation: Optional[str] = None
        self.retention: Optional[str] = None
        self.compression: Optional[str] = None

        # - internal state initialization - file appender/handler
        if log_file_config and log_file_config.file and log_file_config.file.strip():
            self.file = log_file_config.file
            self.rotation = log_file_config.rotation
            self.retention = log_file_config.retention
            self.compression = log_file_config.compression

        # - internal state initialization - console appender and level
        self.level = level.upper()
        self.console = console

        # - internal state initialization - extra loggers and keys
        self.extra_loggers: Optional[dict[str, str]] = extra_loggers
        self.extra_loggers_keys: list[str] = (
            extra_loggers.keys() if extra_loggers else []  # type: ignore[assignment]
        )

        # Store effective per-logger levels for filtering (NEW-AI)
        self.logger_levels: dict[str, str] = {}
        if extra_loggers:
            for name, lvl in extra_loggers.items():
                if not lvl:
                    raise ValueError(f"Empty log level for logger '{name}'")
                try:
                    logger.level(lvl.upper())  # validate immediately
                except ValueError as e:
                    raise ValueError(f"Invalid log level '{lvl}' for logger '{name}'") from e
                self.logger_levels[name] = lvl.upper()

        logger.remove()  # Remove default logger (in order to avoid duplicate messages)
        self._configure_logger()  # Configure logger (call internal method)
        self._intercept_standard_logging()  # Intercept standard logging (call internal method)

    def _configure_logger(self) -> None:  # noqa: C901
        """INTERNAL. Configure loguru logger based on settings. Internal method for class LoggerManager.
        This method configure the records formatting, creating and adding the necessary handlers to the
        loguru logger, some additional logger setup ().
        """

        # Custom formatter that handles both application logs (with extra[name]) and intercepted logs.
        # This method is used as parameter for console appender - see below.
        def format_record(record) -> str:
            # Priority:
            #   1. If 'name' explicitly bound via logger.bind(name=...) → use {extra[name]}
            #   2. Otherwise (intercepted) → use {name} (loguru's record["name"])
            has_explicit_name = "name" in record["extra"]

            # For intercepted logs, enrich extra with original logger name for clarity
            if not has_explicit_name and "original_name" not in record["extra"]:
                record["extra"]["original_name"] = record["name"]

            return DEFAULT_LOG_FORMAT if has_explicit_name else INTERCEPTED_LOG_FORMAT

        # NEW-AI: Dynamic level filter respecting per-logger overrides
        def level_filter(record) -> bool:
            # Use logger name (from 'name' field — loguru's default for intercepted logs)
            logger_name = record["name"]
            effective_level = self.level  # fallback: global level

            # Find longest matching logger level override (e.g., "werkzeug" matches "werkzeug.debug")
            for key in sorted(self.logger_levels.keys(), key=len, reverse=True):
                if logger_name == key or logger_name.startswith(key + "."):
                    effective_level = self.logger_levels[key]
                    break

            try:
                level_no = logger.level(effective_level).no
            except ValueError:
                # Invalid level string fallback → INFO
                level_no = logger.level("INFO").no

            # Allow log only if its level is >= effective level
            return record["level"].no >= level_no  # type: ignore

        # ! change some coloring of the log messages
        logger.level("DEBUG", color="<green>")

        # Define handlers configuration
        handlers = []  # handlers storage array

        if self.console:  # if console appender/handler enabled - configure and add it

            handlers.append(  # add console handler (write to console)
                {
                    "sink": sys.stdout,
                    "format": format_record,  # use the method above to format log record
                    # "level": self.level,  # before NEW-AI
                    "level": 0,  # NEW-AI ← Pass *all* to filter (not filtered here, 0 - NOTSET, pass *all*)
                    "filter": level_filter,  # NEW-AI ← Apply custom filtering
                    "colorize": True,
                }
            )

        if self.file:  # if file appender/handler enabled - configure and add it

            log_path: Path = Path(self.file)  # Ensure log directory exists (where logs should be stored)
            log_path.parent.mkdir(parents=True, exist_ok=True)  # create all necessary dirs (intermediate)

            handlers.append(  # add file handler (write to file specified)
                {
                    "sink": self.file,
                    "format": format_record,  # use the method above to format log record
                    # "level": self.level,  # before NEW-AI
                    "level": 0,  # NEW-AI ← Pass *all* to filter (not filtered here, 0 - NOTSET, pass *all*)
                    "filter": level_filter,  # NEW-AI ← Apply custom filtering
                    "rotation": self.rotation,
                    "retention": self.retention,
                    "compression": self.compression,
                    "enqueue": True,  # Thread-safe logging
                }
            )

        # Add all configured handlers to logger
        for handler_config in handlers:
            logger.add(**handler_config)  # type: ignore[arg-type]

    def _intercept_standard_logging(self) -> None:
        """INTERNAL. Intercept standard library logging, used by external libraries and by the flask
        application itself (flask.app, werkzeug) and redirect to loguru. Also set level for some used
        libraries - for development/debug purposes. Internal method for class LoggerManager."""

        global _INTERCEPTED  # pylint: disable=global-statement
        if _INTERCEPTED:
            return  # avoid re-intercepting

        # Safe: replace root handlers instead of using basicConfig(force=True).
        # This avoids ValueError on multiple calls and ensures idempotency
        if not logging.root.handlers:
            # Only set up intercept if no handlers exist (prevent duplication)
            logging.root.handlers = [InterceptHandler()]
            logging.root.setLevel(0)  # same effect as level=0 in basicConfig

        # Intercept specific loggers (they are using python logging mechanism) - for Flask
        if self.extra_loggers:  # if there are extra loggers - process them
            for logger_name in self.extra_loggers_keys:
                if logger_name in FLASK_LOGGERS:  # special init for Flask loggers
                    log = logging.getLogger(name=logger_name)
                    log.handlers = [InterceptHandler()]
                    log.propagate = False
                else:  # just set level for other loggers
                    # ! set the appropriate level for some libraries - it may help to reduce
                    # !   logging output amount (brevity) or clarify libraries internals (more logging)
                    logging.getLogger(logger_name).setLevel(self.extra_loggers[logger_name])

        _INTERCEPTED = True  # Ensure idempotency: set only once

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


# pylint: disable=too-many-arguments, too-many-positional-arguments
def setup_logging(
    level: str = "INFO",
    console: bool = True,
    file: str | None = None,
    rotation: str = FILE_APPENDER_ROTATION,
    retention: str = FILE_APPENDER_RETENTION,
    compression: str = FILE_APPENDER_COMPRESSION,
    extra_loggers: Optional[dict[str, str]] = None,
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
        extra_loggers: dict[str, str] - <logger_name>: <logging_level> for additional loggers to be
            configured with the setup
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

    # create instance of file appender config - if file specified
    log_file_config: Optional[LoggerFileAppenderConfig] = (
        LoggerFileAppenderConfig(file=file, rotation=rotation, retention=retention, compression=compression)
        if file and file.strip()
        else None
    )

    return LoggerManager(
        level=level, console=console, log_file_config=log_file_config, extra_loggers=extra_loggers
    )


# pylint: disable=too-many-arguments, too-many-positional-arguments
def setup_logging_flask(
    level: str = "INFO",
    console: bool = True,
    file: str | None = None,
    rotation: str = FILE_APPENDER_ROTATION,
    retention: str = FILE_APPENDER_RETENTION,
    compression: str = FILE_APPENDER_COMPRESSION,
    extra_loggers: Optional[dict[str, str]] = None,
) -> LoggerManager:
    """MODULE METHOD. Setup application logging for Flask application. This is the MAIN ENTRY POINT
    FOR configuring LOGGING in the application. Should be called once at application startup - this
    method creates and initializes the only instance of the LoggerManager class.
    # ! Difference from the setup_logging() method is that the Flask loggers added to extra_loggers.
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        console: Enable console logging (stdout)
        file: Log file path (None to disable file logging)
        rotation: Log rotation size (e.g., "10 MB", "100 MB", "1 GB")
        retention: Log retention period (e.g., "7 days", "1 week", "1 month")
        compression: Compression format for rotated logs ("zip", "gz", "bz2", "xz")
        extra_loggers: dict[str, str] - <logger_name>: <logging_level> for additional loggers to be
            configured with the setup
    """

    # create instance of file appender config - if file specified
    log_file_config: Optional[LoggerFileAppenderConfig] = (
        LoggerFileAppenderConfig(file=file, rotation=rotation, retention=retention, compression=compression)
        if file and file.strip()
        else None
    )

    # add Flask loggers to the dictionary of extra_loggers
    if not extra_loggers:  # init extra loggers in case it is not initialized
        extra_loggers = {}

    for logger_name in FLASK_LOGGERS:
        extra_loggers[logger_name] = "INFO"  # by default set the INFO, but this value will be ignored

    return LoggerManager(
        level=level, console=console, log_file_config=log_file_config, extra_loggers=extra_loggers
    )
