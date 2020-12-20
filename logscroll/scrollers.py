from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import List

from logscroll.commands import Command


class Scroller(metaclass=ABCMeta):
    @abstractmethod
    def add_command(self, command: Command) -> None:
        pass

    @abstractmethod
    def step_forwards(self) -> None:
        pass

    @abstractmethod
    def step_backwards(self) -> None:
        pass

    @abstractmethod
    def restart(self) -> None:
        pass

    @abstractmethod
    def get_context(self) -> dict:
        pass

    @abstractmethod
    def get_execution_index(self) -> int:
        pass


class DefaultScroller(Scroller):
    def __init__(self):
        self._command_stack: List[Command] = []
        self._context: dict = {}
        self._execution_index: int = -1

    def add_command(self, command):
        self._command_stack.append(command)
        command.do(self._context)
        self._execution_index += 1

    def step_forwards(self):
        self._execution_index += 1
        command_to_do = self._command_stack[self._execution_index]
        command_to_do.do(self._context)

    def step_backwards(self):
        command_to_undo = self._command_stack[self._execution_index]
        command_to_undo.undo(self._context)
        self._execution_index -= 1

    def restart(self):
        while self._execution_index >= 0:
            self.step_backwards()

    def get_context(self):
        return self._context

    def get_execution_index(self):
        return self._execution_index
