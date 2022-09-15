# Pydantic models corresponding to flume's object structure

from typing import Any, Callable, Dict, List, Optional, Union
from enum import Enum
from pydantic import BaseModel


class ControlType(str, Enum):
    """Control types available at the React side"""

    text = "text"
    number = "number"
    checkbox = "checkbox"
    select = "select"
    multiselect = "multiselect"
    custom = "custom"


class Color(str, Enum):
    """Different Color options available for the ports. Should match flume lib."""

    yellow = "yellow"
    orange = "orange"
    red = "red"
    pink = "pink"
    purple = "purple"
    blue = "blue"
    green = "green"
    grey = "grey"


class Control(BaseModel):
    """Control pydantic model. Not used to create any new ones at python end"""

    type: ControlType
    name: str
    label: str
    placeHolder: Optional[str]
    step: Optional[int]
    defaultValue: Optional[Any]
    options: Optional[List[dict]]  # Not implemented yet
    render: Optional[str]  # Not implemented yet

    class Config:
        use_enum_values = True


class Port(BaseModel):
    """Port objects are equivalent to python types.
    Some of the standard ports are avaiable at the React side.
    """

    type: str
    name: str
    label: str
    arg_or_kwarg: Optional[str]
    color: Optional[Color]
    acceptTypes: Optional[List[str]]
    hidePort: Optional[bool]
    controls: Optional[List[Control]]

    def __eq__(self, other):
        return self.type == other.type

    def __hash__(self):
        return hash(self.type)

    class Config:
        use_enum_values = True
        fields = {"arg_or_kwarg": {"exclude": True}}


class Node(BaseModel):
    """Objects corresponding to python functions. But only the name of the
    function are stored in the pydantic model
    """

    type: str
    label: str
    method: Callable
    module: Optional[str]
    description: Optional[str]
    initialWidth: Optional[Union[int, float]]
    addable: Optional[bool]
    deletable: Optional[bool]
    inputs: Optional[List[Port]]
    outputs: Optional[List[Port]]

    def __hash__(self):
        return hash(self.type)

    class Config:
        fields = {"method": {"exclude": True}}


class ConfigModel(BaseModel):
    """Python based FlumeConfig which gets converted to
    actual FlumeConfig object at the React end.
    """

    portTypes: List[Port]
    nodeTypes: List[Node]


# All Out* models are related to the data that's recieved from the editor
# (or from a json data parsed from a node file)
class OutConnection(BaseModel):
    """Input or output item"""

    nodeId: str
    portName: str
    job_id: Optional[str]


class OutConnections(BaseModel):
    """Collection of connections represeting all inputs and outputs of a node"""

    inputs: Dict[str, List[OutConnection]]
    outputs: Dict[str, List[OutConnection]]


class OutNode(BaseModel):
    """Node output from the flume UI.
    This could as well be a saved json file parsed
    """

    id: str
    x: int
    y: int
    type: str
    width: int
    connections: OutConnections
    inputData: Dict[str, Dict[str, Any]]

    # Below two items are created at the python end when the `run` event is
    # called on the MappedNode object.
    status: str = "idle"

    # The value of the node once it completes execution.
    result: Optional[Any]
    result_mapped: Optional[Dict[str, Any]]

    # Error traceback for node
    error: Optional[str]

    # asyncio event object.
    # Event object is used so that mutiple await calls can be made to this
    # object without causing a runtime error.
    run_event: Optional[Any]

    job: Optional[Any]
    job_id: Optional[str]

    # rq related settings which will be passed to enqueue function
    settings: Optional[Dict[str, Any]]


class OutNodes(BaseModel):
    __root__: Dict[str, OutNode]

    def __getitem__(self, item):
        return self.__root__[item]

    def items(self):
        return self.__dict__.items()
