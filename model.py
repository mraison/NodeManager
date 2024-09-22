from dataclasses import dataclass

from NodeManager.dao import DeviceDAO


@dataclass
class Address:
    id: int
    name: str
    email: str

    def __eq__(self, other):
        return self.__key() == self.__key()

    def __key(self):
        return self.id, self.name, self.email

    def __hash__(self):
        return hash(self.__key())


@dataclass
class Device:
    id: int
    name: str
    subscribers: list[Address]


class DeviceCollection:
    def __init__(
        self,
        dao: DeviceDAO
    ):
        self.data: list[Device] = []

        self._dao = dao

    def load_all(self):
        payload = self._dao.get()

        self.data = []
        for device in payload:
            subscribers = []
            for address in device.get('subscribers', []):
                subscribers.append(
                    Address(
                        id=address['id'],
                        name=address['name'],
                        email=address['email']
                    )
                )
            self.data.append(
                Device(
                    id=device['id'],
                    name=device['name'],
                    subscribers=subscribers
                )
            )
