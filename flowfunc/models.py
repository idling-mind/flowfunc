# Pydantic models corresponding to flume's object structure

from typing import Any, Callable
from enum import Enum
from pydantic import BaseModel, Field


class ControlType(str, Enum):
    """Control types available at the React side"""

    number = "number"
    int = "int"
    float = "float"
    text = "text"
    str = "str"
    checkbox = "checkbox"
    bool = "bool"
    select = "select"
    multiselect = "multiselect"
    color = "color"
    date = "date"
    time = "time"
    month = "month"
    week = "week"
    object = "object"
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

    model_config = {"use_enum_values": True}

    type: ControlType
    name: str
    label: str
    placeHolder: str | None = None
    step: int | None = None
    defaultValue: Any | None = None
    options: list[dict] | None = None
    render: str | None = None  # Not implemented yet


class Port(BaseModel):
    """Port objects are equivalent to python types.
    Some of the standard ports are avaiable at the React side.
    """

    model_config = {"use_enum_values": True}

    type: str
    name: str
    label: str
    py_type: Any | None = Field(default=None, exclude=True)  # Associated python type
    arg_or_kwarg: str | None = Field(default=None, exclude=True)  # arg or kwarg
    color: Color | None = None
    acceptTypes: list[str] | None = None
    hidePort: bool | None = None
    controls: list[Control] | None = None

    def __eq__(self, other):
        return self.type == other.type

    def __hash__(self):
        return hash(self.type)


class PortFunction(BaseModel):
    """Use clientside javascript functions instead of ports"""

    source: str | None = None
    path: str | None = None


class Node(BaseModel):
    """Objects corresponding to python functions. But only the name of the
    function are stored in the pydantic model
    """

    type: str
    label: str
    method: Callable = Field(exclude=True)
    module: str | None = None
    category: str | None = None
    description: str | None = None
    initialWidth: int | float | None = None
    addable: bool | None = None
    deletable: bool | None = None
    inputs: list[Port] | PortFunction | None = None
    outputs: list[Port] | PortFunction | None = None

    def __hash__(self):
        return hash(self.type)


class ConfigModel(BaseModel):
    """Python based FlumeConfig which gets converted to
    actual FlumeConfig object at the React end.
    """

    portTypes: list[Port]
    nodeTypes: list[Node]


# All Out* models are related to the data that's recieved from the editor
# (or from a json data parsed from a node file)
class OutConnection(BaseModel):
    """Input or output item"""

    nodeId: str
    portName: str
    job_id: str | None = None


class OutConnections(BaseModel):
    """Collection of connections represeting all inputs and outputs of a node"""

    inputs: dict[str, list[OutConnection]]
    outputs: dict[str, list[OutConnection]]


class OutNode(BaseModel):
    """Node output from the flume UI.
    This could as well be a saved json file parsed
    """

    id: str
    x: float
    y: float
    type: str
    width: float
    connections: OutConnections
    inputData: dict[str, dict[str, Any]]

    # Below two items are created at the python end when the `run` event is
    # called on the MappedNode object.
    status: str = "idle"

    # The value of the node once it completes execution.
    result: Any | None = None
    result_mapped: dict[str, Any] | None = None

    # Error traceback for node
    error: str | None = None

    # asyncio event object.
    # Event object is used so that mutiple await calls can be made to this
    # object without causing a runtime error.
    run_event: Any | None = Field(default=None, exclude=True)

    job: Any | None = Field(default=None, exclude=True)
    job_id: str | None = None

    # rq related settings which will be passed to enqueue function
    settings: dict[str, Any] | None = None

    def model_dump_json(self, *args, **kwargs) -> str:
        kwargs["exclude"] = {"run_event", "job"}
        return super().model_dump_json(*args, **kwargs)
