import os

from NodeManager.manager.services.command_parser.option import OptionCollection


class FuncWrap:
    _indent = "  "

    def __init__(
        self,
        f: callable,
        options: OptionCollection = OptionCollection([]),
        help_txt: str = ""
    ):
        self._f = f
        self._opts = options
        self._help = help_txt

    def get_help(self, layer: int = 0):
        indent = self._indent * layer
        sub_text = self._opts.get_help(layer + 1)
        if sub_text == "":
            return f"{os.linesep}{indent}(func) {self._help}"
        else:
            return f"{os.linesep}{indent}(func) {self._help}: {self._opts.get_help(layer + 1)}"

    def print_help(self):
        print(self.get_help())

    def __call__(self, cmd_line_args: list[str] = []):
        if 'help' in cmd_line_args:
            return self.print_help
        return self._f(
            *self._opts(cmd_line_args)
        )
