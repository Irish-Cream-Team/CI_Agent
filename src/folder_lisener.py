from file import File
import os
from typing import List


class FolderLisenenr:

    @staticmethod
    def listen(path: str) -> List[File]:
        files = []
        for dir_entry in os.scandir(path):
            if(dir_entry.is_file()):
                files.append(File.from_dir_entry(dir_entry))
        if (FolderLisenenr.is_updated(path, files)):
            new_files = FolderLisenenr.find_new_files(path, files)
        return new_files

    @staticmethod
    def is_updated(path: str, files: List[File]):
        for dir_entry in os.scandir(path):
            if(dir_entry.is_file()):
                for file in files:
                    if(file.is_updated(dir_entry)):
                        return True
        return False

    @staticmethod
    def get_folder_files(path: str) -> List[File]:
        files = []
        for dir_entry in os.scandir(path):
            if(dir_entry.is_file()):
                files.append(File.from_dir_entry(dir_entry))
        return files

    @staticmethod
    def find_file_by_name(name: str, files: List[File]) -> File:
        for file in files:
            if(file.get_name() == name):
                return file
        return None
