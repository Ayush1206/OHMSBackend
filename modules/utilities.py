#!/usr/bin/python3

"""
This module sets up logging for the application, enabling logging to both the console and an optional log file.

The logging configuration can be customized based on whether logging to a file is needed.
By default, logs are sent to the console, but you can enable file logging by passing `log_to_file=True`.

Additionally, the `Colours` class is provided to facilitate colored terminal output for different types of messages, such as headers, warnings, or errors.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

# Create a directory for logs if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")


def setup_logging(
    log_file="app.log",
    log_level=logging.INFO,
    log_to_file=True,
    max_bytes=1_000_000,
    backup_count=5,
):
    """
    Set up logging for the application.

    :param log_file: The name of the log file.
    :param log_level: The logging level (e.g., logging.DEBUG, logging.INFO).
    :param log_to_file: Boolean flag to enable or disable file logging.
    :param max_bytes: The maximum size of the log file before rotating.
    :param backup_count: The number of backup log files to keep.
    :return: A logger instance.
    """
    logger = logging.getLogger("app_logger")
    logger.setLevel(log_level)

    if log_to_file:
        # Create a rotating file handler
        file_handler = RotatingFileHandler(
            os.path.join("logs", log_file), maxBytes=max_bytes, backupCount=backup_count
        )
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(file_handler)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(console_handler)

    return logger


# Example usage
logger = setup_logging()

# Example of logging messages
logger.info("Logging system initialized")
logger.warning("This is a warning message")
logger.error("This is an error message")


class Colours:
    """
    A utility class for ANSI escape sequences to format text with colors and styles in the terminal.
    """

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKRED = "\033[91m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"  # Resets color to default
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def log_with_color(level, message, color):
    """
    Log a message with a specified color.

    :param level: The logging level (e.g., logging.INFO, logging.WARNING).
    :param message: The message to log.
    :param color: The color code from the Colours class.
    """
    log_message = f"{color}{message}{Colours.ENDC}"
    logger.log(level, log_message)
