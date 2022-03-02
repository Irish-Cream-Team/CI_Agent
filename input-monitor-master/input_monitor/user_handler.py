import multiprocessing as mp
import threading
import time
import logging
import logging.handlers
from queue import Empty as QueueIsEmptyException
from input_monitor.folder_monitor import FolderMonitor
from input_monitor.common.profile import Profile
from typing import List


class UserMonitorProcess(mp.Process):

    _logger = logging.getLogger(__name__)

    def __init__(self, profile: Profile, termination_event: mp.Event, log_queue: mp.Queue):
        mp.Process.__init__(self)
        self._profile = profile
        self._termination_event = termination_event
        self._log_queue = log_queue

    def run(self) -> None:
        self._setup_logger()
        monitor_obj = FolderMonitor(self._profile.stream_input_folder)
        monitor_obj.start_monitor()

        UserMonitorProcess._logger.critical(f"start monitor folder: {self._profile.stream_input_folder}")

        while not self._termination_event.is_set():
            try:
                new_file = monitor_obj.files_queue.get()
            except QueueIsEmptyException:
                time.sleep(1)
                continue
            print(new_file)
        monitor_obj.stop_monitor()

    def _setup_logger(self):
        """setup logging - logger will add messages to a queue."""
        logger = logging.getLogger()
        logger.handlers = []
        logging_handler = logging.handlers.QueueHandler(self._log_queue)
        logger.addHandler(logging_handler)

    @property
    def profile(self) -> Profile:
        return self._profile


class UsersManager:

    _logger = logging.getLogger(__name__)

    def __init__(self):
        self._users_list: List[UserMonitorProcess] = []
        self._termination_event: mp.Event = mp.Event()
        self._log_queue: mp.Queue = mp.Queue()
        self._logging_thread = None

    def add_user(self, profile):
        """adds new UserMonitorProcess to the UsersManager process pool"""
        self._users_list.append(UserMonitorProcess(profile, self._termination_event, self._log_queue))

    def start_all(self):
        """start each UserMonitorProcess according to its profile"""
        if len(self._users_list) == 0:
            raise Exception("There are no users to start")
        self._logging_thread = threading.Thread(target=self._handle_logging, daemon=True)
        self._logging_thread.start()
        for user in self._users_list:
            UsersManager._logger.info(f"starting user {user.profile.name}")
            user.start()

    def stop_all_and_join(self) -> bool:
        """
        try to stop all process conventionally...
        :return: True is succeeded, else False
        """
        if self.is_alive:
            self._termination_event.set()
            for user in self._users_list:
                user.join(timeout=10)
            self._logging_thread.join()
        return not self.is_alive

    def kill_all(self):
        """kill processes with os.kill (unsafe)"""
        for user in self._users_list:
            if user.is_alive():
                user.kill()

    def _handle_logging(self):
        while not self._termination_event.is_set():
            try:
                record = self._log_queue.get(timeout=0.69)
                UsersManager._logger.handle(record)
            except Exception:
                pass

        # after stop flag, empty the queue
        while not self._log_queue.empty():
            try:
                record = self._log_queue.get(timeout=0.69)
                UsersManager._logger.handle(record)
            except Exception:
                pass

    @property
    def is_alive(self) -> bool:
        return any(user.is_alive() for user in self._users_list)
