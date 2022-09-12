from dash_flume.config import process_node_docstring
from dash_flume.models import Node, Port
from .methods import add_with_docstring, add_with_inspect, sumnprod_with_docstring, sumnprod_with_inspect

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
