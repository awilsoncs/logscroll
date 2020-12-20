from abc import ABC, abstractmethod

from logscroll.commands import Command


class Pattern(ABC):
    """Define a rule for interpreting a line of text as a command."""

    @staticmethod
    @abstractmethod
    def is_match(line: str) -> bool:
        """Return whether this string matches the pattern."""
        pass

    @staticmethod
    @abstractmethod
    def get_command(line: str) -> Command:
        """Get a command to represent this line in context."""
        pass
