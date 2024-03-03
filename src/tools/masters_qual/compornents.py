from dash import Input, Output, State, callback, dcc, html

from .generator import gen_input
from .io import Input as Input2
from .visualizer import get_input_visualizer, get_output_visualizer


def get_title() -> html.H1:
    return html.H1("Visualizer for masters-qual")


def get_parameter_div() -> html.Div:
    return html.Div(
        [
            "Seed:",
            dcc.Input(type="number", min=0, max=99, value=0, id="seed"),
        ]
    )


def get_input_textarea_div() -> html.Div:
    return html.Div(
        [
            html.P("Input:"),
            dcc.Textarea(
                placeholder="input",
                readOnly=True,
                id="input",
                style={"width": "50%", "height": 200},
            ),
        ]
    )


def get_output_textarea_div() -> html.Div:
    return html.Div(
        [
            html.P("Output:"),
            dcc.Textarea(
                placeholder="output", id="output", style={"width": "50%", "height": 200}
            ),
        ]
    )


def get_graph(id: str = "graph") -> dcc.Loading:
    return dcc.Loading(dcc.Graph(id=id), type="cube")


def get_compornent() -> html.Div:
    return html.Div(
        [
            get_title(),
            get_parameter_div(),
            get_input_textarea_div(),
            get_output_textarea_div(),
            get_graph(),
            get_graph(id="graph2"),
        ]
    )


@callback(
    Output("input", "value"),
    Output("graph", "figure"),
    Input("seed", "value"),
)
def visualize_input(seed: int):
    input = gen_input(seed=seed)

    try:
        fig = get_input_visualizer(input=input)
    except Exception as e:
        print(e)
        import plotly.graph_objects as go

        fig = go.Figure()
    return str(input), fig


@callback(
    Output("graph2", "figure"),
    Input("output", "value"),
    State("input", "value"),
)
def visualize_output(output: str, input: str):
    input = Input2.from_str(input)

    a = []
    for ai in output.split("\n"):
        if ai == "":
            continue
        a.append(list(map(int, ai.split())))

    fig = get_output_visualizer(input, a)
    return fig
