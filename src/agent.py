import os
import time

from folder_listener import start_listener
from log import config_logger


def create_folder(folder_path: str):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        time.sleep(0.1)


def main():
    logger = config_logger()
    logger.info('agent is runnig')

    folder_to_listen = './Yesodot/Unorganize'
    create_folder(folder_to_listen)
    start_listener(folder_to_listen)


if __name__ == "__main__":
    main()
