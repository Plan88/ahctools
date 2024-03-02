from abc import ABCMeta, abstractmethod

from .io import IInput, IOutput


class IEvaluator(metaclass=ABCMeta):
    def __init__(self, input: IInput):
        self.input = input

    @abstractmethod
    def evaluate(self, output: IOutput) -> float:
        raise NotImplementedError()
