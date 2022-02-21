import logging
from agent import create_folder


def config_logger():
    create_folder('./logs')
    FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

    logging.basicConfig(filename=f'./logs/try.log', format=FORMAT)
    return logging.getLogger()
