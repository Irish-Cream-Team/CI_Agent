import time
import queue
import os
import threading
from typing import Set
from dataclasses import dataclass, field
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from watchdog.utils.dirsnapshot import DirectorySnapshot


class FolderMonitor:

    @dataclass(repr=False, eq=False)
    class OverlappedFilesHandler:
        """
        The purpose of this class is to handles files that were monitored before taking folder
        snapshot (prevents file duplication in the queue)
        """
        check_for_overlap: bool = True  # check if file already captured in the snapshot
        overlapped_files: Set[str] = field(
            default_factory=set)  # set contain files that were monitored before taking folder snapshot

    def __init__(self, folder_path: str):
        self._folder_path = folder_path
        self._is_monitoring: bool = False
        self.files_queue = queue.Queue()  # contain all files that are already exist in folder and files moved into it
        self._overlap_handler = self.OverlappedFilesHandler()
        self._thread_locker: threading.Lock = threading.Lock()
        self._folder_observer = None  # watchdog observer object
        self._initialize_folder_observer()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._is_monitoring:
            self.stop_monitor()

    def _initialize_folder_observer(self):
        """initialize the observer object with the needed event handlers"""
        event_handler = PatternMatchingEventHandler(case_sensitive=True)
        event_handler.on_moved = self._handle_new_file
        self._folder_observer = Observer()
        self._folder_observer.schedule(event_handler, self._folder_path, recursive=True)

    def start_monitor(self):
        """start monitor the target folder. the function monitor both new files and existing files"""
        self._is_monitoring = True
        self._folder_observer.start()  # start handle new files moved into the folder
        self._handle_existing_files()  # start handle files that were already exist in the folder

    def _handle_existing_files(self):
        """take folder snapshot and enqueue the existing files in the folder."""
        folder_snapshot = DirectorySnapshot(path=self._folder_path)
        cur_paths = folder_snapshot.paths
        with self._thread_locker:
            self._overlap_handler.check_for_overlap = False
            cur_paths.difference_update(self._overlap_handler.overlapped_files)
            self._overlap_handler.overlapped_files.clear()

        for entry in cur_paths:
            if os.path.isfile(entry):
                self.files_queue.put(entry)

    def _handle_new_file(self, event):
        """enqueue new file in the folder"""
        path = event.dest_path
        if os.path.isfile(path):
            if self._overlap_handler.check_for_overlap:
                self._overlap_handler.overlapped_files.add(path)
            self.files_queue.put(path)

    def stop_monitor(self):
        """stop current monitoring immediately"""
        if not self._is_monitoring:
            raise Exception("No monitoring was preformed")
        self._folder_observer.stop()
        self._folder_observer.join()
        self._is_monitoring = False

    @property
    def is_monitoring(self) -> bool:
        return self._is_monitoring

    @property
    def folder_path(self) -> str:
        return self._folder_path


def main():
    with FolderMonitor(folder_path=r"D:\python_projects\watchdog\test_folder") as fm:
        x = fm.OverlappedFilesHandler()
        from sys import getsizeof
        print(getsizeof(x))


if __name__ == '__main__':
    main()
