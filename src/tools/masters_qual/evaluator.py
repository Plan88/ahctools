import math

from ..interface.evaluator import IEvaluator
from .io import Input, Output


class Evaluator(IEvaluator):
    def evaluate(self, output: Output) -> float:
        D = evaluate_grid(self.input, self.input.a)
        D2 = evaluate_grid(self.input, output.get_grid(self.input))

        score = max(1.0, round(1_000_000 * math.log2(D2 / D)))
        return score


def evaluate_grid(input: Input, a: list[list[int]]) -> int:
    N = input.N
    score = 0

    for i in range(N):
        for j in range(N - 1):
            if input.v[i][j]:
                continue
            diff = a[i][j] - a[i][j + 1]
            score += diff * diff

    for i in range(N - 1):
        for j in range(N):
            if input.h[i][j]:
                continue
            diff = a[i][j] - a[i + 1][j]
            score += diff * diff

    return score