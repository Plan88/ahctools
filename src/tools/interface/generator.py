import random
from abc import ABCMeta, abstractmethod

from .io import IInput


class IGenerator(metaclass=ABCMeta):
    def __init__(self, seed: int | None = None):
        self.rand = random.Random(seed)

    @abstractmethod
    def _gen(self):
        raise NotImplementedError()

    def __call__(self, *args):
        return self._gen(*args)


def gen_input(
    seed: int, N: int | None = None, M: int | None = None, eps: int | None = None
) -> IInput:
    raise NotImplementedError()
