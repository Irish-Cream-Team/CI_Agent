import json
import os
import shutil
import time
from typing import Dict

from API import run_ci_pipline
from log import config_logger

logger = config_logger()


def get_file_metadata(file_path: str) -> Dict[str, str]:
    file_metadata = os.getxattr(file_path, 'user.info').decode("utf-8")
    return json.loads(file_metadata)


def get_file_name(file_path: str) -> str:
    return os.path.basename(file_path)


def get_new_file_location(azureProjectName: str, teamName: str, fileName: str) -> str:
    return f'./Yesodot/{teamName}/{azureProjectName}/Images/{fileName}'


def move_file(src_file_path: str, dest_file_path: str):
    shutil.move(src_file_path, dest_file_path)
    time.sleep(0.1)
    if(os.path.isfile(dest_file_path)):
        logger.info(f'File moved successfully to {dest_file_path}')
    else:
        logger.critical(f'File failed to move to {dest_file_path}')


def file_handler_main(event):
    logger.info(
        f'new file {event.src_path} detected, start file handler process')

    try:
        file_metadata = get_file_metadata(event.src_path)

        azure_project_name = file_metadata.get('AzureProjectName')
        azure_project_organization = file_metadata.get(
            'AzureProjectOrganization')
        team_name = file_metadata.get('TeamName')
    except Exception as e:
        logger.critical(f'Failed to get file metadata: {e}')
        logger.critical(f'Exit file_handler process')
        return

    file_name = get_file_name(event.src_path)
    new_file_location = get_new_file_location(
        azure_project_name, team_name, file_name)

    move_file(event.src_path, new_file_location)
    logger.info('file handler process finished')
    run_ci_pipline(azure_project_organization, azure_project_name)
    return
