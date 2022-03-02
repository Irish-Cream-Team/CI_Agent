import logging
import colorama
from input_monitor.input_monitor import InputMonitor


class DebugHandler(logging.Handler):
    _color_dict = {"DEBUG": str(),
                   "INFO": colorama.Fore.GREEN,
                   "WARNING": colorama.Fore.YELLOW,
                   "ERROR": colorama.Fore.RED,
                   "CRITICAL": colorama.Fore.MAGENTA}

    def __init__(self):
        super().__init__()
        colorama.init(autoreset=True)

    def emit(self, record):
        print(self._color_dict[record.levelname] + self.format(record))


def main():
    logging.basicConfig(handlers=[DebugHandler()],
                        level=logging.DEBUG,
                        format='%(asctime)s\t\t%(processName)s\t\t%(name)s\t\t%(levelname)s\t\t%(message)s')
    with InputMonitor(config_path="config.json") as im:
        im.start_monitor()


if __name__ == '__main__':
    main()
