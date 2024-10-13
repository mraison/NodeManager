from pathlib import Path

from NodeManager.manager.config.model import Config
from NodeManager.manager.service.client import DevicesClient, NodeClient
from NodeManager.manager.distributors.distributors import distribute_device_address_book
from NodeManager.manager.service.utils import _start_node, _stop_node


class Service:
    def __init__(self, config_file: Path):
        self._conf = Config(config_file)
        self._conf.load()

    def reset(self):
        self._conf.empty()
        self._conf.save()

    def add_node(self):
        ip, port, _id = _start_node()
        self._conf.node_configs.add(ip=ip, port=port, id=_id)
        self._conf.save()

    def print_node(self, _id: str):
        try:
            node = self._conf.node_configs.find_node(_id)
            print(node.to_struct())
        except Exception:
            print(f"node {_id} not found.")

    def print_nodes(self):
        print(
            self._conf.node_configs.to_struct()
        )

    def remove_node(self, _id: str):
        try:
            node = self._conf.node_configs.remove(_id)
        except Exception:
            print(f"node {_id} not found.")
            return

        _stop_node(int(node.id))
        self._conf.save()

    def print_device_config(self):
        print(
            self._conf.device_configs.to_struct()
        )

    def set_device_source(self, source: str):
        self._conf.device_configs.source = source
        self._conf.save()

    def pull_device_config(self):
        cli = DevicesClient(
            self._conf.device_configs.source
        )
        self._conf.device_configs.devices = cli.get_config()
        self._conf.save()

    def distribute_config_to_nodes(self):
        node_configs = distribute_device_address_book(
            self._conf.device_configs.devices,
            len(self._conf.node_configs.nodes)
        )
        for i, node in enumerate(self._conf.node_configs.nodes):
            NodeClient(node.ip, node.port).send_config(
                node_configs[i]
            )
