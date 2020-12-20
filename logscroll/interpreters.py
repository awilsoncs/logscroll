from abc import ABCMeta, abstractmethod

from logscroll.scrollers import DefaultScroller


class Interpreter(metaclass=ABCMeta):
    @abstractmethod
    def read_line(self, line: str) -> None:
        """Interpret a string and add a command."""
        pass


class DefaultInterpreter(Interpreter):
    def __init__(self, patterns=None, scroller=None):
        self._patterns = patterns if patterns else []
        self._scroller = scroller if scroller else DefaultScroller()

    def read_line(self, line):
        """Interpret a string and add a command."""
        for pattern in self._patterns:
            if pattern.is_match(line):
                command = pattern.get_command(line)
                self._scroller.add_command(command)
