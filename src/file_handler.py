import json
import os
import shutil
import time
from typing import Dict

from custom_error import *
from logger import Logger
from file import File
from config import Config


class FileHandler(File):
    def __init__(self, logger: Logger, file_path: str, config: Dict[str, str]):

        self.logger = logger
        self.file_path = file_path
        self.file_name = self._get_file_name()
        self.config = config

        self.metadata = self._get_file_metadata()
        self.team_name = self._get_teamName()
        self.azure_project_name = self.get_azureProjectName()
        self.azure_project_organization = self.get_azureProjectOrganization()

    def _get_file_metadata(self) -> Dict[str, str]:
        try:
            team_name = self._get_file_name().split('_')[1]
            file_metadata = Config.get_teamInfo(team_name)

            return file_metadata
        except Exception as error:
            raise FileMetadataError(f'Failed to get file metadata: {error}')

    def _get_file_name(self) -> str:
        return os.path.basename(self.file_path).split('.')[0]

    def _get_teamName(self) -> str:
        try:
            return self.metadata['TeamName']

        except Exception as error:
            raise FileMetadataNotFound(f'required metadata not found: {error}')

    def get_azureProjectName(self) -> str:
        try:
            return self.metadata['AzureProjectName']

        except Exception as error:
            raise FileMetadataNotFound(f'required metadata not found: {error}')

    def get_azureProjectOrganization(self) -> str:
        try:
            return self.metadata['AzureProjectOrganization']
        except Exception as error:
            raise FileMetadataNotFound(f'required metadata not found: {error}')

    def get_dest_path(self) -> str:
        return f'./Yesodot/{self.team_name}/{self.azure_project_name}/Images/{self.file_name}'

    def _check_file_moved(self) -> bool:
        if(os.path.isfile(self.get_dest_path())):
            self.logger.info(f'File moved successfully to {self.file_path}')
            return True
        else:
            raise MoveFileError(f'File failed to move to {self.file_path}')

    def move_file(self, dest_path: str):
        shutil.move(self.file_path, dest_path)
        time.sleep(0.1)
        self._check_file_moved()
        self.file_path = self.get_dest_path()
