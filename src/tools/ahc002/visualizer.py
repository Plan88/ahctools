import plotly.graph_objects as go

from .io import Input, Output, get_tile_infos


def get_visualizer(input: Input, output: Output) -> go.Figure:
    fig = go.Figure()
    tiles = get_tile_infos(input)

    N = 50
    for i in range(N + 1):
        fig.add_trace(
            go.Scatter(x=[0, N], y=[i, i], mode="lines", marker=dict(color="black"))
        )
        fig.add_trace(
            go.Scatter(x=[i, i], y=[0, N], mode="lines", marker=dict(color="black"))
        )
    for tile in tiles:
        line_info = tile.get_white_line()
        if line_info is None:
            continue
        fig.add_trace(go.Scatter(**line_info, mode="lines", marker=dict(color="white")))

    # for i in range(N):
    #     for j in range(N):
    #         pij = input.p[i][j]
    #         fig.add_annotation(
    #             x=j + 0.5,
    #             y=i + 0.5,
    #             text=pij,
    #             showarrow=False,
    #         )

    def get_next_pos(x: int, y: int, direction: str) -> tuple[int, int]:
        if direction == "L":
            y -= 1
        elif direction == "R":
            y += 1
        elif direction == "U":
            x -= 1
        else:
            x += 1
        return (x, y)

    x, y = input.si, input.sj
    xs = [y + 0.5]
    ys = [x + 0.5]

    for direction in output.s:
        x, y = get_next_pos(x, y, direction)
        xs.append(y + 0.5)
        ys.append(x + 0.5)

    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", marker=dict(color="orange")))

    fig.add_shape(
        type="rect",
        x0=xs[0] - 0.5,
        x1=xs[0] + 0.5,
        y0=ys[0] - 0.5,
        y1=ys[0] + 0.5,
        fillcolor="blue",
        opacity=0.5,
    )
    fig.add_shape(
        type="rect",
        x0=xs[-1] - 0.5,
        x1=xs[-1] + 0.5,
        y0=ys[-1] - 0.5,
        y1=ys[-1] + 0.5,
        fillcolor="red",
        opacity=0.5,
    )

    fig.update_layout(
        height=1200,
        width=1200,
        showlegend=False,
        plot_bgcolor="white",
    )
    fig.update_xaxes(range=(0, N))
    fig.update_yaxes(range=(N, 0))
    return fig
