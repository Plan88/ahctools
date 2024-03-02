from abc import ABCMeta, abstractmethod

from .io import IOutput


class IValidator(metaclass=ABCMeta):
    @abstractmethod
    def validate_output(self, output: IOutput):
        raise NotImplementedError()
