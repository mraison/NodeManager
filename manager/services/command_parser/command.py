import os

from NodeManager.manager.services.command_parser.protocol import ParserType


class CommandOptionBind:
    _indent = "  "

    def __init__(self, cmd_func_map: dict[str, ParserType]):
        self._cmd_func_map = cmd_func_map

    def get_help(self, layer: int = 0):
        help_txt = ""
        indent = self._indent * layer
        for key, func in self._cmd_func_map.items():
            help_txt += f"{os.linesep}{indent}(cmd) {key}: {func.get_help(layer + 1)}"

        return help_txt

    def print_help(self, *args, **kwargs):
        print(self.get_help())

    def __call__(self, sub_cmd: str) -> callable:
        if 'help' == sub_cmd:
            return self.print_help

        if sub_cmd not in self._cmd_func_map:
            raise Exception(f"Invalid command: {sub_cmd}")

        return self._cmd_func_map[sub_cmd]


class CommandChain:

    def __init__(self, cmd_bind: CommandOptionBind):
        self._cmd_bind = cmd_bind

    def get_help(self, layer: int = 0):
        return self._cmd_bind.get_help(layer + 1)

    def print_help(self):
        print(self.get_help())

    def __call__(self, full_cmd: list[str]):
        if len(full_cmd) > 0 and 'help' == full_cmd[0]:
            return self.print_help()

        f = self._cmd_bind
        end_index = 0
        for i, cmd_part in enumerate(full_cmd):
            f = f(cmd_part)
            if isinstance(f, CommandOptionBind):
                continue
            else:
                end_index = i + 1
                break

        remaining_args = full_cmd[end_index:] if end_index < len(full_cmd) else []
        return f(remaining_args)


