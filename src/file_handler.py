import os
import shutil
import json
import time
from API import run_ci_pipline
from log import config_logger
logger = config_logger()


def get_file_metadata(file_path):
    file_metadata = os.getxattr(file_path, 'user.info').decode("utf-8")
    return json.loads(file_metadata)


def get_file_name(file_path):
    return os.path.basename(file_path)


def new_file_location(azureProjectName, teamName, fileName):
    return f'./Yesodot/{teamName}/{azureProjectName}/Images/{fileName}'


def move_file(src_file_path, dest_file_path):
    shutil.move(src_file_path, dest_file_path)
    time.sleep(0.1)
    if(os.path.isfile(dest_file_path)):
        logger.info(f'File moved successfully to {dest_file_path}')
    else:
        logger.critical(f'File failed to move to {dest_file_path}')


def file_handler_main(event):
    logger.info('new file detected, start file handler process')
    
    fileMetadata = get_file_metadata(event.src_path)

    azureProjectName = fileMetadata.get('AzureProjectName')
    azureProjectOrganization = fileMetadata.get('AzureProjectOrganization')
    teamName = fileMetadata.get('TeamName')

    fileName = get_file_name(event.src_path)
    newFileLocation = new_file_location(azureProjectName, teamName, fileName)

    move_file(event.src_path, newFileLocation)
    logger.info('file handler process finished')
    run_ci_pipline(azureProjectOrganization, azureProjectName)
