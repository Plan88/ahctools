from .io import Input, Output, Query, Answer
import math


class Solver:
    def __init__(self, input: Input):
        self.input = input
        self.queries = []
        self.query_manager = QueryManager(input)

    def solve(self) -> Output:
        for i in range(self.input.M):
            q = self.input.to_query(i)
            self.query(q)
        self.answer(self.input.get_correct_answer())
        return Output(query=self.queries)

    def query(self, q: Query) -> int:
        self.queries.append(q)
        return self.query_manager.query(q)

    def answer(self, a: Answer) -> int:
        self.queries.append(a)
        return self.query_manager.answer(a)


class QueryManager:
    def __init__(self, input: Input):
        self.input = input
        self.grid = input.get_ground_truth()
        self.num_query = 0

    def query(self, q: Query) -> int:
        if q.n == 1:
            return self.get_vS(q)

        vS = self.get_vS(q)
        mean = self.get_mean(q, vS)
        std = math.sqrt(self.get_var(q))
        smp = self.input.e[self.num_query]
        self.num_query += 1

        return max(0, int(round(mean + std * smp)))

    def answer(self, a: Answer) -> int:
        return 1

    def get_vS(self, q: Query) -> int:
        vS = 0
        for i in range(q.n):
            x, y = q.points[2 * i], q.points[2 * i + 1]
            vS += self.grid[x][y]
        return vS

    def get_mean(self, q: Query, vS: int) -> float:
        k = q.n
        eps = self.input.eps
        mean = (k - vS) * eps + vS * (1 - eps)
        return mean

    def get_var(self, q: Query) -> float:
        k = q.n
        eps = self.input.eps
        var = k * eps * (1 - eps)
        return var


def solve(input: Input) -> Output:
    solver = Solver(input)
    return solver.solve()
