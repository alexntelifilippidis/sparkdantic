Logger Module
=============

.. automodule:: sparkdantic.logger
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:


Colored Logging System
----------------------

SparkDantic includes a sophisticated logging system with colored output and emoji indicators for different log levels.

ColoredFormatter
~~~~~~~~~~~~~~~~

The ``ColoredFormatter`` class provides visually appealing log output with:

- 🔍 **DEBUG**: Cyan colored debug information
- ✨ **INFO**: Green colored informational messages
- ⚠️ **WARNING**: Yellow colored warnings
- ❌ **ERROR**: Red colored error messages
- 🚨 **CRITICAL**: Magenta colored critical errors

SparkModelLogger
~~~~~~~~~~~~~~~~

The ``SparkModelLogger`` class manages logger instances across your application using a singleton pattern.

Default Log Level
^^^^^^^^^^^^^^^^^

The logging level is set to ``INFO`` by default. You can change this by setting the ``LOG_LEVEL``
environment variable to a different level such as ``DEBUG``, ``WARNING``, or ``ERROR``.

**Usage Example:**

.. code-block:: python

   from sparkdantic.logger import SparkModelLogger
   import os

   #Set up log level
   os.environ["LOGLEVEL"] = "INFO"

   # Get a logger instance
   logger = SparkModelLogger.get_logger("MyModule")

   # Use with colored output
   logger.info("Processing data...")
   logger.warning("Low memory warning")
   logger.error("Failed to process record")

**Log Format:**

Each log message includes:

- Timestamp in white
- Logger name in bold blue
- Log level with emoji and color
- Message content in level-specific color

Example output::

   2025-01-01 12:30:45 - MyModule - ✨ INFO - Processing completed successfully
