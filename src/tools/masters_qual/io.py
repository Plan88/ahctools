from ..interface.io import IInput, IOutput
from .domain import Tile, TileType


class Input(IInput):
    si: int
    sj: int
    t: list[list[int]]
    p: list[list[int]]

    def from_str(s: str) -> "Input":
        lines = s.split("\n")

        si, sj = map(int, lines[0].split())

        t = []
        for i in range(1, 51):
            t.append(list(map(int, lines[i].split())))

        p = []
        for i in range(51, 101):
            p.append(list(map(int, lines[i].split())))

        return Input(si=si, sj=sj, t=t, p=p)

    def __str__(self) -> str:
        s = ""
        s += f"{self.si} {self.sj}\n"

        def to_str_line(t: list[int]) -> str:
            t_str = map(str, t)
            return " ".join(t_str) + "\n"

        for ti in self.t:
            s += to_str_line(ti)
        for pi in self.p:
            s += to_str_line(pi)

        return s


class Output(IOutput):
    s: str

    def from_str(s: str) -> "Output":
        return Output(s=s)


def get_tile_infos(input: Input) -> list[Tile]:
    N = 50
    M = N * N

    used = [False] * M
    tiles = [None] * M

    for i in range(N):
        for j in range(N):
            tij = input.t[i][j]
            if used[tij]:
                continue

            used[tij] = True

            score = input.p[i][j]
            tile_type = TileType.one

            if i < N - 1 and input.t[i + 1][j] == tij:
                used[input.t[i + 1][j]] = True
                score = (score, input.p[i + 1][j])
                tile_type = TileType.tate
            elif j < N - 1 and input.t[i][j + 1] == tij:
                used[input.t[i][j + 1]] = True
                score = (score, input.p[i][j + 1])
                tile_type = TileType.yoko

            tiles[tij] = Tile(tile_type=tile_type, score=score, pos=(i, j))

    while tiles[-1] is None:
        tiles.pop()

    return tiles
