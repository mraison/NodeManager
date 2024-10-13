from NodeManager.manager.client import NodeClient, DevicesClient
from NodeManager.distributors.distributors import distribute_device_address_book


class NodeManager:
    def __init__(self, nodes: list[NodeClient], devices: DevicesClient):
        self.nodes = nodes
        self.devices_config = devices
        self.node_configs = []

    def load_central_config(self):
        self.devices_config.load_config()

    def configure_nodes(self):
        node_configs = distribute_device_address_book(
            self.devices_config.get_config(),
            len(self.nodes)
        )
        for i, node in enumerate(self.nodes):
            node.configure(
                node_configs[i]
            )
