from pydantic import BaseModel

from ..interface.io import IInput, IOutput


class Query(IOutput):
    n: int
    points: list[int]

    def __str__(self) -> str:
        s = f"q {self.n} " + " ".join(map(str, self.points))
        return s

    def __post_init__(self):
        if self.n + self.n != len(self.points):
            raise ValueError(f"{2*self.n=} != {len(self.points)=}")

    def from_str(self, s: str) -> "Query":
        int_list = list(map(int, s[2:].split()))
        n = int_list[0]
        points = int_list[1:]
        return Query(n, points)


class Answer(IOutput):
    n: int
    points: list[int]

    def __str__(self) -> str:
        s = f"a {self.n} " + " ".join(map(str, self.points))
        return s

    def __post_init__(self):
        if self.n + self.n != len(self.points):
            raise ValueError(f"{2*self.n=} != {len(self.points)=}")

    def from_str(self, s: str) -> "Answer":
        int_list = list(map(int, s[2:].split()))
        n = int_list[0]
        points = int_list[1:]
        return Answer(n, points)


class Output(BaseModel):
    query: list[Query | Answer]

    def __str__(self) -> str:
        s = "\n".join(map(str, self.query))
        return s


class Input(IInput):
    N: int
    M: int
    eps: float
    s: list[int]
    points: list[list[int]]
    d: list[tuple[int, int]]
    e: list[float]

    def get_ground_truth(self) -> list[list[int]]:
        grid = [[0] * self.N for _ in range(self.N)]

        for i in range(self.M):
            dx, dy = self.d[i]
            for j in range(self.s[i]):
                x, y = self.points[i][2 * j], self.points[i][2 * j + 1]
                grid[x + dx][y + dy] += 1

        return grid

    def get_correct_answer(self) -> Answer:
        correct_answer = []
        grid = self.get_ground_truth()
        for i in range(self.N):
            for j in range(self.N):
                if grid[i][j] > 0:
                    correct_answer.append(i)
                    correct_answer.append(j)
        n = len(correct_answer) // 2
        return Answer(n=n, points=correct_answer)

    def to_query(self, i: int) -> Query:
        dx, dy = self.d[i]
        n = self.s[i]
        points = []
        for j in range(n):
            x, y = self.points[i][2 * j], self.points[i][2 * j + 1]
            points.append(x + dx)
            points.append(y + dy)
        return Query(n=n, points=points)

    def __str__(self):
        s = f"{self.N} {self.M} {self.eps}\n"
        for i in range(self.M):
            str_oil = f"{self.s[i]}"
            for j in range(2 * self.s[i]):
                str_oil += f" {self.points[i][j]}"
            str_oil += "\n"
            s += str_oil

        for i in range(self.M):
            s += f"{self.d[i][0]} {self.d[i][1]}\n"

        for row in self.get_ground_truth():
            s += " ".join(map(str, row)) + "\n"

        for i in range(self.N * self.N * 2):
            s += f"{self.e[i]}\n"

        return s
