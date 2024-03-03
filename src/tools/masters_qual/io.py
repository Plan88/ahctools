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
    actions: list[tuple[str, str, str]]

    def from_str(s: str) -> "Output":
        lines = s.split("\n")
        pi, pj, qi, qj = map(int, lines[0].split())

        actions = []
        for line in lines:
            if line == "":
                continue

            s, d, e = line.split()
            s = int(s)

            actions.append((s, d, e))
        return Output(pi=pi, pj=pj, qi=qi, qj=qj, actions=actions)

    def get_grid(self, input: Input) -> list[list[int]]:
        a = input.a.copy()

        x1, y1, x2, y2 = self.pi, self.pj, self.qi, self.qj
        for action in self.actions:
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

        return a
