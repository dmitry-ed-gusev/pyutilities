# -*- coding: utf-8 -*-

import io
import logging
import os
import sys
import tempfile
from pathlib import Path

import pytest
from hypothesis import given, strategies as st

from pyutilities.log.log_manager import (
    LoggerManager,
    LoggerFileAppenderConfig,
    InterceptHandler,
    setup_logging,
    setup_logging_flask,
    FLASK_LOGGERS,
)


# === FIXTURES ===
@pytest.fixture(autouse=True)
def reset_state():
    """Reset loguru + logging state between tests."""
    from loguru import logger
    logger.remove()

    import pyutilities.log.log_manager as lm_mod
    lm_mod._INTERCEPTED = False

    logging.root.handlers.clear()
    logging.root.setLevel(logging.WARNING)
    yield


# === UNIT TESTS ===

class TestInterceptHandler:
    """Test InterceptHandler — using real sinks, not mocks."""

    def test_emits_with_original_name_bound(self):
        """Verify InterceptHandler binds 'original_name' to extra."""
        record = logging.LogRecord(
            name="test.logger", level=logging.INFO, pathname="", lineno=0,
            msg="Test message", args=(), exc_info=None
        )
        handler = InterceptHandler()

        output = io.StringIO()
        from loguru import logger
        logger.add(output, format="{message} | extra: {extra}")

        handler.emit(record)

        assert "Test message" in output.getvalue()
        assert "original_name" in output.getvalue()
        assert "test.logger" in output.getvalue()

    @pytest.mark.parametrize("level_name", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    def test_maps_levels(self, level_name):
        """Verify standard levels are converted to loguru levels."""
        record = logging.LogRecord(
            name="x", level=getattr(logging, level_name), pathname="", lineno=0,
            msg=f"msg at {level_name}", args=(), exc_info=None
        )
        handler = InterceptHandler()

        output = io.StringIO()
        from loguru import logger
        logger.add(output, format="{level} | {message}")

        handler.emit(record)

        assert f" | msg at {level_name}" in output.getvalue()
        assert level_name in output.getvalue()

    # def test_fallback_for_unknown_level(self):
    #     """Verify non-standard levels don’t crash (e.g., level=9999 → '9999')."""
    #     record = logging.LogRecord(
    #         name="x", level=9999, pathname="", lineno=0,
    #         msg="unknown level", args=(), exc_info=None
    #     )
    #     handler = InterceptHandler()

    #     output = io.StringIO()
    #     from loguru import logger
    #     logger.add(output, format="{message}")

    #     handler.emit(record)

    #     assert "unknown level" in output.getvalue()
    #     # Should not crash; level appears as "9999" (string)
    #     assert "9999" in output.getvalue() or "INFO" in output.getvalue()


class TestLoggerManager:
    """Core LoggerManager tests — using actual sinks."""

    def test_init_console_only(self):
        lm = LoggerManager(level="DEBUG", console=True)
        assert lm.level == "DEBUG"
        assert lm.console is True
        assert lm.file is None

    # def test_init_file_only(self):
    #     with tempfile.TemporaryDirectory() as tmpdir:
    #         log_file = os.path.join(tmpdir, "app.log")
    #         cfg = LoggerFileAppenderConfig(file=log_file)
    #         lm = LoggerManager(level="INFO", console=False, log_file_config=cfg)
    #         assert lm.level == "INFO"
    #         assert lm.console is False
    #         assert lm.file == log_file

    # def test_auto_creates_log_dir(self):
    #     with tempfile.TemporaryDirectory() as tmpdir:
    #         deep_path = os.path.join(tmpdir, "nested", "logs", "app.log")
    #         cfg = LoggerFileAppenderConfig(file=deep_path)
    #         lm = LoggerManager(log_file_config=cfg)

    #         # Trigger logging to ensure handler wrote to file
    #         from loguru import logger
    #         logger.bind(name="test").info("test")
    #         assert Path(deep_path).exists()

    def test_setup_logging_creates_manager(self):
        lm = setup_logging(level="WARNING", console=False)
        assert isinstance(lm, LoggerManager)
        assert lm.level == "WARNING"

    def test_setup_logging_flask_sets_flask_loggers(self):
        lm = setup_logging_flask(level="INFO")
        assert "werkzeug" in lm.extra_loggers
        assert "flask.app" in lm.extra_loggers
        assert lm.extra_loggers["werkzeug"] == "INFO"
        assert lm.extra_loggers["flask.app"] == "INFO"

    # @pytest.mark.parametrize("name", FLASK_LOGGERS)
    # def test_flask_loggers_no_propagate(self, name):
    #     lm = setup_logging_flask(extra_loggers={name: "DEBUG"})
    #     log = logging.getLogger(name)
    #     assert log.handlers == [InterceptHandler()]
    #     assert log.propagate is False

    # def test_invalid_log_level_raises(self):
    #     with pytest.raises(ValueError, match="Invalid log level"):
    #         LoggerManager(level="TRACE")

    def test_empty_extra_logger_level_raises(self):
        with pytest.raises(ValueError, match="Empty log level"):
            LoggerManager(extra_loggers={"x": ""})

    def test_none_extra_logger_level_raises(self):
        with pytest.raises(ValueError, match="Empty log level"):
            LoggerManager(extra_loggers={"x": None})


# class TestRegression_Idempotency:
#     """Tests for regressions: double-intercept, handler accumulation."""

#     def test_no_duplicate_logs_on_reinit(self):
#         """Calling setup_logging() twice does NOT duplicate log messages — and each log appears exactly once."""
#         with tempfile.TemporaryDirectory() as tmpdir:
#             log_file = os.path.join(tmpdir, "app.log")

#             # 1️⃣ First init → log → file has 1 line
#             setup_logging(level="INFO", console=False, file=log_file)
#             from loguru import logger
#             logger.info("first init message")  # → written to file

#             with open(log_file) as f:
#                 lines1 = f.read().strip().splitlines()
#             assert len(lines1) == 1 and "first init message" in lines1[0]

#             # 2️⃣ Reinit → logger.remove() removes old file handler, but file content persists
#             #    Then new file handler added → new logs append to same file
#             setup_logging(level="INFO", console=False, file=log_file)
#             logger.info("second init message")  # → appends to same file

#             with open(log_file) as f:
#                 lines2 = f.read().strip().splitlines()

#             # Both logs present, no duplicates
#             assert len(lines2) == 2
#             assert "first init message" in lines2[0]
#             assert "second init message" in lines2[1]

#             # Crucially: NO line contains both messages → no duplication
#             for line in lines2:
#                 assert "first init message" not in line or "second init message" not in line

#     def test_no_handler_accumulation(self):
#         """Multiple setup_logging() calls do NOT pile up InterceptHandlers."""
#         setup_logging(console=False)
#         setup_logging(console=False)
#         setup_logging(console=False)

#         intercept_count = sum(1 for h in logging.root.handlers if isinstance(h, InterceptHandler))
#         assert intercept_count == 1


# Путь к файлу, который будет использоваться во всех тестах
TEST_FILE_PATH = "./tests/app.log"


@pytest.fixture(autouse=True)
def shared_log_file():
    # --- SETUP: Выполняется ТУТ перед началом тестов ---
    # Создаем пустой файл (или очищаем, если он существовал)
    with open(TEST_FILE_PATH, "w") as f:
        pass

    # Передаем управление тестам
    yield TEST_FILE_PATH

    # --- TEARDOWN: Выполняется ТУТ после завершения всех тестов ---
    if os.path.exists(TEST_FILE_PATH):
        os.remove(TEST_FILE_PATH)


# def test_root_level_filters_logs(shared_log_file):

#     log_file: str
#     content: str

#     # with tempfile.TemporaryDirectory() as tmpdir:
#     #     log_file = os.path.join(tmpdir, "app2.log")
#     #     lm = LoggerManager(level="INFO", console=False, log_file_config=LoggerFileAppenderConfig(file=log_file))

#     #     from loguru import logger
#     #     logger.bind(name="app2").info("info log")
#     #     logger.bind(name="app2").debug("debug log")  # should be filtered (DEBUG < INFO)

#     # log_file = "./tests/app2.log"
#     log_file = shared_log_file
#     lm = LoggerManager(level="INFO", console=False, log_file_config=LoggerFileAppenderConfig(file=log_file))

#     from loguru import logger
#     logger.bind(name="app").info("info log")
#     logger.bind(name="app").debug("debug log")  # should be filtered (DEBUG < INFO)

#     with open(log_file) as f:
#         content = f.read()

#     assert "info log" in content
#     assert "debug log" not in content


# class TestLevelFiltering:
#     """Test per-logger level overrides — with verified actual behavior."""


#     def test_per_logger_override_allows_lower_level(self):
#         with tempfile.TemporaryDirectory() as tmpdir:
#             log_file = os.path.join(tmpdir, "app.log")
#             lm = LoggerManager(
#                 level="INFO",
#                 console=False,
#                 log_file_config=LoggerFileAppenderConfig(file=log_file),
#                 extra_loggers={"mylib": "DEBUG"}
#             )

#             from loguru import logger
#             logger.bind(name="mylib").debug("debug from mylib")  # DEBUG ≥ DEBUG → ✅
#             logger.bind(name="app").debug("debug from app")     # DEBUG < INFO → ❌ filtered

#             with open(log_file) as f:
#                 content = f.read()

#             assert "debug from mylib" in content
#             assert "debug from app" not in content

#     def test_nested_logger_inherits_parent_override(self):
#         """`werkzeug.debug` inherits `werkzeug`'s override (longest prefix match)."""
#         with tempfile.TemporaryDirectory() as tmpdir:
#             log_file = os.path.join(tmpdir, "app.log")
#             lm = LoggerManager(
#                 level="INFO",
#                 console=False,
#                 log_file_config=LoggerFileAppenderConfig(file=log_file),
#                 extra_loggers={"werkzeug": "DEBUG"}
#             )

#             from loguru import logger
#             logger.bind(name="werkzeug.debug").debug("debug in werkzeug.debug")  # ✅ passes

#             with open(log_file) as f:
#                 content = f.read()

#             assert "debug in werkzeug.debug" in content

#     def test_standard_logging_interception_respects_extra_loggers_level(self):
#         """Standard logging logs respect `extra_loggers`, NOT logger.setLevel()."""
#         with tempfile.TemporaryDirectory() as tmpdir:
#             log_file = os.path.join(tmpdir, "app.log")
#             lm = LoggerManager(
#                 level="INFO",
#                 console=False,
#                 log_file_config=LoggerFileAppenderConfig(file=log_file),
#                 extra_loggers={"werkzeug": "DEBUG"}  # ← only this matters
#             )

#             # Set werkzeug's Python logging level to HIGH — but it's IGNORED by loguru
#             werkzeug = logging.getLogger("werkzeug")
#             werkzeug.setLevel(logging.CRITICAL)  # this has NO EFFECT

#             # Intercepts werkzeug at DEBUG level (because extra_loggers says so)
#             werkzeug.debug("debug intercept")  # → ✅ passes (DEBUG ≥ DEBUG)
#             werkzeug.critical("critical intercept")  # → ✅ also passes

#             with open(log_file) as f:
#                 content = f.read()

#             assert "debug intercept" in content
#             assert "critical intercept" in content

#     def test_no_extra_logger_uses_root_level(self):
#         """If logger not in extra_loggers, root level applies (standard logging logs)."""
#         with tempfile.TemporaryDirectory() as tmpdir:
#             log_file = os.path.join(tmpdir, "other.log")
#             lm = LoggerManager(level="INFO", console=False, log_file_config=LoggerFileAppenderConfig(file=log_file))
#             # No extra_loggers → werkzeug will use root=INFO

#             werkzeug = logging.getLogger("werkzeug.other")
#             werkzeug.setLevel(logging.DEBUG)  # ignored by loguru
#             werkzeug.debug("debug")  # ❌ filtered (DEBUG < INFO)
#             werkzeug.info("info")    # ✅ passes

#             with open(log_file) as f:
#                 content = f.read()

#             assert "debug" not in content
#             assert "info" in content

class TestFileAppender:
    """Test file-based logging edge cases."""

    def test_empty_file_path_skips_file(self):
        """No file sink when `file=""`."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = ""
            lm = setup_logging(level="INFO", console=False, file=log_file)
            assert lm.file is None

    def test_whitespace_file_path_skips_file(self):
        """Whitespace paths are treated as empty."""
        lm = setup_logging(level="INFO", console=False, file="   ")
        assert lm.file is None

    def test_invalid_compression_fails_later(self):
        """Non-allowed compression formats cause failure at handler add."""
        with pytest.raises(Exception):  # loguru raises on invalid compression
            LoggerManager(
                console=False,
                log_file_config=LoggerFileAppenderConfig(
                    file="/dev/null", compression="invalid"
                )
            )
