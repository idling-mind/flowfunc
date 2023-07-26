from time import sleep
from typing import Literal, Union, Tuple, NewType
from dash import html, dcc
import plotly.express as px
import pandas as pd
import numpy as np
import asyncio
import dash
from flowfunc.types import date, time, month, color, week
from dataclasses import dataclass


async def add_async(number1: int, number2: int) -> int:
    """Add Numbers"""
    sleeptime = np.random.randint(0, 5)
    print(f"sleeping for {sleeptime}")
    await asyncio.sleep(sleeptime)
    return number1 + number2


def add_sync(number1: Union[int, float], number2: int) -> int:
    """Add Numbers

    Add two numbers together

    Parameters
    ----------
    number1 : float
        Number1
    number2: float
        Number2

    Returns
    -------
    number: float
        Sum
    """
    return number1 + number2


def add_same_objects(object1, object2):
    """Add Objects

    Add any two objects of the same type

    Parameters
    ----------
    object1: object
        First Object
    object2: object
        Second Object

    Returns
    -------
    combined_object: object
        Combined Object
    """
    return object1 + object2


def enter_string(in_string:str) -> str:
    """String"""
    return in_string


def enter_integer(in_int: int) -> int:
    """String"""
    return in_int


def multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Multiply Numbers"""
    return a * b


def sum(list_of_items: list) -> Union[float, int, str]:
    return sum(list_of_items)

def convert_to_string(obj):
    """Convert to string

    Convert any object to string

    Parameters
    ----------
    obj: object
        Object to convert

    Returns
    -------
    string: str
        String output
    """
    return str(obj)


def dataframe_to_datatable(df: pd.DataFrame):
    """Convert dataframe to a dash datatable

    Parameters
    ----------
    df: dataframe
        Dataframe

    Returns
    -------
    Datatable : object
        Dash datatable
    """
    from dash import dash_table

    return dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
    )


def convert_to_markdown(markdown: str):
    """Display Markdown

    Display markdown in the dash app

    Parameters
    ----------
    markdown: str
        Markdown to display

    Returns
    -------
    markdown: object
        Dash markdown object
    """
    return dash.dcc.Markdown(markdown)

def display(output1, output2="", output3="", output4="", output5=""):
    """Display outputs"""
    return html.Div([output1, output2, output3, output4, output5])

def read_dataframe(url: str, data_type: Literal["csv", "excel"], separator: str) -> pd.DataFrame:
    """Read a dataframe"""
    if data_type == "csv":
        return pd.read_csv(url, sep=separator)
    elif data_type == "excel":
        return pd.read_excel(url)
    return pd.read_table(url)

def scatter_plot(df: pd.DataFrame, x: str, y: str) -> dcc.Graph:
    """Create a scatter plot from a dataframe"""
    return dcc.Graph(figure=px.scatter(df, x=x, y=y))

def custom_controls(m: month, w: week, d: date, t: time, c: color) -> str:
    """Trying custom controls"""
    out = ""
    for item in [m, w, d, t, c]:
        out += f"{item} ({type(item)})\n"
    return out.strip()

@dataclass
class vector:
    x: int
    y: int
    z: int

    def magnitude(self):
        return (self.x **2 + self.y**2 + self.z **2)**0.5

def get_vector_magnitude(v: vector):
    """Using dataclass as a port with multiple controls"""
    return v.magnitude()

all_functions = [
    add_async,
    add_sync,
    enter_string,
    enter_integer,
    add_same_objects,
    convert_to_string,
    dataframe_to_datatable,
    convert_to_markdown,
    read_dataframe,
    display,
    scatter_plot,
    custom_controls,
    get_vector_magnitude,
]
