import json
import logging
from typing import Dict
from input_monitor.common.profile import Profile
from input_monitor.user_handler import UsersManager


class InputMonitor:

    _logger = logging.getLogger(__name__)

    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            config = json.load(f)

        InputMonitor._logger.info("Creating InputMonitor instance")

        self._profiles: Dict[str, Profile] = {p.name: p for p in Profile.make(config)}
        self._users_manager = UsersManager()

        InputMonitor._logger.info('Successfully set up InputMonitor instance.')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._users_manager.is_alive:
            self._users_manager.kill_all()

    def start_monitor(self):
        """Start the folder monitoring for each profile"""
        InputMonitor._logger.info("Start monitoring")
        for profile in self._profiles.values():
            self._users_manager.add_user(profile)
        self._users_manager.start_all()
        InputMonitor._logger.info("Successfully started monitoring")

    def stop_monitor(self):
        """stop all monitor processes"""
        if not self._users_manager.is_alive:
            raise Exception("No monitoring is currently preformed")

        InputMonitor._logger.info("attempt to stop monitoring")
        is_succeeded = self._users_manager.stop_all_and_join()
        if not is_succeeded:
            InputMonitor._logger.warning("timeout reached killing processes")
            self._users_manager.kill_all()
        else:
            InputMonitor._logger.info("monitoring stopped successfully")
