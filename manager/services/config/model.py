from pathlib import Path
from dataclasses import dataclass

from NodeManager.manager.services.config.dao import write_config_to_file, read_config_from_file
from NodeManager.model import DeviceCollection


@dataclass
class Node:
    id: str
    ip: str
    port: int

    def to_struct(self):
        return {
            "id": self.id,
            "ip": self.ip,
            "port": self.port
        }

    @classmethod
    def load_from_struct(cls, data: dict):
        _id = data.get("id", "")
        ip = data.get("ip", "")
        port = data.get("port", -1)
        if ip == "" or port == -1 or _id == "":
            raise Exception("Invalid data, cannot load.")

        return cls(_id, ip, port)


@dataclass
class NodeCollection:
    nodes: list[Node]

    def to_struct(self):
        return [
            node.to_struct() for node in self.nodes
        ]

    @classmethod
    def load_from_struct(cls, data: list):
        nodes = [
            Node.load_from_struct(sub_data) for sub_data in data
        ]
        return cls(nodes)


@dataclass
class DeviceConfig:
    source: str
    devices: DeviceCollection

    def to_struct(self):
        return {
            'source': self.source,
            'devices': self.devices.to_struct()
        }

    @classmethod
    def load_from_struct(cls, data: dict):
        source = data.get("source", "")
        devices = DeviceCollection.load_from_struct(data.get("devices", []))
        # if source == "":
        #     raise Exception("Invalid data, cannot load.")

        return cls(source, devices)


@dataclass
class _Config:
    nodes_collection: NodeCollection
    device_config: DeviceConfig

    def to_struct(self):
        return {
            'nodes_collection': self.nodes_collection.to_struct(),
            'device_config': self.device_config.to_struct()
        }

    @classmethod
    def load_from_struct(cls, data: dict):
        return cls(
            NodeCollection.load_from_struct(data.get('nodes_collection', [])),
            DeviceConfig.load_from_struct(data.get('device_config', {}))
        )


class ManagerConfigModel:
    def __init__(self, config_file: Path):
        self.config = _Config(
            nodes_collection=NodeCollection([]),
            device_config=DeviceConfig("", DeviceCollection([]))
        )
        self._config_file = config_file

    def load(self):
        self.config = _Config.load_from_struct(
            read_config_from_file(self._config_file)
        )

    def save(self):
        write_config_to_file(self.config.to_struct(), self._config_file)
