import datetime
from typing import NewType
from uuid import uuid4

import dash
from dash import Input, Output, State, html
from dash_flume import DashFlume, config, jobrunner
from dash_flume.models import OutConnections, OutNode
from yaml import safe_load

date = NewType("date", str)


def enter_date(d: date) -> str:
    return d


def enter_string(input_string: str) -> str:
    return input_string


def get_month_from_date(d: datetime.date):
    return d.month


def add(a, b):
    """Add two numbers

    Parameters
    ----------
    a: int
        First number
    b: int
        Second number

    Returns
    -------
    Sum: int
        Sum of numbers
    """
    return a + b


def subtract(a, b):
    """Subtract one number from another

    Parameters
    ----------
    a: int
        First number
    b: int
        Number to subtract from first number

    Returns
    -------
    Difference: int
        Difference of a and b
    """
    return a - b


flist = [add, subtract, safe_load, enter_date, enter_string, get_month_from_date]
app = dash.Dash(__name__)
fconfig = config.Config.from_function_list(flist)
runner = jobrunner.JobRunner(fconfig)

app.layout = html.Div(
    [
        html.Button(id="btn_run", children=["Run"]),
        html.Button(id="btn_addnode", children=["Add a node"]),
        html.Div(
            DashFlume(
                id="someid",
                config=fconfig.config_dict(),
                disableZoom=True,
                duck_type=True,
            ),
            style={"height": "600px", "width": "100%"},
        ),
        html.Div(id="output"),
    ]
)


@app.callback(
    Output("output", "children"),
    Input("btn_run", "n_clicks"),
    State("someid", "nodes"),
)
def run(nclicks, nodes):
    if not nodes:
        return
    output = runner.run(nodes)
    output_html = []
    for node in output.values():
        output_html.append(html.Div(f"{node.type}: {node.value}"))
        if node.error:
            output_html.append(html.Div(f"{node.error}"))
    return output_html


@app.callback(
    [Output("someid", "nodes"), Output("someid", "editor_status")],
    Input("btn_addnode", "n_clicks"),
    State("someid", "nodes"),
)
def add_node(nclicks, nodes):
    if not nodes:
        nodes = {}
    node_id = str(uuid4())
    nodes[node_id] = OutNode(
        id=node_id,
        x=0,
        y=0,
        width=150,
        type="__main__.add",
        connections=OutConnections(inputs={}, outputs={}),
        inputData={},
    ).dict()
    return nodes, "server"


if __name__ == "__main__":
    app.run_server(debug=True)
