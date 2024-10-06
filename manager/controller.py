from NodeManager.manager.model import Node, CentralConfigModel
from NodeManager.distributors.distributors import distribute_device_address_book


class NodeManager:
    def __init__(self, nodes: list[Node], config: CentralConfigModel):
        self.nodes = nodes
        self.central_config = config
        self.node_configs = []

    def load_central_config(self):
        self.central_config.load_all()

    def configure_nodes(self):
        node_configs = distribute_device_address_book(
            self.central_config.get(),
            len(self.nodes)
        )
        for i, node in enumerate(self.nodes):
            node.configure(
                node_configs[i]
            )
