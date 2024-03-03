from ..interface.io import IInput, IOutput


class Input(IInput):
    t: int
    N: int
    v: list[list[int]]
    h: list[list[int]]
    a: list[list[int]]

    def from_str(s: str) -> "Input":
        lines = s.split("\n")

        t, N = map(int, lines[0].split())

        vl, vr = 1, N + 1
        hl, hr = vr, vr + N - 1
        al, ar = hr, hr + N

        v = []
        for i in range(vl, vr):
            v.append(list(map(int, lines[i])))

        h = []
        for i in range(hl, hr):
            h.append(list(map(int, lines[i])))

        a = []
        for i in range(al, ar):
            a.append(list(map(int, lines[i].split())))
        return Input(t=t, N=N, v=v, h=h, a=a)

    def __str__(self) -> str:
        s = ""
        s += f"{self.t} {self.N}\n"

        def to_str_line(t: list[int], delimiter: str = " ") -> str:
            t_str = map(str, t)
            return delimiter.join(t_str) + "\n"

        for vi in self.v:
            s += to_str_line(vi, "")
        for hi in self.h:
            s += to_str_line(hi, "")
        for ai in self.a:
            s += to_str_line(ai)

        return s


class Output(IOutput):
    pi: int
    pj: int
    qi: int
    qj: int
    actions: list[tuple[int, str, str]]

    def from_str(s: str) -> "Output":
        lines = s.split("\n")
        pi, pj, qi, qj = map(int, lines[0].split())

        actions = []
        for line in lines[1:]:
            if line == "":
                continue

            s, d, e = line.split()
            s = int(s)

            actions.append((s, d, e))
        return Output(pi=pi, pj=pj, qi=qi, qj=qj, actions=actions)

    def get_taka_path(self) -> list[tuple[int, int]]:
        d = [c for _, c, _ in self.actions]
        return self.get_path(self.pi, self.pj, d)

    def get_aoki_path(self) -> list[tuple[int, int]]:
        d = [c for _, _, c in self.actions]
        return self.get_path(self.qi, self.qj, d)

    def get_path(self, x: int, y: int, d: list[str]) -> list[tuple[int, int]]:
        path = [(x, y)]
        for c in d:
            if c == "L":
                y -= 1
            elif c == "R":
                y += 1
            elif c == "U":
                x -= 1
            elif c == "D":
                x += 1
            path.append((x, y))
        return path

    def get_grid(self, input: Input) -> list[list[int]]:
        a = input.a.copy()

        x1, y1, x2, y2 = self.pi, self.pj, self.qi, self.qj
        for i, action in enumerate(self.actions):
            s, d, e = action

            if s == 1:
                a[x1][y1], a[x2][y2] = a[x2][y2], a[x1][y1]

            if d == "L":
                y1 -= 1
            elif d == "R":
                y1 += 1
            elif d == "U":
                x1 -= 1
            elif d == "D":
                x1 += 1

            if e == "L":
                y2 -= 1
            elif e == "R":
                y2 += 1
            elif e == "U":
                x2 -= 1
            elif e == "D":
                x2 += 1

            if (
                not (0 <= x1 < input.N)
                or not (0 <= x2 <= input.N)
                or not (0 <= y1 <= input.N)
                or not (0 <= y2 < input.N)
            ):
                print(len(self.actions))
                raise Exception(
                    f"Out of Grid, tern {i+1}, pi={x1}, pj={y1}, qi={y1}, qj={y2}"
                )
        return a
