from pprint import pprint
import time
import flowfunc
from flowfunc.config import Config
from flowfunc.jobrunner import JobRunner
from flowfunc.models import Node, Port, PortFunction, Control, ControlType
import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc, ALL, MATCH
import dash_bootstrap_components as dbc
import json
import base64

from dash.dcc import Upload

from flowfunc.models import OutNode
from nodes import all_functions, slider1_port, slider2_port

app = dash.Dash(
    __name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.SLATE]
)


def convert_template(**kwargs):
    """Testing dynamic ports"""
    return str(kwargs)


def convert_to_list(**kwargs):
    return list(kwargs.values())


increasing_ports_function = PortFunction(path="increasing_ports")

dynamic_port_function = PortFunction(path="subspace.dynamic_ports")
# "dynamic_ports" should be defined in /assets/*.js at the
# path window.dash_clientside.flowfunc.dynamic_ports


template_node = Node(
    type="dynamic_ports",
    label="Dynamic Ports",
    description="Testing dynamic ports",
    method=convert_template,
    inputs=dynamic_port_function,
    outputs=[Port(type="str", name="template", label="Template")],
)

list_node = Node(
    type="increasing_list",
    label="Auto increasing list",
    description="Auto increasing list",
    method=convert_to_list,
    inputs=increasing_ports_function,
    outputs=[Port(type="object", name="object", label="List")],
)

custom_control_port = Port(
    type="cc",
    name="cc",
    label="custom control",
    controls=[
        Control(
            type=ControlType.custom,
            name="upload",
            label="Upload",
            # defaultValue="1",
            renderFunction="upload_control",  # defined in assets/funcs.js
        )
    ],
)

custom_control_node = Node(
    type="custom_control",
    label="Custom Control",
    description="Custom Control",
    method=convert_template,
    inputs=PortFunction(path="increasing_ports_upload"),
    outputs=[Port(type="str", name="output", label="output control")],
)

app = dash.Dash(external_stylesheets=[dbc.themes.SLATE])

fconfig = Config.from_function_list(
    all_functions,
    extra_nodes=[template_node, list_node, custom_control_node],
    extra_ports=[custom_control_port, slider1_port, slider2_port],
)
# fconfig = Config.from_function_list(all_functions)
job_runner = JobRunner(fconfig)

# pprint(fconfig.dict())

node_editor = html.Div(
    [
        dbc.ButtonGroup(
            [
                dbc.Button(id="run", children="Run"),
                dbc.Button(id="save", children="Save"),
                dbc.Button(id="clear", children="Clear"),
                dcc.Upload(
                    id="uploader", children=dbc.Button(id="load", children="Load")
                ),
                dash.dcc.Download(id="download"),
            ],
            style={
                "position": "absolute",
                "top": "15px",
                "left": "15px",
                "zIndex": "15",
            },
        ),
        html.Div(
            id="nodeeditor_container",
            children=flowfunc.Flowfunc(
                id="input",
                # config=inconfig,
                config=fconfig.dict(),
                context={"context": "initial"},
            ),
            style={
                "position": "relative",
                "width": "100%",
                "height": "100vh",
            },
        ),
    ]
)

app.layout = html.Div([
    dbc.Row(
        [
            dbc.Col(width=8, children=node_editor),
            dbc.Col(
                id="output", width=4, style={"height": "100vh", "overflow": "auto"}
            ),
        ],
    )],
    style={"overflow": "hidden"},
)


def parse_uploaded_contents(contents):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    data = json.loads(decoded.decode("utf-8"))
    try:
        for key, value in data.items():
            node = OutNode(**value)
        # Parsing succeeded
        return data
    except Exception as e:
        print(e)
        print("The uploaded file could not be parsed as a flow file.")


@app.callback(
    [
        Output("output", "children"),
        Output("input", "nodes_status"),
    ],
    [
        Input("run", "n_clicks"),
        State("input", "nodes"),
    ],
)
def display_output(runclicks, nodes):
    if not nodes:
        return [], {}
    # output_dict = job_runner.run(nodes)
    nodes_output = job_runner.run(nodes)
    outdiv = html.Div(children=[])
    for node in nodes_output.values():
        if node.error:
            outdiv.children.append(str(node.error))
        if "display" in node.type:
            outdiv.children.append(node.result)

    return outdiv, {node_id: node.status for node_id, node in nodes_output.items()}


@app.callback(
    Output("download", "data"),
    [Input("save", "n_clicks"), State("input", "nodes")],
    prevent_initial_call=True,
)
def func(n_clicks, nodes):
    return dict(content=json.dumps(nodes), filename="nodes.json")


@app.callback(
    [
        Output("input", "nodes"),
        Output("input", "editor_status"),
    ],
    [
        Input("uploader", "contents"),
        Input("clear", "n_clicks"),
        State("input", "nodes"),
    ],
    prevent_initial_call=True,
)
def update_output(contents, nclicks, nodes):
    ctx = dash.callback_context
    if not ctx.triggered:
        return nodes, "server"
    control = ctx.triggered[0]["prop_id"].split(".")[0]
    if control == "uploader":
        newnodes = parse_uploaded_contents(contents)
        return newnodes, "server"
    return {}, "server"


if __name__ == "__main__":
    app.run_server(debug=True)
