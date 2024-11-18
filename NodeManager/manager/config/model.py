from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass

from NodeManager.model import DeviceCollection
from NodeManager.manager.config.client import LocalConfigClient


@dataclass
class _NodeConfig:
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
class _NodeConfigCollection:
    nodes: list[_NodeConfig]

    def add(self, ip: str, port: int, id: str):
        self.nodes.append(
            _NodeConfig(ip=ip, port=port, id=id)
        )

    def remove(self, _id: str):
        i = self._find_node_index(_id)
        if i != -1:
            return self.nodes.pop(i)
        else:
            raise Exception(f"id {_id} not found")

    def _find_node_index(self, _id: str):
        for i, node in enumerate(self.nodes):
            if node.id == _id:
                return i
        return -1

    def find_node(self, _id: str):
        i = self._find_node_index(_id)
        if i != -1:
            return self.nodes[i]
        else:
            raise Exception(f"id {_id} not found")

    def to_struct(self):
        return [
            node.to_struct() for node in self.nodes
        ]

    @classmethod
    def load_from_struct(cls, data: list):
        nodes = [
            _NodeConfig.load_from_struct(sub_data) for sub_data in data
        ]
        return cls(nodes)


@dataclass
class _DevicesConfigCollection:
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

        return cls(source, devices)


class Config:
    def __init__(self, config_file: Path, cli: LocalConfigClient = None):
        self._file = config_file
        self._cli = cli or LocalConfigClient(self._file)
        self._cli.ensure()

        self.node_configs = _NodeConfigCollection([])
        self.device_configs = _DevicesConfigCollection(
            source="",
            devices=DeviceCollection([])
        )

    def load(self):
        payload = self._cli.read_config()
        self.node_configs = _NodeConfigCollection.load_from_struct(
            payload.get('node_configs', [])
        )
        self.device_configs = _DevicesConfigCollection.load_from_struct(
            payload.get('device_configs', {})
        )

    def empty(self):
        self.node_configs = _NodeConfigCollection([])
        self.device_configs = _DevicesConfigCollection(
            source="",
            devices=DeviceCollection([])
        )

    def save(self):
        self._cli.write_config(
            {
                'node_configs': self.node_configs.to_struct(),
                'device_configs': self.device_configs.to_struct()
            }
        )
