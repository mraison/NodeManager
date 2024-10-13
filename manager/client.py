from NodeManager.manager.dao import NodeDAO, DevicesDAO
from NodeManager.model import DeviceCollection


class DevicesClient:
    def __init__(
        self,
        devices: DeviceCollection = DeviceCollection([]),
        dao: DevicesDAO = DevicesDAO()
    ):
        self._devices = devices
        self._dao = dao

    def load_config(self):
        payload = self._dao.get()
        self._devices = DeviceCollection.load_from_struct(payload)

    def get_config(self):
        return self._devices


class NodeClient:
    def __init__(self, ip: str, port: str, dao: NodeDAO = None):
        self.ip = ip
        self.port = port
        self._dao = dao or NodeDAO(f"http://{ip}:{port}/")
        self._config = DeviceCollection([])

    def configure(self, devices: DeviceCollection):
        self._config = devices
        self._dao.post(devices.to_struct())

    def get_config(self):
        return self._config

    def load_config(self):
        payload = self._dao.get()
        self._config = DeviceCollection.load_from_struct(payload)
