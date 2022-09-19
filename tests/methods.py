from typing import Tuple, Union


def add_with_docstring(a, b):
    """Add two numbers together

    Parameters
    ----------
    a: int
        First number
    b: int
        Second number

    Returns
    -------
    sum: int
        Sum of two numbers
    """
    return a + b


def add_alternate_docstring(a, b):
    """Add two numbers

    Args:
        a (int): First number
        b (int): Second number

    Returns:
        int: Sum of numbers
    """
    return a + b


def add_int_float_docstring(a, b):
    """Add two numbers together

    Parameters
    ----------
    a: int or float
        First number
    b: int or float
        Second number

    Returns
    -------
    sum: int or float
        Sum of two numbers
    """
    return a + b

def add_int_float_inspect(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    return a + b

def add_diff_int_and_float_inspect(a: Union[int, float], b: Union[int, float]) -> Tuple[int, float]:
    return a + b, a-b


def add_with_type_anno(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b


def add_nothing(a, b):
    return a + b


def sumnprod_with_docstring(a, b):
    """Sum and product of two numbers

    Parameters
    ----------
    a: int
        First number
    b: int
        Second number

    Returns
    -------
    sum: int
        Sum of two numbers
    prod: int
        Product of two numbers
    """
    return a + b, a * b


def sumnprod_with_inspect(a: int, b: int) -> Tuple[int, int]:
    """Sum and product of two numbers"""
    return a + b, a * b

def add_position_only(a:int, b:int, /) -> int:
    return a+b

def add_wrong_docstring(a: int, b: int) -> int:
    """Add two numbers
    
    Args:
        a (int): first number
    
    Returns:
        sum: sum of numbers
    """
    return a + b

def add_str_type(a: "number", b: "number") -> "number":
    return a + b

def add_tuples_inspect(a: Union[Tuple[int,int], Tuple[float, float]], b: int) -> Tuple[float, float]:
    return a[0] + b, a[1] + b