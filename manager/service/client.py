from NodeManager.manager.service.dao import NodeDAO, DevicesDAO
from NodeManager.model import DeviceCollection


class DevicesClient:
    def __init__(
        self,
        source: str,
        dao: DevicesDAO = None
    ):
        self._dao = dao or DevicesDAO(source)

    def get_config(self):
        payload = self._dao.get()
        return DeviceCollection.load_from_struct(payload)


class NodeClient:
    def __init__(self, ip: str, port: str, dao: NodeDAO = None):
        self.ip = ip
        self.port = port
        self._dao = dao or NodeDAO(f"http://{ip}:{port}/")
        self._config = DeviceCollection([])

    def send_config(self, devices: DeviceCollection):
        self._dao.post(devices.to_struct())

    def get_config(self):
        payload = self._dao.get()
        return DeviceCollection.load_from_struct(payload)
