from abc import ABCMeta, abstractmethod
import random

from .io import Input


class Generator(metaclass=ABCMeta):
    def __init__(self, seed: int | None = None):
        self.rand = random.Random(seed)

    @abstractmethod
    def _gen(self):
        pass

    def __call__(self, *args):
        return self._gen(*args)


class NGenerator(Generator):
    def _gen(self, N: int | None = None):
        if N is None:
            N = self.rand.randint(10, 20)
        return N


class MGenerator(Generator):
    def _gen(self, N: int, M: int | None = None) -> int:
        if M is None:
            M = self.rand.randint(2, N * N // 20)
        return M


class EpsGenerator(Generator):
    def _gen(self, eps: float | None) -> float:
        if eps is None:
            eps = self.rand.randint(1, 20) / 100
        return eps


class OilGenerator(Generator):
    def _gen(
        self, N: int, M: int
    ) -> tuple[list[int], list[list[int]], list[tuple[int, int]]]:
        s = [4] * M
        points = [[0, 0, 0, 1, 1, 0, 1, 1]] * M
        d = [
            (self.rand.randint(0, N - 2), self.rand.randint(0, N - 2)) for _ in range(M)
        ]

        return s, points, d


class ErrorGenerator(Generator):
    def _gen(self, N: int) -> list[float]:
        e = [self.rand.gauss(0, 1) for _ in range(2 * N * N)]
        return e


class InputGenerator(Generator):
    def __init__(self, seed: int | None = None):
        self.seed = seed

    def _gen(
        self, N: int | None = None, M: int | None = None, eps: float | None = None
    ) -> Input:
        N = NGenerator(self.seed)(N)
        M = MGenerator(self.seed)(N, M)
        eps = EpsGenerator(self.seed)(eps)
        s, points, d = OilGenerator(self.seed)(N, M)
        e = ErrorGenerator(self.seed)(N)

        return Input(
            N=N,
            M=M,
            eps=eps,
            s=s,
            points=points,
            d=d,
            e=e,
        )


def gen_input(
    seed: int, N: int | None = None, M: int | None = None, eps: int | None = None
) -> Input:
    return InputGenerator(seed)(N, M, eps)
