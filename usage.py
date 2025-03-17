import math
from typing import Annotated, Literal
import dash
from dash import Input, Output, State, html
from flowfunc import Flowfunc, config, jobrunner
from enum import Enum

def add(a: int, b: int):
    """Add two numbers"""
    return a + b


def subtract(
    a: Annotated[int | float, {"label": "First number"}],
    b: Annotated[int | float, {"label": "Second number"}],
):
    """Subtract one number from another"""
    return a - b

class MathFunction(str, Enum):
    sin = "sin"
    cos = "cos"
    tan = "tan"
    asin = "asin"
    acos = "acos"
    atan = "atan"


def trig_function(
    x: float, func: Annotated[MathFunction, {"label": "Function", "hidePort": True}]
):
    """Trigonometric function"""
    return getattr(math, func)(x)


flist = [
    add,
    subtract,
    trig_function,
]
app = dash.Dash(__name__)
fconfig = config.Config.from_function_list(flist)
runner = jobrunner.JobRunner(fconfig)

app.layout = html.Div(
    [
        html.Button(id="btn_run", children=["Run"]),
        html.Div(
            Flowfunc(
                id="nodeeditor",
                config=fconfig.dict(),
                disable_zoom=True,
                type_safety=False,
            ),
            style={"height": "500px", "width": "100%"},
        ),
        html.Div(id="output"),
    ]
)


@app.callback(
    [Output("output", "children"), Output("nodeeditor", "nodes_status")],
    Input("btn_run", "n_clicks"),
    State("nodeeditor", "nodes"),
)
def run(nclicks, nodes):
    if not nodes:
        return [], {}
    output = runner.run(nodes)
    output_html = []
    nodes_status = {}
    for node in output.values():
        output_html.append(html.Div(f"{node.type}: {node.result}"))
        if node.error:
            output_html.append(html.Div(f"{node.error}"))
        nodes_status[node.id] = node.status
    return output_html, nodes_status


if __name__ == "__main__":
    app.run_server(debug=True)
