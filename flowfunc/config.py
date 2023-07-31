from copy import deepcopy
from dataclasses import fields, is_dataclass
from enum import Enum
import inspect
from typing import Any, Callable, List, Optional, Union
try:
    from typing import get_args, get_origin
except ImportError:
    from typing_extensions import get_args, get_origin
from warnings import warn
from pydantic import BaseModel

from .models import Color, ConfigModel, ControlType, Node, Port, Control, PortFunction


def arg_or_kwarg(par: inspect.Parameter):
    arg_kwarg_mapper = {
        inspect.Parameter.POSITIONAL_ONLY: "arg",
        inspect.Parameter.KEYWORD_ONLY: "kwarg",
        inspect.Parameter.POSITIONAL_OR_KEYWORD: "kwarg",
        inspect.Parameter.VAR_KEYWORD: "kwarg",
        inspect.Parameter.VAR_POSITIONAL: "arg",
    }
    return arg_kwarg_mapper.get(par.kind, "kwarg")


def process_port_inspect(pname, pobj) -> Port:
    """Convert input arg of a function and convert it to flume config data
    based on it's signature

    Parameters
    ----------
    pname: str
        Name of the parameter
    pobj: Any
        The object representation of the arg

    Returns
    -------
    output_dict: dict
        Flume config dict
    """
    if pobj == inspect.Signature.empty:
        return Port(
            type="object",
            name=pname,
            label=f"{pname} (object)",
        )
    elif isinstance(pobj, str):
        if pobj.startswith("'") and pobj.endswith("'"):
            pobj = pobj[1:-1]
        ptype = pobj.split("|")[0].strip()
        return Port(type=ptype, name=pname, label=f"{pname} ({ptype})", py_type=ptype)
    d = {}
    origin = get_origin(pobj)
    if origin == Union:
        ptypes = get_args(pobj)
        # Checking for Optional
        # Represented as typing.Union[type, NoneType]
        if len(ptypes) == 2 and ptypes[1] == type(None):
            return process_port_inspect(pname, ptypes[0])
        pptypes = []
        for ptype in ptypes:
            if get_origin(ptype):
                pptypes.append(get_origin(ptype).__name__)
            else:
                pptypes.append(ptype.__name__)
        # Sorting so that the combination names are always consistent
        pptypes = sorted(set(pptypes))
        d["type"] = "|".join(pptypes)
        d["acceptTypes"] = pptypes
    elif origin:
        try:
            d["type"] = origin.__name__
        except AttributeError:
            # Special type origins
            d["type"] = str(origin).replace("typing.", "")
        d["py_type"] = pobj
        d["acceptTypes"] = [d["type"]]
    else:
        d["type"] = pobj.__name__
        d["py_type"] = pobj
        d["acceptTypes"] = [pobj.__name__]
    d["name"] = pname
    d["label"] = f"{pname} ({','.join(d['acceptTypes'])})"
    return Port(**d)


def process_output_inspect(pobj):
    """Process the return object based on signature

    Parameters
    ----------
    pobj: Any
        The return signature

    Returns
    -------
    output_dict: dict
        Flume config dict
    """
    if pobj == inspect.Signature.empty:
        return [
            Port(
                type="object",
                name="object",
                label="object",
            )
        ]
    return_types = []
    origin = get_origin(pobj)
    if origin == tuple:
        for t in get_args(pobj):
            tt = get_origin(t)
            if tt:
                return_types.append(
                    process_port_inspect(str(tt).replace("typing.", ""), t)
                )
            else:
                return_types.append(
                    Port(
                        type=t.__name__,
                        name=t.__name__,
                        label=t.__name__,
                    )
                )
        return return_types
    return [process_port_inspect("result", pobj)]


def process_node_inspect(func: Callable) -> Node:
    """Generate a node dict from a function object using it's signature.

    This function creates a dictionary with information on how to create a
    flume node from the function by using the doc string of the function.

    Parameters
    ----------
    func: function
        The function whose signature should be parsed and extracted.

    Returns
    -------
    node_dict: dict
    """
    node_dict = {}
    sign = inspect.signature(func)
    node_dict["method"] = func
    node_dict["type"] = ".".join([func.__module__, func.__name__])
    node_dict["label"] = func.__name__.replace("_", " ").strip().title()
    node_dict["module"] = func.__module__
    try:
        node_dict["description"] = func.__doc__.strip().split("\n")[0]
    except AttributeError:
        node_dict["description"] = "No Description"

    node_dict["inputs"] = []
    for pname, pobj in sign.parameters.items():
        input_dict = process_port_inspect(pname, pobj.annotation)
        # input_dict["arg_or_kwarg"] = arg_or_kwarg(pobj)
        if arg_or_kwarg(pobj) == "arg":
            # TODO: Handling args is not supported now
            warn(
                "Handling position only parameter is not supported now."
                f" Node for {node_dict['type']} will not work as expected."
            )
        node_dict["inputs"].append(input_dict)
    node_dict["outputs"] = process_output_inspect(sign.return_annotation)

    return Node(**node_dict)


def control_from_field(
    cname: str, cobj: Any, port: Optional[Port] = None
) -> Control:
    """Create a control from a give type object and it's properties

    Paramters:
        cname: Name of the argument
        cobj: Type hint used

    Returns:
        Control: A flowfunc Control object corresponding to the type annotation
    """
    control_types = [x.name for x in ControlType]
    if inspect.isclass(cobj) and issubclass(cobj, Enum):
        # Enum
        clabel = f"{cname} (enum)"
        options = [{"label": x.name, "value": x.value} for x in cobj]
        return Control(
            type=ControlType.select, name=cname, label=clabel, options=options
        )
    if (
        get_origin(cobj) == list
        and inspect.isclass(get_args(cobj)[0])
        and issubclass(get_args(cobj)[0], Enum)
    ):
        # List of enums
        clabel = f"{cname} (list)"
        options = [{"label": x.name, "value": x.value} for x in get_args(cobj)[0]]
        print("listenum", options)
        return Control(
            type=ControlType.multiselect, name=cname, label=clabel, options=options
        )
    if isinstance(cobj, str) and cobj in control_types:
        # When type annotation is a string
        clabel = f"{cname} ({cobj})"
        return Control(
            type=cobj,
            name=cname,
            label=clabel,
        )
    if hasattr(cobj, "__name__") and cobj.__name__ in control_types:
        clabel = f"{cname} ({cobj.__name__})"
        return Control(
            type=cobj.__name__,
            name=cname,
            label=clabel,
        )
    if port and port.acceptTypes and any([x in control_types for x in port.acceptTypes]):
        # If any of the accepted type has a corresponding control
        for t in port.acceptTypes:
            if t in control_types:
                return Control(
                    type=t,
                    name=cname,
                    label=port.label,
                )


def ports_from_nodes(nodes: List[Node]) -> List[Port]:
    """Function to find unique port types that are used in all nodes"""
    ports_: List[Port] = []
    for node in nodes:
        if not isinstance(node.inputs, PortFunction):
            ports_ += node.inputs
        if not isinstance(node.outputs, PortFunction):
            ports_ += node.outputs
    colors = [x.name for x in Color]
    ports = []
    for port_ in ports_:
        port = deepcopy(port_)
        ports.append(port)
        # Copy is made so that the port instance in Node object is unaffected
        if inspect.isclass(port.py_type) and issubclass(port.py_type, BaseModel):
            # Use a pydantic model
            port.controls = []
            for arg_name, field in port.py_type.__fields__.items():
                port.controls.append(
                    control_from_field(
                        field.name,
                        field.outer_type_,
                    )
                )
        elif inspect.isclass(port.py_type) and is_dataclass(port.py_type):
            port.controls = []
            for field in fields(port.py_type):
                port.controls.append(
                    control_from_field(
                        field.name,
                        field.type,
                    )
                )

        else:
            control = control_from_field(port.name, port.py_type, port)
            # Dont set controls if there are no controls corresponding to type
            if control:
                port.controls = [control]

    return ports


class Config:
    """This class is the python class corresponding to the flume config object.

    Attributes
    ----------
    nodes: list[Node]
        A list of pydantic Node objects which represent a node in the node editor config.
    ports: list
        A list of pydantic Port objects which represent a port in the node editor config.
    """

    @classmethod
    def from_function_list(
        cls,
        function_list: List[Callable],
        extra_nodes: Optional[List[Node]] = None,
        extra_ports: Optional[List[Port]] = None,
    ):
        """Create config from a list of functions

        Parameters
        ----------
        function_list: List[Callable]
            List of functions
        extra_nodes: Optional[List[Node]]
            List of extra nodes that should be added added to the config
        extra_ports: Optional[List[Node]]
            List of extra ports that should be added added to the config

        Returns
        -------
        config: Config
            An instance of Config object
        """
        nodes = []
        for func in function_list:
            node = process_node_inspect(func)
            nodes.append(node)

        if extra_nodes is None:
            extra_nodes = []
        if extra_ports is None:
            extra_ports = []
        nodes = nodes + extra_nodes
        ports = extra_ports + ports_from_nodes(nodes)
        return cls(nodes, ports)

    def __init__(self, nodes, ports=None) -> None:
        self.nodes = nodes
        # if ports is None, during the conversion of the object to a dict, the
        # ports from nodes are automatically extracted and used.
        self.ports = ports

    def get_node(self, node_type: str) -> Node:
        """Get a node object

        Parameters
        ----------
        node_type: str
            The type of node

        Returns
        -------
        node: Node
            Node pydantic object
        """
        for node in self.nodes:
            if node.type == node_type:
                return node
        raise ValueError(f"Node type {node_type} not found in config.")

    def dict(self) -> dict:
        """Function to generate the config dict

        This dictionary will be sent to the react backend
        """
        self.ports = list(filter(lambda p: p.type != "object", self.ports))
        # To create an object port, all available types have to be determined so that it
        # can connect to all port types.
        port_object = Port(
            type="object",
            name="object",
            label="object",
            color=Color.red,
            acceptTypes=[p.type for p in self.ports] + ["object"],
        )
        return ConfigModel(
            portTypes=self.ports + [port_object], nodeTypes=self.nodes
        ).dict(exclude_none=True)
