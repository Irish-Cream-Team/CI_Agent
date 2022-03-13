import os
import time 

from config import *
from custom_error import *
from folder_lisener import FolderLisenenr
from log import Logger
from api import API
from file_handler import FileHandler


class Agent:

    def __init__(self):
        
        """
        Initializes the Agent class.
        """
        self.logger: Logger
        self.config: Dict[str, str]
        self.teamInfo: Dict[str, str]
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
            lisener = FolderLisenenr(Config.get_input_folder(self.config))
            new_files = lisener.listen()
            if new_files:
                for file in new_files:
                    self.logger.info(
                        f'new file {file.get_name()} detected, start file handler process')
                    try:
                        new_file = FileHandler(
                            self.logger, file.get_path(), self.config)
                        new_file.move_file(new_file.get_dest_path())
                        self.logger.info('file handler process finished')

                        api = API(new_file.get_azureProjectOrganization(),
                                  new_file.get_azureProjectName(), self.config, self.logger)
                        api.run_ci_pipline()

                    except FileMetadataError as error:
                        self.logger.error(
                            f'{file.get_name()} has metadata error, file will be ignored')
                    except Exception as error:
                        self.logger.error(
                            f'{file.get_name()} has unknown error, file will be ignored {error}')
    @staticmethod
    def create_folder(folder_path: str):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            time.sleep(0.1)


if __name__ == "__main__":
    agent = Agent()
    agent.main()
