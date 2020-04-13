"""
Customization for logging module output and creation of separate logger for each module that will import this
"""
import logging
import sys
from logging.handlers import TimedRotatingFileHandler

FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE = "my_app.log"


def get_console_handler():
    """Creation of a Logging Stream Handler and set of a formatter for it"""
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    """Creation of a Logging File Handler and set of a formatter for it"""
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    """
    Method that returns the logger with a Stream Handler configured to display log records in a specific format
    :param logger_name:
    :return: the custom logger
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.propagate = False
    return logger
