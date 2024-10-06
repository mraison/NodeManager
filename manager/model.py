from NodeManager.manager.dao import NodeDAO, CentralConfigDAO
from NodeManager.model import DeviceCollection


class CentralConfigModel:
    def __init__(
        self,
        dao: CentralConfigDAO = CentralConfigDAO()
    ):
        self._config = DeviceCollection([])
        self._dao = dao

    def load_all(self):
        payload = self._dao.get()
        self._config = DeviceCollection.load_from_struct(payload)

    def get(self):
        return self._config


class Node:
    def __init__(self, ip: str, port: str, dao: NodeDAO = None):
        self.ip = ip
        self.port = port
        self._dao = dao or NodeDAO(f"http://{ip}:{port}/")
        self._config = DeviceCollection([])

    def configure(self, devices: DeviceCollection):
        self._config = devices
        self._dao.post(devices.to_dict())

    def get_config(self):
        return self._config

    def load_config(self):
        payload = self._dao.get()
        self._config = DeviceCollection.load_from_struct(payload)
