from pathlib import Path
from dataclasses import dataclass, replace

from NodeManager.manager.services.utils import write_config_to_file, read_config_from_file
from NodeManager.model import DeviceCollection


@dataclass
class Node:
    id: int
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
        _id = data.get("id", -1)
        ip = data.get("ip", "")
        port = data.get("port", -1)
        if ip == "" or port == -1 or _id == -1:
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


class _Config:
    nodes_collection: NodeCollection
    devices_collection: DeviceCollection

    def to_struct(self):
        return {
            'nodes_collection': self.nodes_collection.to_struct(),
            'devices_collection': self.devices_collection.to_struct()
        }

    @classmethod
    def load_from_struct(cls, data: dict):
        return cls(
            NodeCollection.load_from_struct(data.get('nodes_collection', [])),
            DeviceCollection.load_from_struct(data.get('devices_collection', []))
        )


class ManagerConfigModel:
    def __init__(self, config_file: Path):
        self.config = {}
        self._config_file = config_file

    def load(self):
        self.config = _Config.load_from_struct(
            read_config_from_file(self._config_file)
        )

    def save(self):
        write_config_to_file(self.config, self._config_file)
