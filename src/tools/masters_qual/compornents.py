from dash import Input, Output, callback, dcc, html

from .generator import gen_input
from .visualizer import get_input_visualizer


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


def get_input_graph() -> dcc.Loading:
    return dcc.Loading(dcc.Graph(id="graph"), type="cube")


def get_output_graph() -> dcc.Loading:
    return dcc.Loading(dcc.Graph(id="output_graph"), type="cube")


def get_compornent() -> html.Div:
    return html.Div(
        [
            get_title(),
            get_parameter_div(),
            get_input_textarea_div(),
            get_output_textarea_div(),
            get_input_graph(),
            get_output_graph(),
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


# @callback(
#     Output("output_graph", "figure"),
#     Input("output", "value"),
# )
# def visualize_output(output: str):
#     import plotly.graph_objects as go

#     fig = go.Figure()
#     return fig
