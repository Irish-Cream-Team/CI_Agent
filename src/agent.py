import os
import time

from config import Config
from custom_error import *
from folder_lisener import start_lisener
from log import Logger


class Agent:

    def __init__(self):
        """
        Initializes the Agent class.
        """
        self.logger: Logger
        self.config: Config
        self.setup_Agent()

        self.logger.info('Agent started')
        start_lisener(self.config.get_input_folder(), self.logger, self.config)

    def setup_Agent(self):
        """
        Sets up the Agent class.
        """
        try:
            self.logger = Logger()
            self.logger.info('Setting up Agent')
            self.config = Config()

        except MissingConfigurationError as error:
            self.logger.throw_critical_error(error)
            self.logger.critical(
                'Agent failed to setup. This is critical error, exiting program')
            exit(1)

        self.logger.info('Agent setup complete')

    @staticmethod
    def create_folder(folder_path: str):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            time.sleep(0.1)


if __name__ == "__main__":
    agent = Agent()
