from abc import ABC, abstractmethod


class Command(ABC):

    @abstractmethod
    def do(self, context: dict) -> None:
        pass

    @abstractmethod
    def undo(self, context: dict) -> None:
        pass
