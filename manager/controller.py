from NodeManager.chunker.model import DeviceChunkGroups
from NodeManager.model import Device, DeviceCollection
from NodeManager.manager.model import Node


class NodeManager:
    def __init__(self, nodes: list[Node], devices: DeviceCollection):
        self.nodes = nodes
        self.devices = devices
        self.device_chunk_groups = DeviceChunkGroups(len(self.nodes))

    def load_devices(self):
        self.devices.load_all()
        self.device_chunk_groups = DeviceChunkGroups(len(self.nodes))
        for device in self.devices.data:
            self.device_chunk_groups.create_device(device)

    def configure_nodes(self):
        configs = self._compose_node_configurations()
        for i, node in enumerate(self.nodes):
            node.configure(
                configs[i]
            )

    def _compose_node_configurations(self):
        payloads = {}
        for device in self.devices.data:

            chunk_groups = self.device_chunk_groups.get_chunk_groups(device.id)
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
