import requests

from NodeManager.chunker.model import DeviceChunkGroups
from NodeManager.node.model import Node
from NodeManager.model import Device, Address, DeviceCollection


class Manager:
    _config_uri = "/config"
    _method = "POST"

    def __init__(self, nodes: list[Node], devices: DeviceCollection):
        self._nodes = nodes
        self._devices = devices
        self._device_chunk_groups = DeviceChunkGroups(len(self._nodes))

    def load_devices(self):
        self._devices.load_all()
        for device in self._devices.data:
            self._device_chunk_groups.create_device(device)

    def configure_nodes(self):
        configs = self._compose_node_configurations()
        for i, node in enumerate(self._nodes):
            node.configure(
                configs[i]
            )

    def _compose_node_configurations(self):
        payloads = {}
        for device in self._devices.data:

            chunk_groups = self._device_chunk_groups.get_chunk_groups(device.id)
            for i, chunk in enumerate(chunk_groups):
                if i not in payloads:
                    payloads[i] = []
                payloads[i].append(
                    Device(
                        id=device.id,
                        name=device.name,
                        subscribers=chunk.subscribers
                    )
                )
        return payloads





