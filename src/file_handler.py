import json
import os
import shutil
import time
from typing import Dict

from api import API
from config import Config
from custom_error import *
from log import Logger


class FileHandler:
    def __init__(self, logger: Logger, file_path: str, config: Config):
        self.logger = logger
        self.file_path = file_path
        self.metadata = self.get_file_metadata()
        self.team_name = self.get_teamName()
        self.azure_project_name = self.get_azureProjectName()
        self.azure_project_organization = self.get_azureProjectOrganization()
        self.file_name = self.get_file_name()
        self.config = config

    def get_file_metadata(self) -> Dict[str, str]:
        try:
            file_metadata = os.getxattr(
                self.file_path, 'user.info').decode("utf-8")
            return json.loads(file_metadata)
        except Exception as error:
            raise FileMetadataError(f'Failed to get file metadata: {error}')

    def get_file_name(self) -> str:
        return os.path.basename(self.file_path)

    def get_teamName(self) -> str:
        return self.metadata['teamName']

    def get_azureProjectName(self) -> str:
        return self.metadata['azureProjectName']

    def get_azureProjectOrganization(self) -> str:
        return self.metadata['AzureProjectOrganization']

    def get_dest_path(self) -> str:
        return f'./Yesodot/{self.team_name}/{self.azure_project_name}/Images/{self.file_name}'

    def check_file_moved(self) -> bool:
        if(os.path.isfile(self.get_dest_path())):
            self.logger.info(f'File moved successfully to {self.file_path}')
            return True
        else:
            raise MoveFileError(f'File failed to move to {self.file_path}')

    def move_file(self):
        shutil.move(self.file_path, self.get_dest_path())
        time.sleep(0.1)
        self.check_file_moved()
        self.file_path = self.get_dest_path()

    def file_handler_main(self):
        self.logger.info(
            f'new file {self.file_path} detected, start file handler process')

        self.move_file()
        self.logger.info('file handler process finished')
        api = API(self.azure_project_organization,
                  self.azure_project_name, self.config, self.logger)
        api.run_ci_pipline()
