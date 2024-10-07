from typing import Protocol


class ParserType(Protocol):
    def get_help(self, layer: int = 0):
        """
        Return the help text associated.
        """

    def __call__(self, *args, **kwargs):
        """
        Must be callable
        """
