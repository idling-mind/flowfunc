import pytest
from flowfunc.config import Config
from flowfunc.models import Node
from .methods import (
    add_str_inspect,
    add_str_type,
    all_methods,
    add_with_type_anno,
    get_dataclass_user,
    get_optional_arg,
    get_pydantic_user,
)


def test_creation_from_function_list():
    config = Config.from_function_list(all_methods)
    assert isinstance(config, Config)
    assert len(config.nodes) == len(all_methods)  # above methods
    assert len(config.ports) == 6  # int, float, float|int, object


def test_get_node():
    config = Config.from_function_list(all_methods)
    found_node = config.get_node("tests.methods.add_nothing")
    assert isinstance(found_node, Node)
    assert found_node.type == "tests.methods.add_nothing"
    with pytest.raises(ValueError):
        found_node = config.get_node("randomnode")


def test_convert_to_dict():
    config = Config.from_function_list(all_methods)
    config_dict = config.dict()
    assert isinstance(config_dict, dict)
    assert all(x in config_dict.keys() for x in ["nodeTypes", "portTypes"])
    assert isinstance(config_dict["nodeTypes"], list)
    assert isinstance(config_dict["portTypes"], list)
    assert len(config_dict["nodeTypes"]) == len(all_methods)
    assert len(config_dict["portTypes"]) == 6
    assert isinstance(config_dict["nodeTypes"][0], dict)


def test_int_port_controls():
    config = Config.from_function_list([add_with_type_anno])
    assert len(config.ports) == 1
    assert config.ports[0].type == "int"
    assert len(config.ports[0].controls) == 1
    assert config.ports[0].controls[0].type == "int"


def test_str_port_controls():
    config = Config.from_function_list([add_str_inspect])
    assert len(config.ports) == 1
    assert config.ports[0].type == "str"
    assert len(config.ports[0].controls) == 1
    assert config.ports[0].controls[0].type == "str"


def test_str_type_controls():
    config = Config.from_function_list([add_str_type])
    assert len(config.ports) == 1
    assert config.ports[0].type == "int"
    assert len(config.ports[0].controls) == 1
    assert config.ports[0].controls[0].type == "int"


def test_pydantic_user():
    config = Config.from_function_list([get_pydantic_user])
    assert len(config.ports) == 1
    assert config.ports[0].type == "PydanticUser"
    assert len(config.ports[0].controls) == 4
    assert config.ports[0].controls[0].type == "str"
    assert config.ports[0].controls[1].type == "str"
    assert config.ports[0].controls[2].type == "int"
    assert config.ports[0].controls[3].type == "select"
    assert len(config.ports[0].controls[3].options) == 3
    assert type(config.ports[0].controls[3].options[0]) == dict
    assert config.ports[0].controls[3].options[0]["value"] == 0


def test_dataclass_user():
    config = Config.from_function_list([get_dataclass_user])
    assert len(config.ports) == 1
    assert config.ports[0].type == "DataclassUser"
    assert len(config.ports[0].controls) == 4
    assert config.ports[0].controls[0].type == "str"
    assert config.ports[0].controls[1].type == "str"
    assert config.ports[0].controls[2].type == "multiselect"
    assert len(config.ports[0].controls[2].options) == 4
    assert type(config.ports[0].controls[2].options[0]) == dict
    assert config.ports[0].controls[2].options[0]["value"] == "house"
    assert config.ports[0].controls[3].type == "bool"


def test_optional():
    config = Config.from_function_list([get_optional_arg])
    assert len(config.ports) == 1
    assert config.ports[0].type == "str"
    assert len(config.ports[0].controls) == 1
    assert config.ports[0].controls[0].type == "str"
