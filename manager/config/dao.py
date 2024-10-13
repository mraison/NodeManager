from pathlib import Path


class FileDao:
    def __init__(self, file: Path):
        self._file = file

    def read_from_file(self):
        if self._file.exists() and self._file.is_file():
            return self._file.read_text()
        else:
            return ""

    def write_to_file(self, payload: str):
        self._file.write_text(payload)
