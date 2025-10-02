import logging
import os
import sys
from datetime import datetime
from typing import Dict
from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class AnsiStyle:
    black: str = "\033[30m"
    red: str = "\033[31m"
    green: str = "\033[32m"
    yellow: str = "\033[33m"
    blue: str = "\033[34m"
    magenta: str = "\033[35m"
    cyan: str = "\033[36m"
    white: str = "\033[37m"
    reset: str = "\033[0m"
    bright: str = "\033[1m"

ansi_style = AnsiStyle()

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

@dataclass(frozen=True)
class LogLevelConfig:
    color: str
    emoji: str
    color_name: str

LOG_LEVEL_CONFIGS: Dict[LogLevel, LogLevelConfig] = {
    LogLevel.DEBUG: LogLevelConfig(color=ansi_style.cyan, emoji="🔍", color_name="cyan"),
    LogLevel.INFO: LogLevelConfig(color=ansi_style.green, emoji="✨", color_name="green"),
    LogLevel.WARNING: LogLevelConfig(color=ansi_style.yellow, emoji="⚠️", color_name="yellow"),
    LogLevel.ERROR: LogLevelConfig(color=ansi_style.red, emoji="❌", color_name="red"),
    LogLevel.CRITICAL: LogLevelConfig(color=ansi_style.magenta, emoji="🚨", color_name="magenta"),
}

DEFAULT_CONFIG = LogLevelConfig(color=ansi_style.white, emoji="📝", color_name="white")

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors and emojis using ANSI codes and dataclass/enum config."""

    def format(self, record: logging.LogRecord) -> str:
        # Try to get config from enum, fallback to default
        try:
            level_enum = LogLevel[record.levelname]
            config = LOG_LEVEL_CONFIGS[level_enum]
        except (KeyError, ValueError):
            config = DEFAULT_CONFIG

        # Format timestamp with white color
        timestamp = f"{ansi_style.white}{datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')}{ansi_style.reset}"
        # Format logger name with blue color and bold
        logger_name = f"{ansi_style.blue}{ansi_style.bright}{record.name}{ansi_style.reset}"
        # Format level with specific color and emoji
        level_text = f"{config.color}{config.emoji} {record.levelname}{ansi_style.reset}"
        # Format message with level-specific color
        message = f"{config.color}{record.getMessage()}{ansi_style.reset}"
        # Combine all parts with dashes
        return f"{timestamp} - {logger_name} - {level_text} - {message}"

class SparkModelLogger:
    """Custom logger for SparkModel with colors and emojis.

    This class provides a singleton-like pattern for managing colored loggers
    across the SparkModel application. It ensures that each named logger
    is created only once and configured with the custom ColoredFormatter.

    :cvar _loggers: Cache of created logger instances
    :vartype _loggers: Dict[str, logging.Logger]
    """

    _loggers: Dict[str, logging.Logger] = {}

    @classmethod
    def get_logger(cls, name: str = "SparkModel") -> logging.Logger:
        """Get or create a colored logger instance.

        Creates a new logger with ColoredFormatter if it doesn't exist,
        or returns the existing logger for the given name.

        :param name: Name of the logger to create or retrieve
        :type name: str
        :return: Configured logger instance with colored formatting
        :rtype: logging.Logger

        . note::
           The logger is configured with DEBUG level and uses stdout for output.
           Propagation is disabled to prevent duplicate messages.

        . code-block:: python

           logger = SparkModelLogger.get_logger("MyModule")
           logger.info("This is a colored log message")
        """
        loglevel = os.getenv("LOGLEVEL", "INFO")
        if name not in cls._loggers:
            logger = logging.getLogger(name)
            logger.setLevel(getattr(logging, loglevel.upper(), logging.INFO))

            # Remove existing handlers to avoid duplicates
            logger.handlers.clear()

            # Create console handler
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(ColoredFormatter())

            logger.addHandler(handler)
            logger.propagate = False

            cls._loggers[name] = logger

        return cls._loggers[name]
