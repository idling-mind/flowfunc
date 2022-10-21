from enum import Enum
from typing import Any, Literal, Union, Tuple
from dash import html, dcc
import plotly.express as px
import pandas as pd
import numpy as np
import asyncio
import time
import dash


def add(item1: Any, item2: Any) -> Any:
    """Add two objects"""
    return item1 + item2


def enter_string(in_string:str) -> str:
    """Enter a string"""
    return in_string


def enter_integer(in_int: int) -> int:
    """Enter an integer"""
    return in_int


def multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Multiply two numbers"""
    return a * b


def convert_to_string(obj):
    """Convert any object to string"""
    return str(obj)


def dataframe_to_datatable(df: pd.DataFrame):
    """Convert dataframe to a dash datatable so that it can be displayed

    Parameters
    ----------
    df: dataframe
        Dataframe

    Returns
    -------
    Datatable : object
        Dash datatable
    """
    ddf = df.copy()
    if isinstance(ddf.columns[0], tuple):
        ddf.columns = [".".join(x) for x in df.columns.tolist()]  # For multiindex columns
    from dash import dash_table

    return dash_table.DataTable(
        id="table",
        columns=[{"name":col, "id": col} for col in ddf.columns.tolist()],
        data=ddf.to_dict("records"),
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


class DataFileType(Enum):
    csv = "csv"
    excel = "excel"

def read_dataframe(url: str, data_type: DataFileType, separator: str) -> pd.DataFrame:
    """Read a dataframe"""
    if data_type.value == "csv":
        return pd.read_csv(url, sep=separator)
    elif data_type.value == "excel":
        return pd.read_excel(url)
    return pd.read_table(url)

def iris_dataset() -> pd.DataFrame:
    """Iris data as a dataframe"""
    return read_dataframe(
        "https://gist.github.com/netj/8836201/raw/6f9306ad21398ea43cba4f7d537619d0e07d5ae3/iris.csv",
        DataFileType.csv,
        ","
    )

def titanic_dataset() -> pd.DataFrame:
    """Titanic data as a dataframe"""
    return read_dataframe(
        "https://github.com/datasciencedojo/datasets/raw/master/titanic.csv",
        DataFileType.csv,
        ","
    )

def scatter_plot(df: pd.DataFrame, x: str, y: str) -> dcc.Graph:
    """Create a scatter plot from a dataframe"""
    return dcc.Graph(figure=px.scatter(df, x=x, y=y))

all_functions = [
    add,
    enter_string,
    enter_integer,
    multiply,
    convert_to_string,
    dataframe_to_datatable,
    convert_to_markdown,
    read_dataframe,
    display,
    scatter_plot,
    iris_dataset,
    titanic_dataset,
]
