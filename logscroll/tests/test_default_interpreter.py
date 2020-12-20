import unittest
from dataclasses import dataclass

from logscroll.commands import Command
from logscroll.interpreters import DefaultInterpreter
from logscroll.patterns import Pattern
from logscroll.scrollers import Scroller


class TestScroller(Scroller):
    def __init__(self):
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def step_forwards(self):
        pass

    def step_backwards(self):
        pass

    def restart(self):
        pass

    def get_context(self):
        pass

    def get_execution_index(self):
        pass


class TestCommand(Command):
    def do(self, context: dict):
        pass

    def undo(self, context: dict):
        pass


class TestDefaultInterpreter(unittest.TestCase):
    def test_add_command_good_line(self):
        command = TestCommand()

        class TestPattern(Pattern):
            @staticmethod
            def is_match(line):
                return True

            @staticmethod
            def get_command(line):
                return command

        scroller = TestScroller()

        interpreter = DefaultInterpreter(
            patterns=[TestPattern],
            scroller=scroller
        )
        interpreter.read_line('actual input doesnt matter here')
        self.assertIn(
            command,
            scroller.commands
        )

    def test_dont_add_bad_command(self):
        bad_command = TestCommand()

        class TestPattern(Pattern):
            @staticmethod
            def is_match(line: str) -> bool:
                return False

            @staticmethod
            def get_command(line: str) -> Command:
                return bad_command

        scroller = TestScroller()

        interpreter = DefaultInterpreter(
            patterns=[TestPattern],
            scroller=scroller
        )

        interpreter.read_line('actual input doesnt matter here')
        self.assertNotIn(
            bad_command,
            scroller.commands
        )




if __name__ == '__main__':
    unittest.main()
