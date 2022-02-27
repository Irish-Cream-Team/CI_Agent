
# import the modules
import time

from watchdog.events import RegexMatchingEventHandler
from watchdog.observers import Observer


class FolderLisenenr:

    def __init__(self) -> None:
        self.event = None

    def create_event_handler(self):
        # create the event handler
        ignore_directories = False
        case_sensitive = True
        my_event_handler = RegexMatchingEventHandler(ignore_directories=ignore_directories,
                                                     case_sensitive=case_sensitive)
        return my_event_handlerit

    def start_lisener(self, path: str) -> str:
        event_handler = self.create_event_handler()
        event_handler.on_created = self.on_create
        if self.event is not None:
            return self.event
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)

        # Start the observer
        observer.start()
        try:
            while True:
                # Set the thread sleep time
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    def on_create(self, event):
        self.event = event
