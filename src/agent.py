import os
from folder_listener import start_listener
import time

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        time.sleep(0.1)


def main():
    folderToListen = "./Yesodot/Unorganize"
    create_folder(folderToListen)
    start_listener(folderToListen)


if __name__ == "__main__":
    main()
