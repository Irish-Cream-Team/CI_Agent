import logging
import pathlib
from typing import Type


class Logger:
    def __init__(self, log_file: str = '/logs/log.log') -> None:
        """
        Initializes the logger class.
        :param log_file: Log file path.
        """
        self.logger = logging.getLogger('logger')
        self.logger.setLevel(logging.INFO)
        FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
        DATE_FORMAT = '%d-%m-%Y %H:%M:%S'
        formatter = logging.Formatter(FORMAT, DATE_FORMAT)
        handler = logging.FileHandler(str(pathlib.Path.cwd()) + log_file)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.info('Logger initialized')

    def debug(self, message: str) -> None:
        """
        Logs a debug message.
        :param message: Message to log.
        """
        self.logger.debug(message)

    def warning(self, message: str) -> None:
        """
        Logs a warning message.
        :param message: Message to log.
        """
        self.logger.warning(message)

    def info(self, message: str) -> None:
        """
        Logs an info message.
        :param message: Message to log.
        """
        self.logger.info(message)

    def error(self, message: str):
        """
        Logs an error message.
        :param message: Message to log.
        """
        self.logger.error(message)

    def critical(self, message: str) -> None:
        """
        Logs a critical message.
        :param message: Message to log."""
        self.logger.critical(message)

