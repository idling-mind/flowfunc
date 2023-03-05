import pytest
from flowfunc.config import process_node_docstring, process_node_inspect
from flowfunc.models import Node, Port
from .methods import (
    add_with_docstring,
    add_alternate_docstring,
    add_nothing,
    add_with_type_anno,
    add_int_float_docstring,
    add_int_float_inspect,
    add_diff_int_and_float_inspect,
    sumnprod_with_docstring,
    add_position_only,
    add_str_type,
    add_tuples_inspect
)


def test_process_node_docstring_add():
    """Testing add with docstring"""
    add_node = process_node_docstring(add_with_docstring)
    assert isinstance(add_node, Node)
    assert add_node.method == add_with_docstring
    assert "add_with_docstring" in add_node.type
    assert add_node.description == "Add two numbers together"
    assert add_node.label == "Add With Docstring"
    assert isinstance(add_node.inputs, list)
    assert len(add_node.inputs) == 2
    assert isinstance(add_node.inputs[0], Port)
    assert add_node.inputs[0].type == "int"
    assert add_node.inputs[0].label == "a (int)"
    assert add_node.inputs[0].acceptTypes[0] == "int"
    assert isinstance(add_node.inputs[1], Port)
    assert add_node.inputs[1].type == "int"
    assert add_node.inputs[1].label == "b (int)"
    assert add_node.inputs[1].acceptTypes[0] == "int"
    assert isinstance(add_node.outputs, list)
    assert len(add_node.outputs) == 1
    assert add_node.outputs[0].type == "int"
    assert add_node.outputs[0].label == "sum (int)"


def test_process_node_alternate_docstring():
    """Testing add with alternate docstring"""
    add_node = process_node_docstring(add_alternate_docstring)
    assert isinstance(add_node, Node)
    assert add_node.method == add_alternate_docstring
    assert "add_alternate_docstring" in add_node.type
    assert add_node.description == "Add two numbers"
    assert add_node.label == "Add Alternate Docstring"
    assert isinstance(add_node.inputs, list)
    assert len(add_node.inputs) == 2
    assert isinstance(add_node.inputs[0], Port)
    assert add_node.inputs[0].type == "int"
    assert add_node.inputs[0].label == "a (int)"
    assert add_node.inputs[0].acceptTypes[0] == "int"
    assert isinstance(add_node.inputs[1], Port)
    assert add_node.inputs[1].type == "int"
    assert add_node.inputs[1].label == "b (int)"
    assert add_node.inputs[1].acceptTypes[0] == "int"
    assert isinstance(add_node.outputs, list)
    assert len(add_node.outputs) == 1
    assert add_node.outputs[0].type == "int"
    assert add_node.outputs[0].label == "int"


def test_process_node_int_float_docstring():
    """Testing add with multiple types"""
    add_node = process_node_docstring(add_int_float_docstring)
    assert isinstance(add_node, Node)
    assert add_node.method == add_int_float_docstring
    assert "add_int_float_docstring" in add_node.type
    assert isinstance(add_node.inputs, list)
    assert len(add_node.inputs) == 2
    assert isinstance(add_node.inputs[0], Port)
    assert add_node.inputs[0].type == "float|int"
    assert add_node.inputs[0].label == "a (float,int)"
    assert add_node.inputs[0].acceptTypes[0] == "float"
    assert add_node.inputs[0].acceptTypes[1] == "int"
    assert isinstance(add_node.inputs[0], Port)
    assert add_node.inputs[1].type == "float|int"
    assert add_node.inputs[1].label == "b (float,int)"
    assert add_node.inputs[1].acceptTypes[0] == "float"
    assert add_node.inputs[1].acceptTypes[1] == "int"
    assert isinstance(add_node.outputs, list)
    assert len(add_node.outputs) == 1
    assert add_node.outputs[0].type == "float|int"
    assert add_node.outputs[0].label == "sum (int or float)"

def test_process_node_int_float_inspect():
    """Testing add with multiple types"""
    add_node = process_node_inspect(add_int_float_inspect)
    assert isinstance(add_node, Node)
    assert add_node.method == add_int_float_inspect
    assert "add_int_float_inspect" in add_node.type
    assert isinstance(add_node.inputs, list)
    assert len(add_node.inputs) == 2
    assert isinstance(add_node.inputs[0], Port)
    assert add_node.inputs[0].type == "float|int"
    assert add_node.inputs[0].label == "a (float,int)"
    assert add_node.inputs[0].acceptTypes[0] == "float"
    assert add_node.inputs[0].acceptTypes[1] == "int"
    assert isinstance(add_node.inputs[0], Port)
    assert add_node.inputs[1].type == "float|int"
    assert add_node.inputs[1].label == "b (float,int)"
    assert add_node.inputs[1].acceptTypes[0] == "float"
    assert add_node.inputs[1].acceptTypes[1] == "int"
    assert isinstance(add_node.outputs, list)
    assert len(add_node.outputs) == 1
    assert add_node.outputs[0].type == "float|int"
    assert add_node.outputs[0].label == "result (float,int)"

def test_process_node_int_and_float_inspect():
    """Testing add with multiple types"""
    add_node = process_node_inspect(add_diff_int_and_float_inspect)
    assert isinstance(add_node, Node)
    assert add_node.method == add_diff_int_and_float_inspect
    assert "add_diff_int_and_float_inspect" in add_node.type
    assert isinstance(add_node.outputs, list)
    assert len(add_node.outputs) == 2
    assert add_node.outputs[0].type == "int"
    assert add_node.outputs[0].label == "int"
    assert add_node.outputs[1].type == "float"
    assert add_node.outputs[1].label == "float"

def test_process_node_sum_prod_docstring():
    """Testing add with multiple types"""
    add_node = process_node_docstring(sumnprod_with_docstring)
    assert isinstance(add_node, Node)
    assert isinstance(add_node.outputs, list)
    assert len(add_node.outputs) == 2
    assert add_node.outputs[0].type == "int"
    assert add_node.outputs[0].label == "sum (int)"
    assert add_node.outputs[1].type == "int"
    assert add_node.outputs[1].label == "prod (int)"


def test_raise_exception():
    with pytest.raises(Exception):
        add_node = process_node_docstring(add_nothing)


def test_process_node_inspect_add():
    add_node = process_node_inspect(add_nothing)
    assert isinstance(add_node, Node)
    assert add_node.method == add_nothing
    assert "add_nothing" in add_node.type
    assert add_node.description == "No Description"
    assert add_node.label == "Add Nothing"
    assert isinstance(add_node.inputs, list)
    assert len(add_node.inputs) == 2
    assert isinstance(add_node.inputs[0], Port)
    assert add_node.inputs[0].type == "object"
    assert add_node.inputs[0].label == "a (object)"
    assert add_node.inputs[0].acceptTypes is None
    assert isinstance(add_node.inputs[1], Port)
    assert add_node.inputs[1].type == "object"
    assert add_node.inputs[1].label == "b (object)"
    assert add_node.inputs[1].acceptTypes is None
    assert isinstance(add_node.outputs, list)
    assert len(add_node.outputs) == 1
    assert add_node.outputs[0].type == "object"
    assert add_node.outputs[0].label == "object"


def test_process_node_inspect_add_with_type_anno():
    add_node = process_node_inspect(add_with_type_anno)
    assert isinstance(add_node, Node)
    assert add_node.method == add_with_type_anno
    assert "add_with_type_anno" in add_node.type
    assert add_node.description == "Add two numbers together"
    assert add_node.label == "Add With Type Anno"
    assert isinstance(add_node.inputs, list)
    assert len(add_node.inputs) == 2
    assert isinstance(add_node.inputs[0], Port)
    assert add_node.inputs[0].type == "int"
    assert add_node.inputs[0].label == "a (int)"
    assert add_node.inputs[0].acceptTypes[0] == "int"
    assert isinstance(add_node.inputs[1], Port)
    assert add_node.inputs[1].type == "int"
    assert add_node.inputs[1].label == "b (int)"
    assert add_node.inputs[0].acceptTypes[0] == "int"
    assert isinstance(add_node.outputs, list)
    assert len(add_node.outputs) == 1
    assert add_node.outputs[0].type == "int"
    assert add_node.outputs[0].label == "result (int)"

def test_position_only_warning():
    """This should raise a warning"""
    with pytest.warns(UserWarning):
        _ = process_node_inspect(add_position_only)

def test_str_type():
    """Node with str type"""
    add_node = process_node_inspect(add_str_type)
    assert isinstance(add_node, Node)
    assert add_node.method == add_str_type
    assert add_node.inputs[0].type == "int"
    assert add_node.inputs[1].type == "int"
    assert add_node.outputs[0].type == "int"

def test_add_tuple_inspect():
    """Inspect node with tuples"""
    add_node = process_node_inspect(add_tuples_inspect)
    assert isinstance(add_node, Node)
    assert add_node.method == add_tuples_inspect
    assert len(add_node.inputs) == 2
    assert len(add_node.outputs) == 2
    assert add_node.inputs[0].type == "tuple"
    assert add_node.inputs[1].type == "int"
    assert add_node.outputs[0].type == "tuple"
    assert add_node.outputs[1].type == "float"
