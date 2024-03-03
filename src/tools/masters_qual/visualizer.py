import plotly.graph_objects as go

from .io import Input, Output


def int_to_color(a: int, N: int) -> str:
    rate = a / N
    r = 255 * rate
    b = 255 * (1 - rate)
    return f"rgb({r}, 0, {b})"


def get_input_visualizer(input: Input) -> go.Figure:
    fig = go.Figure()

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
                    marker=dict(color="black"),
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
                    marker=dict(color="black"),
                    hoverinfo="skip",
                )
            )

    N2 = N * N
    for i in range(N):
        for j in range(N):
            aij = input.a[i][j]
            color = int_to_color(aij, N2)
            fig.add_trace(
                go.Scatter(
                    x=[j, j, j + 1, j + 1],
                    y=[i, i + 1, i + 1, i],
                    mode="lines",
                    line=dict(color=color, width=0),
                    fill="toself",
                )
            )

    for i in range(N - 1):
        fig.add_vline(x=i + 1, opacity=0.2)
        fig.add_hline(y=i + 1, opacity=0.2)
    fig.update_layout(width=500, height=500, showlegend=False)
    fig.update_xaxes(range=(0, N))
    fig.update_yaxes(range=(N, 0))
    return fig
