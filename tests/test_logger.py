import logging
from src.logger import SparkModelLogger, ColoredFormatter


def test_logger_outputs_colored_messages():
    logger = SparkModelLogger.get_logger("TestLogger")
    assert logger.name == "TestLogger"
    assert isinstance(logger.handlers[0].formatter, ColoredFormatter)


def test_logger_reuses_existing_instance():
    logger1 = SparkModelLogger.get_logger("SharedLogger")
    logger2 = SparkModelLogger.get_logger("SharedLogger")
    assert logger1 is logger2


def test_logger_creates_new_instance_for_different_name():
    logger1 = SparkModelLogger.get_logger("LoggerOne")
    logger2 = SparkModelLogger.get_logger("LoggerTwo")
    assert logger1 is not logger2


def test_formatter_applies_correct_colors_and_emojis():
    formatter = ColoredFormatter()
    record = logging.LogRecord(
        name="TestLogger",
        level=logging.INFO,
        pathname="test_path",
        lineno=10,
        msg="This is a test message",
        args=None,
        exc_info=None,
    )
    formatted_message = formatter.format(record)
    assert "✨ INFO" in formatted_message
    assert "This is a test message" in formatted_message


def test_formatter_handles_unknown_log_level():
    formatter = ColoredFormatter()
    record = logging.LogRecord(
        name="TestLogger",
        level=99,  # Unknown log level
        pathname="test_path",
        lineno=10,
        msg="Unknown level message",
        args=None,
        exc_info=None,
    )
    formatted_message = formatter.format(record)
    assert "📝" in formatted_message
    assert "Unknown level message" in formatted_message
