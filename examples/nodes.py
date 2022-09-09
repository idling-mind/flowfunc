from typing import Union, Tuple
import pandas as pd
import numpy as np
import asyncio
import time
import dash


async def add_async(number1: Union[int, float], number2: int) -> int:
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
    sleeptime = np.random.randint(0, 10)
    print(f"sleeping for {sleeptime}")
    await asyncio.sleep(sleeptime)
    return number1 + number2


async def add_async_win(number1: Union[int, float], number2: int) -> int:
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
    sleeptime = np.random.randint(0, 10)
    print(f"sleeping for {sleeptime} in windows")
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
    sleeptime = np.random.randint(0, 10)
    print(f"sleeping for {sleeptime}")
    time.sleep(sleeptime)
    return number1 + number2


def junk(abc, xyz: Union[str, int, float]) -> Tuple[str, int]:
    return "hey", 3223


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


def create_file(filepath, filetext):
    """Create File

    Create a file and writes a text and a number to it

    Parameters
    ----------
    filepath : str
        Path to the file
    filetext : str
        Text to write to the file
    """
    with open(filepath, "w") as f:
        f.write(filetext)


def enter_string(in_string):
    """String

    Input a string

    Parameters
    ----------
    in_string: str
        Input String
        {"hidePort": true}

    Returns
    -------
    string: str
        Entered String
    """
    return in_string


def enter_number(in_int):
    """String

    Input a string

    Parameters
    ----------
    in_int: int
        Input Number
        {"hidePort": true}

    Returns
    -------
    number: int
        Entered Number
    """
    return in_int


def multiply(**kwargs):
    """Multiply Numbers

    Multiply two numbers

    Parameters
    ----------
    number1 : float
        Number1
    number2: float
        Number2

    Returns
    -------
    number: float
        Product
    """
    return kwargs.get("number1") * kwargs.get("number2")


def sum(list_of_items: list) -> Union[float, int, str]:
    return sum(list_of_items)


def shaderman(shade1, color):
    """Shader control test

    Parameters
    ----------
    shade1 : shader
        shader1
    color: str
        color of shader

    Returns
    -------
    number: shader
        someshader
    """
    return shade1 + color


def read_file(filepath):
    """Read File

    Read a file and return the contents

    Parameters
    ----------
    filepath: str
        Path to the file

    Returns
    -------
    output: str
        Content of file
    """
    try:
        with open(filepath) as f:
            return f.read()
    except FileNotFoundError:
        return ""


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


def read_json_pandas(api_address):
    """Fake People

    Generate fake people data

    Parameters
    ----------
    api_address: str
        Web address of the api

    Returns
    -------
    Dataframe: object
        Pandas dataframe
    """
    import requests
    import json

    r = requests.get("https://fakerapi.it/api/v1/persons")
    return pd.DataFrame(json.loads(r.text)["data"])


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


def display_markdown(markdown):
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


all_functions = [
    add_async,
    add_sync,
    add_async_win,
    shaderman,
    enter_string,
    enter_number,
    junk,
    add_same_objects,
    convert_to_string,
    dataframe_to_datatable,
    display_markdown,
]
