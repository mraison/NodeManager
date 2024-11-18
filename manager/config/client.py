from pathlib import Path
import json

from NodeManager.manager.config.dao import FileDao


class LocalConfigClient:
    def __init__(
        self,
        file: Path,
        dao: FileDao = None
    ):
        self._dao = dao or FileDao(file)

    def ensure(self):
        self._dao.ensure()

    def read_config(self):
        payload = self._dao.read_from_file()
        return json.loads(
            payload
        )

    def write_config(self, config: dict):
        return self._dao.write_to_file(
            json.dumps(
                config
            )
        )
