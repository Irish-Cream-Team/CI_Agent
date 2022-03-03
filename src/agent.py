import os
import time

from api import API
from config import *
from custom_error import *
from file_handler import FileHandler
from folder_lisener import FolderLisenenr
from log import Logger

"""
todo:
    # - static config,
    # - private functions,
    - add file lisenenr
    
"""


class Agent:

    def __init__(self):
        """
        Initializes the Agent class.
        """
        self.logger: Logger
        self.config: Dict[str, str]
        self.setup_Agent()

        self.logger.info('Agent started')

    def setup_Agent(self):
        """
        Sets up the Agent class.
        """
        try:
            self.logger = Logger()
            self.logger.info('Setting up Agent')
            self.config = Config.get_config()

        except Exception as error:
            self.logger.critical(f'Error: {error}')
            self.logger.critical(
                'Agent failed to setup. This is critical error, exiting program')
            exit(1)

        self.logger.info('Agent setup complete')

    def main(self):
        is_running = True
        while is_running:
            files = FolderLisenenr.listen(self.config['path'])
            for file in files:
                folder_files = FolderLisenenr.get_folder_files(
                    self.config['path'])
                if (not file.is_updated(FolderLisenenr.find_file_by_name(file.get_name(), folder_files))):
                    new_file_ob = file

            self.logger.info(
                f'new file {new_file_ob.get_name()} detected, start file handler process')

            new_file = FileHandler(
                self.logger, new_file_ob.get_path(), self.config)
            new_file.move_file(new_file.get_dest_path())
            self.logger.info('file handler process finished')

            api = API(new_file.get_azureProjectOrganization(),
                      new_file.get_azureProjectName(), self.config, self.logger)
            api.run_ci_pipline()

    @staticmethod
    def create_folder(folder_path: str):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            time.sleep(0.1)


if __name__ == "__main__":
    agent = Agent()
    agent.main()
