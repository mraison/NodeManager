class CommandOption:
    def __init__(self, cast: callable):
        self._cast = cast

    def __call__(self, val):
        try:
            return self._cast(val)
        except Exception as e:
            raise Exception(f"Invalid type error: {e}")


class CommandOptionCollection:
    def __init__(self, options: list[CommandOption] = []):
        self._options = options

    def __call__(self, options: list[str] = []):
        cast_opts = []
        for i, option in enumerate(options):
            try:
                cast_opts.append(
                    self._options[i](option)
                )
            except Exception:
                raise Exception("Too many arguments provided.")

        return cast_opts


class FuncCommandOptionWrap:
    def __init__(self, f: callable, options: CommandOptionCollection = CommandOptionCollection([])):
        self._f = f
        self._opts = options

    def __call__(self, cmd_line_args: list[str] = []):
        return self._f(
            *self._opts(cmd_line_args)
        )
