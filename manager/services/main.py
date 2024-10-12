import sys
import uuid
from pathlib import Path

from NodeManager.manager.services.config.model import Node
from NodeManager.manager.services.command_parser.command import CommandChain, CommandOptionBind
from NodeManager.manager.services.command_parser.func import FuncWrap
from NodeManager.manager.services.command_parser.option import Option, OptionCollection
from NodeManager.manager.services.config.model import ManagerConfigModel
from NodeManager.manager.services.utils import generate_unique_string


config_file = Path("./config.json")
if not config_file.exists():
    config_file.write_text("")

config_container = ManagerConfigModel(
    config_file
)
config_container.load()


def add_node(ip, port):
    _id = generate_unique_string()
    config_container.config.nodes_collection.nodes.append(
        Node(ip=ip, port=port, id=_id)
    )
    print(f"node id: {_id}")
    config_container.save()


def list_node(_id: str):
    for node in config_container.config.nodes_collection.nodes:
        if node.id == _id:
            print(
                node.to_struct()
            )
            return


def list_all_nodes():
    print(
        config_container.config.nodes_collection.to_struct()
    )


def remove_node(_id: str):
    found_index = -1
    for i, node in enumerate(config_container.config.nodes_collection.nodes):
        if node.id == _id:
            found_index = i
            break

    if found_index >= 0:
        config_container.config.nodes_collection.nodes.pop(found_index)

    config_container.save()


service_command_map = CommandChain(
    CommandOptionBind(
        {
            'node': CommandOptionBind(
                {
                    # 'start': FuncWrap(
                    #     f=()
                    # ),
                    # 'stop': FuncWrap(
                    #     f=()
                    # ),
                    'add': FuncWrap(
                        f=add_node,
                        options=OptionCollection(
                            [
                                Option(str, help_txt="ip must be string"),
                                Option(int, help_txt="port must be int")
                            ]
                        ),
                        help_txt="Adds a Node to configuration"
                    ),
                    'list': FuncWrap(
                        f=list_node,
                        options=OptionCollection(
                            [
                                Option(str, help_txt="Node id must be str")
                            ]
                        ),
                        help_txt="list a Node configuration"
                    ),
                    'list-all': FuncWrap(
                        f=list_all_nodes,
                        help_txt="list all Node to configurations"
                    ),
                    'remove': FuncWrap(
                        f=remove_node,
                        options=OptionCollection(
                            [
                                Option(str, help_txt="Node id must be str")
                            ]
                        ),
                        help_txt="Remove a Node to configuration"
                    ),
                }
            )
        }
    )
)
# {
#     'node': [
#         'start',
#         'stop',
#         'add',
#         'remove',
#         'clear'
#     ],
#     'central_config': [
#         'pull',
#         'clear'
#     ]
# }


if __name__ == "__main__":
    opt = sys.argv
    opt.pop(0)

    service_command_map(
        opt
    )

    # if opt == "configure_nodes":
    #     m.load_devices()
    #     m.configure_nodes()
