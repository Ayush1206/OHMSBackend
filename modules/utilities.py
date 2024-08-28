"""
Module for setting up logging utilities.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

# Create a directory for logs if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")


def setup_logging(log_file="app.log", log_level=logging.INFO, max_bytes=1_000_000, backup_count=5):
    """
    Set up logging for the application.

    :param log_file: The name of the log file.
    :param log_level: The logging level (e.g., logging.DEBUG, logging.INFO).
    :param max_bytes: The maximum size of the log file before rotating.
    :param backup_count: The number of backup log files to keep.
    :return: A logger instance.
    """
    logger = logging.getLogger("app_logger")
    logger.setLevel(log_level)

    # Create a rotating file handler
    file_handler = RotatingFileHandler(
        os.path.join("logs", log_file), maxBytes=max_bytes, backupCount=backup_count
    )

    # Create a console handler
    console_handler = logging.StreamHandler()

    # Set logging format
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Example usage
logger = setup_logging()

# Example of logging messages
logger.info("Logging system initialized")
logger.warning("This is a warning message")
logger.error("This is an error message")
