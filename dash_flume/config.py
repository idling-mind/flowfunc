import inspect
from typing import Callable, List, Optional, Union, get_args, get_origin
from docstring_parser import parse

from .models import Node, ConfigModel, Color, Port
from .utils import logger


def process_port_docstring(param, ptype):
    """Process an input or an output of a function and convert it to flume
    config data

    Parameters
    ----------
    param:
        Parameter object from the docstring_parser module
    ptype:
        Parameter type

    Returns
    -------
    output_dict: dict
        Port data as dictionary
    """
    d = {}
    # Find out the different type options
    port_types = param.type_name.replace(" or ", ",").split(",")
    port_types = sorted([p.strip() for p in port_types])
    # The type of the port should be unique depending on the different
    # datatypes it accepts
    d["type"] = "|".join(port_types)
    d["acceptTypes"] = port_types
    if ptype == "input":
        if param.arg_name:
            d["name"] = param.arg_name
            d["label"] = f"{param.arg_name} ({','.join(d['acceptTypes'])})"
        else:
            d["name"] = d["label"] = d["type"]
    if ptype == "output":
        if param.return_name:
            d["name"] = param.return_name
            d["label"] = f"{param.return_name} ({param.type_name})"
        else:
            d["name"] = d["label"] = d["type"]
    return d


def process_node_docstring(func: Callable) -> Node:
    """Generate a node dict from a function object using it's docstring.

    This function creates a dictionary with information on how to create a
    flume node from the function by using the doc string of the function.
    It will raise an exception if there is no docstring.

    It expects the docstring format to be compatible with the docstring_parser
    module.

    Parameters
    ----------
    func: function
        The function whose docstring should be parsed and extracted.

    Returns
    -------
    node_dict: dict
    """
    node_dict = {}
    if not func.__doc__:
        raise Exception("Empty doc string!")
    parsed = parse(func.__doc__)
    node_dict["method"] = func
    node_dict["type"] = ".".join([func.__module__, func.__name__])
    node_dict["label"] = func.__name__.replace("_", " ").title()
    node_dict["module"] = func.__module__
    node_dict["description"] = parsed.short_description

    node_dict["inputs"] = [
        process_port_docstring(param, "input") for param in parsed.params
    ]
    node_dict["outputs"] = [
        process_port_docstring(param, "output") for param in parsed.many_returns
    ]

    return Node(**node_dict)


def arg_or_kwarg(par: inspect.Parameter):
    arg_kwarg_mapper = {
        inspect.Parameter.POSITIONAL_ONLY: "arg",
        inspect.Parameter.KEYWORD_ONLY: "kwarg",
        inspect.Parameter.POSITIONAL_OR_KEYWORD: "kwarg",
        inspect.Parameter.VAR_KEYWORD: "kwarg",
        inspect.Parameter.VAR_POSITIONAL: "arg",
    }
    return arg_kwarg_mapper.get(par.kind, "kwarg")


def process_port_inspect(pname, pobj):
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
        return {
            "type": "object",
            "name": pname,
            "label": f"{pname} (object)",
        }
    elif isinstance(pobj, str):
        pname = pobj.split("|")[0].strip()
        return {
            "type": pname,
            "name": pname,
            "label": pname,
        }
    d = {}
    origin = get_origin(pobj)
    if origin == Union:
        ptypes = get_args(pobj)
        pptypes = []
        for ptype in ptypes:
            if get_origin(ptype):
                pptypes.append(get_origin(ptype).__name__)
            else:
                pptypes.append(ptype.__name__)
        # Sorting so that the combination names are always consistent
        pptypes = sorted(pptypes)
        d["type"] = "|".join(pptypes)
        d["acceptTypes"] = pptypes
    elif origin:
        d["type"] = origin.__name__
        d["acceptTypes"] = [origin.__name__]
    else:
        d["type"] = pobj.__name__
        d["acceptTypes"] = [pobj.__name__]
    d["name"] = pname
    d["label"] = f"{pname} ({','.join(d['acceptTypes'])})"
    return d


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
            {
                "type": "object",
                "name": "object",
                "label": "object",
            }
        ]
    return_types = []
    origin = get_origin(pobj)
    if origin == tuple:
        for t in get_args(pobj):
            tt = get_origin(t)
            if tt:
                return_types.append(
                    str(tt).replace("typing.", ""), process_port_inspect(t)
                )
            else:
                return_types.append(
                    {
                        "type": t.__name__,
                        "name": t.__name__,
                        "label": t.__name__,
                    }
                )
        return return_types
    elif origin:
        if get_origin(origin):
            return [process_port_inspect(str(origin).replace("typing.", ""), origin)]
        else:
            return [process_port_inspect(origin.__name__, origin)]
    else:
        return [
            {
                "type": pobj.__name__,
                "name": pobj.__name__,
                "label": pobj.__name__,
            }
        ]


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
            logger.warning(
                "Handling position only parameter is not supported now."
                f" Node for {node_dict['type']} will not work as expected."
            )
        node_dict["inputs"].append(input_dict)
    node_dict["outputs"] = process_output_inspect(sign.return_annotation)

    return Node(**node_dict)


def ports_from_nodes(nodes: List[Node]) -> List[Port]:
    """Function to find unique port types that are used in all nodes"""
    ports = []
    for node in nodes:
        ports += node.inputs + node.outputs
    return list(set(ports))


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
            try:
                # Making sure node from doc string has the same number of input
                # args as from the inspect. If inspect shows more, use that.
                node_docstring = process_node_docstring(func)
                node_inspect = process_node_inspect(func)
                if len(node_docstring.inputs) < len(node_inspect.inputs):
                    node = node_inspect
                else:
                    node = node_docstring
            except Exception as e:
                node = process_node_inspect(func)
            nodes.append(node)

        if extra_nodes is None:
            extra_nodes = []
        if extra_ports is None:
            extra_ports = []
        # Some of the standard ports will be added at the js end
        # Finding unique ports. extra_ports have to be the first so that if there
        # is a duplicate the ports in that list gets precedence over the ports
        # from nodes
        ports = list(set(extra_ports + ports_from_nodes(nodes)))
        nodes = nodes + extra_nodes
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
