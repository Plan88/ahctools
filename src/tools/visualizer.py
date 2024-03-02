import plotly.graph_objects as go

from .io import Answer, Input, Output, Query


def parse_output(s: str) -> Output:
    query = []

    for q in s.split("\n"):
        if q[0] == "q":
            query.append(Query.from_str(q))
        elif q[0] == "a":
            query.append(Answer.from_str(q))
        elif q[:2] == "#c":
            pass
        elif q == "":
            continue
        else:
            raise ValueError(f"invalid output, {q=}")

    return Output(query)


def get_visualizer(input: Input, output: Output):
    fig_dict = {"data": [], "frames": []}
    duration = 100

    menu_dict = get_menu_dict(duration)
    sliders_dict = get_sliders_dict(duration)

    n = input.N

    # make data
    fig_dict["data"] = get_frame(n)

    # make frame
    for i, q in enumerate(output.query):
        frame = {
            "data": get_frame(n, q),
            "name": i,
        }
        fig_dict["frames"].append(frame)

        slider_step = {
            "args": [
                [i],
                {
                    "frame": {"duration": duration, "redraw": False},
                    "mode": "immediate",
                    "transition": {"duration": duration},
                },
            ],
            "label": i + 1,
            "method": "animate",
        }
        sliders_dict["steps"].append(slider_step)

    fig = go.Figure(fig_dict)
    fig.update_layout(
        width=600,
        height=600,
        sliders=[sliders_dict],
        xaxis=dict(range=(0, n)),
        yaxis=dict(range=(n, 0)),
        updatemenus=[menu_dict],
        showlegend=False,
    )

    fig = add_initial_data(fig, input)

    return fig


def add_initial_data(fig: go.Figure, input: Input) -> go.Figure:
    n = input.N

    # draw line
    for i in range(n + 1):
        fig.add_hline(y=i)
        fig.add_vline(x=i)

    # display oil
    grid = input.get_ground_truth()
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                continue
            v = grid[i][j]
            fig.add_annotation(
                x=j + 0.5, y=i + 0.5, text=f"{v}", opacity=0.5, showarrow=False
            )

    return fig


def get_frame(n: int, q: Query | Answer | None = None) -> list:
    data = []
    for i in range(n):
        for j in range(n):
            data.append(get_rectangle(i, j))

    if q is not None:
        color = "red"
        if isinstance(q, Answer):
            color = "blue"
        for i in range(q.n):
            x, y = q.points[2 * i], q.points[2 * i + 1]
            data[x * n + y] = get_rectangle(x, y, color=color, opacity=0.5)

    return data


def get_rectangle(x: int, y: int, color: str = "red", **kwargs) -> go.Scatter:
    if "opacity" not in kwargs:
        kwargs["opacity"] = 0.0

    return go.Scatter(
        x=[y, y, y + 1, y + 1],
        y=[x, x + 1, x + 1, x],
        mode="lines",
        line=dict(width=0.0, color=color),
        fill="toself",
        **kwargs,
    )


def get_menu_dict(duration: int = 200) -> dict:
    menu_dict = {
        "buttons": [
            {
                "args": [
                    None,
                    {
                        "frame": {"duration": duration, "redraw": False},
                        "fromcurrent": True,
                        "transition": {
                            "duration": duration,
                            "easing": "quadratic-in-out",
                        },
                    },
                ],
                "label": "Play",
                "method": "animate",
            },
            {
                "args": [
                    [None],
                    {
                        "frame": {"duration": duration, "redraw": False},
                        "mode": "immediate",
                        "transition": {"duration": 0},
                    },
                ],
                "label": "Pause",
                "method": "animate",
            },
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top",
    }
    return menu_dict


def get_sliders_dict(duration: int = 200) -> dict:
    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Query No:",
            "visible": True,
            "xanchor": "right",
        },
        "transition": {"duration": duration, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": [],
    }
    return sliders_dict
