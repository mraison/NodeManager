import os


class Option:
    _indent = "  "

    def __init__(self, cast: callable, help_txt: str = ""):
        self._cast = cast
        self._help = help_txt

    def get_help(self, layer: int = 0):
        # indent = self._indent * layer
        return self._help

    def print_help(self):
        print(self.get_help())

    def __call__(self, val):
        if 'help' == val:
            return self.print_help
        try:
            return self._cast(val)
        except Exception as e:
            raise Exception(f"Invalid type error: {e}")


class OptionCollection:
    _indent = "  "

    def __init__(self, options: list[Option] = []):
        self._options = options

    def get_help(self, layer: int = 0):
        help_txt = ""
        indent = self._indent * layer
        for i, option in enumerate(self._options):
            help_txt += f"{os.linesep}{indent}(opt {i}) {option.get_help(layer + 1)}"

        return help_txt

    def print_help(self):
        print(self.get_help())

    def __call__(self, options: list[str] = []):
        if 'help' in options:
            return self.print_help

        cast_opts = []
        for i, option in enumerate(options):
            try:
                cast_opts.append(
                    self._options[i](option)
                )
            except Exception:
                raise Exception("Too many arguments provided.")

        return cast_opts
