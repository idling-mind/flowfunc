import pytest
from dash_flume.config import Config
from dash_flume.models import Node
from .methods import (
    add_alternate_docstring,
    add_diff_int_and_float_inspect,
    add_int_float_docstring,
    add_int_float_inspect,
    add_nothing,
    add_with_docstring,
    add_wrong_docstring,
)


def test_creation_from_function_list():
    config = Config.from_function_list(
        [
            add_with_docstring,
            add_alternate_docstring,
            add_diff_int_and_float_inspect,
            add_alternate_docstring,
            add_int_float_docstring,
            add_int_float_inspect,
            add_nothing,
            add_wrong_docstring,
        ]
    )
    assert isinstance(config, Config)
    assert len(config.nodes) == 8  # above methods
    assert len(config.ports) == 4  # int, float, float|int, object

def test_get_node():
    config = Config.from_function_list(
        [
            add_with_docstring,
            add_alternate_docstring,
            add_diff_int_and_float_inspect,
            add_alternate_docstring,
            add_int_float_docstring,
            add_int_float_inspect,
            add_nothing,
            add_wrong_docstring,
        ]
    )
    found_node = config.get_node("tests.methods.add_nothing")
    assert isinstance(found_node, Node)
    assert found_node.type == "tests.methods.add_nothing"
    with pytest.raises(ValueError):
        found_node = config.get_node("randomnode")

def test_convert_to_dict():
    config = Config.from_function_list(
        [
            add_with_docstring,
            add_alternate_docstring,
            add_diff_int_and_float_inspect,
            add_alternate_docstring,
            add_int_float_docstring,
            add_int_float_inspect,
            add_nothing,
            add_wrong_docstring,
        ]
    )
    config_dict = config.dict()
    assert isinstance(config_dict, dict)
    assert all(x in config_dict.keys() for x in ["nodeTypes", "portTypes"])
    assert isinstance(config_dict["nodeTypes"], list)
    assert isinstance(config_dict["portTypes"], list)
    assert len(config_dict["nodeTypes"]) == 8
    assert len(config_dict["portTypes"]) == 4
    assert isinstance(config_dict["nodeTypes"][0], dict)