from pathlib import Path
import json
import sys

from NodeManager.manager.controller import NodeManager
from NodeManager.manager.model import Node, CentralConfigModel
from NodeManager.manager.services.model import ManagerConfigModel


option_map = {
    'node': [
        'start',
        'stop',
        'add',
        'remove',
        'clear'
    ],
    'central_config': [
        'pull',
        'clear'
    ]
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
        ],
        config=CentralConfigModel()
    )
    if opt not in option_map:
        raise Exception('invalid option.')

    if opt == "configure_nodes":
        m.load_devices()
        m.configure_nodes()
