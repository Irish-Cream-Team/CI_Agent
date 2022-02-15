
# import the modules
import time
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler
from file_handler import on_create

def create_event_handler():
    # create the event handler
    ignore_directories = False
    case_sensitive = True
    my_event_handler = RegexMatchingEventHandler(ignore_directories=ignore_directories,
                                                 case_sensitive=case_sensitive)
    return my_event_handler


def start_listener(path):
    event_handler = create_event_handler()
    event_handler.on_created = on_create

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

