from dash_flume.config import process_node_docstring, process_node_inspect
from dash_flume.models import Node, Port
from .methods import (
    add_with_docstring,
    add_alternate_docstring,
    add_nothing,
    add_with_type_anno,
    sumnprod_with_docstring,
    sumnprod_with_inspect,
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
    assert add_node.outputs[0].label == "int"
