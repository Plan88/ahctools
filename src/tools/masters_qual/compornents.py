from dash import Input, Output, callback, dcc, html

from .generator import gen_input
from .io import Output as Output2
from .visualizer import get_visualizer


def get_title() -> html.H1:
    return html.H1("Visualizer")


def get_parameter_div() -> html.Div:
    return html.Div(
        [
            "Seed:",
            dcc.Input(type="number", min=0, max=9, value=0, id="seed"),
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


def get_graph() -> dcc.Loading:
    return dcc.Loading(dcc.Graph(id="graph"), type="cube")


def get_compornent() -> html.Div:
    return html.Div(
        [
            get_title(),
            get_parameter_div(),
            get_input_textarea_div(),
            get_output_textarea_div(),
            get_graph(),
        ]
    )


@callback(
    Output("input", "value"),
    Output("graph", "figure"),
    Input("seed", "value"),
    Input("output", "value"),
)
def visualize(seed: int, output: str):
    input = gen_input(seed=seed)
    if output is None:
        output = ""
    output = Output2.from_str(output)

    try:
        fig = get_visualizer(input=input, output=output)
    except Exception as e:
        print(e)
        import plotly.graph_objects as go

        fig = go.Figure()
    return str(input), fig
