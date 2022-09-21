from datetime import date
from enum import Enum
from pprint import pprint
from typing import Any, List, Literal, NewType, Union
from uuid import uuid4
from pydantic import BaseModel

import dash
from dash import Input, Output, State, html
from dash_flume import DashFlume, config, jobrunner
from dash_flume.models import (
    ControlType,
    OutConnections,
    OutNode,
    OutNodes,
    Port,
    Control,
)
from yaml import safe_load

test_port = Port(
    type="test_port",
    name="test_port",
    label="test_port",
    controls=[
        Control(type=ControlType.text, name="test_port_string", label="some string"),
        Control(type=ControlType.number, name="test_port_number", label="some number"),
    ],
)
date_port = Port(
    type="date",
    name="date",
    label="date",
    controls=[
        Control(type=ControlType.date, name="date", label="some date"),
    ],
)

city_port = Port(
    type="city",
    name="city",
    label="city",
    controls=[
        Control(
            type=ControlType.select,
            name="name",
            label="Select a city",
            options=[
                {"label": "Gothenburg", "value": "Gothenburg"},
                {"label": "Stockholm", "value": "Stockholm"},
                {"label": "Malmo", "value": "Malmo"},
            ],
        ),
        Control(type=ControlType.number, name="pin", label="Pin"),
    ],
)

n = NewType("test_port", Any)


class town(BaseModel):
    name: str
    pin: int
    established_date: date
    zone: Literal["Zone1", "Zone2", "Zone3"]
    extra_zone: List[Literal["Zone1", "Zone2", "Zone3"]]


def enter_date(d: date) -> str:
    return str(d)


def enter_city_and_pin(city: town):
    """Enter a city and a PIN"""
    return city


class AggOption(Enum):
    Min = 1
    Max = 2
    Mean = 3
    SomethingElse = 4


def aggregate_option(
    # agg: List[Literal["min", "max", "mean", "count"]],
    egg: AggOption,
    # beg: List[AggOption],
) -> str:
    return egg.value


def test_port_node(input: n):
    return input


def enter_string(input_string: str) -> str:
    return input_string


def get_month_from_date(d: date):
    return d.month


def add(a: Union[int, float], b: Union[int, float]):
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


def subtract(a: Union[int, float], b: Union[int, float]):
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


flist = [
    add,
    subtract,
    safe_load,
    enter_date,
    enter_string,
    get_month_from_date,
    test_port_node,
    enter_city_and_pin,
    aggregate_option,
]
app = dash.Dash(__name__)
fconfig = config.Config.from_function_list(
    flist, extra_ports=[test_port, city_port, date_port]
)
# pprint(fconfig.dict())
runner = jobrunner.JobRunner(fconfig)

app.layout = html.Div(
    [
        html.Button(id="btn_run", children=["Run"]),
        html.Button(id="btn_addnode", children=["Add a node"]),
        html.Div(
            DashFlume(
                id="someid",
                config=fconfig.dict(),
                disable_zoom=True,
                type_safety=False,
            ),
            style={"height": "600px", "width": "100%"},
        ),
        html.Div(id="output"),
    ]
)


@app.callback(
    [Output("output", "children"), Output("someid", "nodes_status")],
    Input("btn_run", "n_clicks"),
    State("someid", "nodes"),
    State("someid", "comments"),
)
def run(nclicks, nodes, comments):
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
