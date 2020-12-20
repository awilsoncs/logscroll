import unittest

from logscroll.commands import Command
from logscroll.scrollers import DefaultScroller


class CreateCounterCommand(Command):
    def do(self, context: dict):
        context['counter'] = 0

    def undo(self, context: dict):
        del context['counter']


class IncrementCounterCommand(Command):

    def do(self, context: dict):
        context['counter'] += 1

    def undo(self, context: dict):
        context['counter'] -= 1


class TestScroller(unittest.TestCase):
    def test_add_command(self):
        scroller = DefaultScroller()
        scroller.add_command(CreateCounterCommand())
        self.assertEqual(0, scroller.get_context()['counter'])
        scroller.add_command(IncrementCounterCommand())
        self.assertEqual(1, scroller.get_context()['counter'])
        scroller.add_command(IncrementCounterCommand())
        self.assertEqual(2, scroller.get_context()['counter'])

    def test_step_backwards(self):
        scroller = DefaultScroller()
        scroller.add_command(CreateCounterCommand())
        self.assertEqual(0, scroller.get_context()['counter'])
        scroller.add_command(IncrementCounterCommand())
        self.assertEqual(1, scroller.get_context()['counter'])
        scroller.add_command(IncrementCounterCommand())
        self.assertEqual(2, scroller.get_context()['counter'])
        scroller.step_backwards()
        self.assertEqual(1, scroller.get_context()['counter'])
        scroller.step_backwards()
        self.assertEqual(0, scroller.get_context()['counter'])
        scroller.step_backwards()
        self.assertFalse('counter' in scroller.get_context())

    def test_restart(self):
        scroller = DefaultScroller()
        scroller.add_command(CreateCounterCommand())
        scroller.add_command(IncrementCounterCommand())
        scroller.add_command(IncrementCounterCommand())
        scroller.restart()
        self.assertFalse('counter' in scroller.get_context())

    def test_restart_then_step_forward(self):
        scroller = DefaultScroller()
        scroller.add_command(CreateCounterCommand())
        scroller.add_command(IncrementCounterCommand())
        scroller.add_command(IncrementCounterCommand())
        scroller.restart()
        scroller.step_forwards()
        self.assertEqual(0, scroller.get_context()['counter'])
        scroller.step_forwards()
        self.assertEqual(1, scroller.get_context()['counter'])
        scroller.step_forwards()
        self.assertEqual(2, scroller.get_context()['counter'])


if __name__ == '__main__':
    unittest.main()
