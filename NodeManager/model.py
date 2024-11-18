from dataclasses import dataclass


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

    def to_struct(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

    @classmethod
    def load_from_struct(cls, data: dict):
        _id = data.get("id", -1)
        name = data.get("name", "")
        email = data.get("email", "")
        if _id == -1 or name == "" or email == "":
            raise Exception("Invalid data, cannot load.")
        return cls(
            _id, name, email
        )


@dataclass
class Device:
    id: int
    name: str
    subscribers: list[Address]

    def to_struct(self):
        return {
            "id": self.id,
            "name": self.name,
            "subscribers": [add.to_struct() for add in self.subscribers]
        }

    @classmethod
    def load_from_struct(cls, data: dict):
        _id = data.get("id", -1)
        name = data.get("name", "")
        subscribers = []
        for add in data.get("subscribers", []):
            subscribers.append(Address.load_from_struct(add))
        if _id == -1 or name == "":
            raise Exception("Invalid data, cannot load.")
        return cls(
            _id, name, subscribers
        )


@dataclass
class DeviceCollection:
    devices: list[Device]

    def to_struct(self):
        return [
            device.to_struct() for device in self.devices
        ]

    @classmethod
    def load_from_struct(cls, data: list):
        devices = [
            Device.load_from_struct(sub_data) for sub_data in data
        ]
        return cls(devices)
