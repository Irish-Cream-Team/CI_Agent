from file import File
from os import DirEntry, scandir
from time import sleep
from typing import List


class FolderLisenenr:

    def __init__(self, path: str):
        self.path = path
        self.files: List[File] = FolderLisenenr.get_folder_files(self.path)

    def listen(self) -> List[File]:
        while True:
            sleep(0.1)
            new_files = FolderLisenenr.get_folder_files(self.path)
            if (len(self.files) == 0):
                self.files = new_files
            else:
                done_new_files = self.get_done_new_files(self.files, new_files)
                if done_new_files:
                    return done_new_files
                self.files = new_files

    @staticmethod
    def get_done_new_files(old_files: List[File], new_files: List[File]) -> List[File]:
        done_files = []
        for new_file in new_files:
            old_file = FolderLisenenr.get_file_by_name(
                old_files, new_file.get_name())

            if not old_file:
                continue

            elif(File.is_done_updated(old_file, new_file)):
                done_files.append(new_file)
        return done_files

    def convert_to_file_object(self, files: List[DirEntry]) -> List[File]:
        filesObj = []
        for file in files:
            if(file.is_file()):
                filesObj.append(File.from_dir_entry(file))
        return filesObj

    @ staticmethod
    def get_folder_files(path) -> List[File]:
        files = []
        for dir_entry in scandir(path):
            if(dir_entry.is_file()):
                files.append(File.from_dir_entry(dir_entry))
        return files

    @ staticmethod
    def get_file_by_name(files: List[File], name: str) -> File:
        for file in files:
            if(file.get_name() == name):
                return file
        return None
