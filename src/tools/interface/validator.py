from abc import ABCMeta, abstractmethod

from .io import IOutput


class Validator(metaclass=ABCMeta):
    @abstractmethod
    def validate_output(self, output: IOutput):
        raise NotImplementedError()
