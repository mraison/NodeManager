import sys
from pathlib import Path

from NodeManager.manager.command_parser.command import CommandChain, CommandOptionBind
from NodeManager.manager.command_parser.func import FuncWrap
from NodeManager.manager.command_parser.option import Option, OptionCollection
from NodeManager.manager.service.model import Service


service = Service(
    Path("./config.json")
)


service_command_map = CommandChain(
    CommandOptionBind(
        {
            'reset': FuncWrap(
                f=service.reset,
                help_txt="Full reset of settings"
            ),
            'device': CommandOptionBind(
                {
                    'pull': FuncWrap(
                        f=service.pull_device_config,
                        help_txt="Pull device config from upstream"
                    ),
                    'list': FuncWrap(
                        f=service.print_device_config,
                        help_txt="Show current device config"
                    ),
                    'source': FuncWrap(
                        f=service.set_device_source,
                        help_txt="Set device config source",
                        options=OptionCollection(
                            [
                                Option(str, help_txt="source must be a string."),
                            ]
                        ),
                    ),
                }
            ),
            'node': CommandOptionBind(
                {
                    'add': FuncWrap(
                        f=service.add_node,
                        help_txt="Adds a Node to configuration"
                    ),
                    'list': FuncWrap(
                        f=service.print_node,
                        options=OptionCollection(
                            [
                                Option(str, help_txt="Node id must be str")
                            ]
                        ),
                        help_txt="list a Node configuration"
                    ),
                    'list-all': FuncWrap(
                        f=service.print_nodes,
                        help_txt="list all Node to configurations"
                    ),
                    'remove': FuncWrap(
                        f=service.remove_node,
                        options=OptionCollection(
                            [
                                Option(str, help_txt="Node id must be str")
                            ]
                        ),
                        help_txt="Remove a Node to configuration"
                    ),
                    'send-conf': FuncWrap(
                        f=service.distribute_config_to_nodes,
                        help_txt="Distribute device configurations across nodes."
                    ),
                }
            )
        }
    )
)


if __name__ == "__main__":
    opt = sys.argv
    opt.pop(0)

    service_command_map(
        opt
    )