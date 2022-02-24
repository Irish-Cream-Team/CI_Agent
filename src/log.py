import logging
import pathlib
import sys

def config_logger():
    pathlib.Path('./logs').mkdir(parents=True, exist_ok=True)

    FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

    logging.basicConfig( handlers=[
        logging.FileHandler("./logs/try.log",mode='a'),
        logging.StreamHandler()],
        format=FORMAT, level=logging.INFO)
    return logging.getLogger()
