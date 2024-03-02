from dash import Input, Output, callback, dcc, html

from .generator import gen_input
from .solver import solve
from .visualizer import get_visualizer


def get_title() -> html.H1:
    return html.H1("Visualizer")


def get_parameter_div() -> html.Div:
    return html.Div(
        [
            "Seed:",
            dcc.Input(type="number", min=0, value=0, id="seed"),
            " N:",
            dcc.Input(type="number", min=10, value=10, id="N"),
            " M:",
            dcc.Input(type="number", min=2, value=2, id="M"),
            " eps:",
            dcc.Input(
                type="number", min=0.01, max=0.2, step=0.01, value=0.01, id="eps"
            ),
            dcc.Checklist(["fix N", "fix M", "fix eps"], id="fix", value=[]),
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


@callback(
    Output("N", "disabled"),
    Output("M", "disabled"),
    Output("eps", "disabled"),
    Input("fix", "value"),
)
def fix_input(value):
    updated = ["fix N" not in value, "fix M" not in value, "fix eps" not in value]
    return updated


@callback(
    Output("input", "value"),
    Output("output", "value"),
    Output("graph", "figure"),
    Input("seed", "value"),
    Input("N", "value"),
    Input("M", "value"),
    Input("eps", "value"),
    Input("fix", "value"),
)
def print_input(seed: int, N: int, M: int, eps: float, fix_flags: list[bool]):
    fN, fM, feps = "fix N" in fix_flags, "fix M" in fix_flags, "fix eps" in fix_flags

    if not fN:
        N = None
    if not fM:
        M = None
    if not feps:
        eps = None

    input = gen_input(seed, N, M, eps)
    output = solve(input)
    fig = get_visualizer(input, output)
    return str(input), str(output), fig


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
