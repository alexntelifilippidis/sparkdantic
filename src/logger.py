import logging
import sys
from datetime import datetime
from typing import Dict
from colorama import init, Fore, Style

# Initialize colorama for cross-platform color support
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors and emojis using colorama.

    This formatter adds colored output and emoji icons to log messages
    for better visual distinction between different log levels.

    :ivar LEVEL_CONFIG: Configuration mapping for log levels including colors and emojis
    :vartype LEVEL_CONFIG: Dict[str, Dict[str, str]]
    """

    # Level-specific colors and emojis
    LEVEL_CONFIG: Dict[str, Dict[str, str]] = {
        "DEBUG": {"color": Fore.CYAN, "emoji": "🔍"},
        "INFO": {"color": Fore.GREEN, "emoji": "✨"},
        "WARNING": {"color": Fore.YELLOW, "emoji": "⚠️"},
        "ERROR": {"color": Fore.RED, "emoji": "❌"},
        "CRITICAL": {"color": Fore.MAGENTA, "emoji": "🚨"},
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record with colors and emojis.

        :param record: The log record to format
        :type record: logging.LogRecord
        :return: Formatted log message string with colors and emojis
        :rtype: str
        """
        # Get level configuration
        level_config = self.LEVEL_CONFIG.get(
            record.levelname, {"color": Fore.WHITE, "emoji": "📝"}
        )

        # Format timestamp with white color
        timestamp = f"{Fore.WHITE}{datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')}"

        # Format logger name with blue color and bold
        logger_name = f"{Fore.BLUE}{Style.BRIGHT}{record.name}"

        # Format level with specific color and emoji
        level_color = level_config["color"]
        level_text = f"{level_color}{level_config['emoji']} {record.levelname}"

        # Format message with level-specific color
        message = f"{level_color}{record.getMessage()}"

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
        if name not in cls._loggers:
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)

            # Remove existing handlers to avoid duplicates
            logger.handlers.clear()

            # Create console handler
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(ColoredFormatter())

            logger.addHandler(handler)
            logger.propagate = False

            cls._loggers[name] = logger

        return cls._loggers[name]
