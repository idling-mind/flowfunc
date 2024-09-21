from enum import Enum
from typing import List, Optional, Tuple, Union
import asyncio
from pydantic import BaseModel
from dataclasses import dataclass


def add_normal(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


def add_int_float_inspect(
    a: Union[int, float], b: Union[int, float]
) -> Union[int, float]:
    return a + b


def add_diff_int_and_float_inspect(
    a: Union[int, float], b: Union[int, float]
) -> Tuple[int, float]:
    return a + b, a - b


def add_with_type_anno(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b


def add_nothing(a, b):
    return a + b


def sumnprod_with_inspect(a: int, b: int) -> Tuple[int, int]:
    """Sum and product of two numbers"""
    return a + b, a * b


def add_position_only(a: int, b: int, /) -> int:
    return a + b



def add_str_type(a: "int", b: "int") -> "int":
    return a + b


async def add_tuples_inspect(
    a: Union[Tuple[int, int], Tuple[float, float]], b: int
) -> Tuple[Tuple[float, float], float]:
    await asyncio.sleep(2)
    return a[0] + b, a[1] + b


async def add_str_inspect(a: str, b: str) -> str:
    return a + b


class Sex(Enum):
    Female = 0
    Male = 1
    Other = 3


class Things(Enum):
    House = "house"
    Car = "car"
    Boat = "boat"
    Caravan = "caravan"


class PydanticUser(BaseModel):
    firstname: str
    lastname: str
    age: int
    sex: Sex


@dataclass
class DataclassUser:
    firstname: str
    lastname: str
    things: List[Things]
    married: bool


def get_pydantic_user(user: PydanticUser) -> PydanticUser:
    return user


def get_dataclass_user(user: DataclassUser) -> DataclassUser:
    return user


def get_optional_arg(s: Optional[str]) -> str:
    return s


all_methods = [
    add_normal,
    add_diff_int_and_float_inspect,
    add_int_float_inspect,
    add_nothing,
    get_pydantic_user,
    get_dataclass_user,
]

async def add_async_with_sleep(a: int, b: int) -> int:
    """adding numbers with async sleep"""
    await asyncio.sleep(0.1)
    return a+b
    
def divide_numbers(a: int, b: int) -> float:
    """Divide one number by another"""
    return a/b