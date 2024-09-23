from NodeManager.manager.dao import NodeDAO
from NodeManager.model import Device


class Node:
    def __init__(self, ip: str, port: str, dao: NodeDAO = None):
        self.ip = ip
        self.port = port
        self._dao = dao or NodeDAO(f"http://{ip}:{port}/")
        self._config: list[Device] = None

    def configure(self, devices: list[Device]):
        self._config = devices

        self._dao.post([
            device.to_dict() for device in devices
        ])

    def get_config(self):
        return self._config

    def load_config(self):
        self._config = self._dao.get()
