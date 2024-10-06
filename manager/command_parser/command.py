from NodeManager.manager.command_parser.option import FuncCommandOptionWrap


class CommandLineBind:
    def __init__(self, cmd_func_map: dict[str, FuncCommandOptionWrap]):
        self._cmd_func_map = cmd_func_map

    def __call__(self, sub_cmd: str) -> callable:
        # sub_cmd = sub_cmds.pop(0)
        if sub_cmd not in self._cmd_func_map:
            raise Exception(f"Invalid command: {sub_cmd}")

        return self._cmd_func_map[sub_cmd]


class CommandLineChain:

    def __init__(self, cmd_bind: CommandLineBind):
        self._cmd_bind = cmd_bind

    def __call__(self, full_cmd: list[str]):
        f = self._cmd_bind
        end_index = 0
        for i, cmd_part in enumerate(full_cmd):
            f = f(cmd_part)
            if isinstance(f, CommandLineBind):
                continue
            else:
                end_index = i + 1
                break

        remaining_args = full_cmd[end_index:] if end_index < len(full_cmd) else []

        return f(*remaining_args)


