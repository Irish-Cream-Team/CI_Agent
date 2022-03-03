from os import DirEntry


class File:
    def __init__(self, name, path, size, time):
        self._name = name
        self._path = path
        self._size = size
        self._time = time

    @classmethod
    def from_dict(cls, dict):
        return cls(dict['name'], dict['path'], dict['size'], dict['time'])

    @classmethod
    def from_dir_entry(cls, dir_entry):
        if(dir_entry.is_file()):
            return cls(dir_entry.name, dir_entry.path, dir_entry.stat().st_size, dir_entry.stat().st_mtime)
        else:
            raise Exception("Not a file")

    def to_dict(self):
        return {
            'name': self.get_name(),
            'path': self.get_path(),
            'size': self.get_size(),
            'time': self.get_time()
        }

    def is_updated(self, dir_entry):
        return self.get_time() != dir_entry.stat().st_mtime or self.get_size() != dir_entry.stat().st_size

    def get_name(self) -> str:
        return self._name

    def get_path(self) -> str:
        return self._path

    def get_size(self) -> int:
        return self._size

    def get_time(self) -> int:
        return self._time
