import math

import plotly.graph_objects as go

from .evaluator import evaluate_grid
from .io import Input, Output


def int_to_color(a: int, N: int) -> str:
    rate = a / N
    r = 255 * rate
    g = 255 * rate
    b = 255 * rate
    return f"rgb({r}, {g}, {b})"


def add_grid(fig: go.Figure, input: Input) -> go.Figure:
    N = input.N
    for i in range(N - 1):
        fig.add_vline(x=i + 1, opacity=0.2)
        fig.add_hline(y=i + 1, opacity=0.2)
    return fig


def add_wall(fig: go.Figure, input: Input) -> go.Figure:
    N = input.N
    for i in range(N):
        for j in range(N - 1):
            vij = input.v[i][j]
            if vij == 0:
                continue
            fig.add_trace(
                go.Scatter(
                    x=[j + 1, j + 1],
                    y=[i, i + 1],
                    mode="lines",
                    line=dict(color="black", width=5),
                    hoverinfo="skip",
                )
            )

    for i in range(N - 1):
        for j in range(N):
            hij = input.h[i][j]
            if hij == 0:
                continue
            fig.add_trace(
                go.Scatter(
                    x=[j, j + 1],
                    y=[i + 1, i + 1],
                    mode="lines",
                    line=dict(color="black", width=5),
                    hoverinfo="skip",
                )
            )

    return fig


def add_number(fig: go.Figure, a: list[list[int]]) -> go.Figure:
    N = len(a)
    N2 = N * N
    for i in range(N):
        for j in range(N):
            aij = a[i][j]
            color = int_to_color(aij, N2)
            fig.add_trace(
                go.Scatter(
                    x=[j, j, j + 1, j + 1],
                    y=[i, i + 1, i + 1, i],
                    mode="lines",
                    line=dict(color=color, width=0),
                    fill="toself",
                    hoverinfo="skip",
                )
            )
    return fig


def update_layout(fig: go.Figure, N: int) -> go.Figure:
    max_size = 1500
    width = max_size * (N / 100) * math.exp(1 - N / 100)
    height = max_size * (N / 100) * math.exp(1 - N / 100)
    fig.update_layout(width=width, height=height, showlegend=False)
    fig.update_xaxes(range=(0, N))
    fig.update_yaxes(range=(N, 0))
    return fig


def get_input_visualizer(input: Input) -> go.Figure:
    fig = go.Figure()

    fig = add_number(fig, input.a)
    fig = add_wall(fig, input)

    fig = add_grid(fig, input)
    fig = update_layout(fig, input.N)

    score = evaluate_grid(input, input.a)
    fig.update_layout(title=dict(text=f"{score=}"))
    return fig


def add_path(fig: go.Figure, path: list[tuple[int, int]], color: str) -> go.Figure:
    ox = 1 / 3
    oy = 2 / 3
    if color == "blue":
        ox = 2 / 3
        oy = 1 / 3

    fig.add_trace(
        go.Scatter(
            x=[path[0][1] + ox],
            y=[path[0][0] + oy],
            marker=dict(color=color, size=5),
        )
    )

    x = [xi + oy for xi, _ in path]
    y = [yi + ox for _, yi in path]
    fig.add_trace(
        go.Scatter(
            x=y,
            y=x,
            mode="lines",
            line=dict(width=1, color=color),
        )
    )

    return fig


def get_output_visualizer(input: Input, output: Output) -> go.Figure:
    a = output.get_grid(input)
    fig = go.Figure()

    fig = add_number(fig, a)
    fig = add_wall(fig, input)

    fig = add_grid(fig, input)
    fig = update_layout(fig, input.N)
    score = evaluate_grid(input, a)
    fig.update_layout(title=dict(text=f"{score=}"))

    add_path(fig, output.get_taka_path(), color="red")
    add_path(fig, output.get_aoki_path(), color="blue")
    return fig
