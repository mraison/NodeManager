from pathlib import Path
import json
import sys

from NodeManager.manager.controller import NodeManager
from NodeManager.manager.model import Node


def load_config_from_file(config_file: Path):
    if config_file.exists() and config_file.is_file():
        return json.loads(
            config_file.read_text()
        )


config = load_config_from_file(Path("~/node_man_conf.json"))

option_map = {
    'configure_nodes'
}


def run():
    opt = sys.argv[1]

    m = NodeManager(
        nodes=[
            Node(
                ip=node["ip"],
                port=node["port"],
                dao=None
            ) for node in config["nodes"]
        ]
    )
    if opt not in option_map:
        raise Exception('invalid option.')

    if opt == "configure_nodes":
        m.load_devices()
        m.configure_nodes()
