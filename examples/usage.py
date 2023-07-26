import time
import flowfunc
from flowfunc.config import Config
from flowfunc.jobrunner import JobRunner
import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc
import dash_bootstrap_components as dbc
import json
import base64

from flowfunc.models import OutNode
from nodes import all_functions

app = dash.Dash(external_stylesheets=[dbc.themes.SLATE])
from flowfunc.models import Node, Port, Control, ControlType, PortFunction

# This is a simple function which will pass on the selected file name(from the select control) to the output port
# You could as well use an api call or pull data from a database or so to get the file/data.
def file_selector(**kwargs):
    return kwargs

portf = PortFunction(source="""
{
    console.log(arguments);
    var ports = arguments[0];
    var data = arguments[1];
    const template = (data && data.template && data.template.in_string) || "";
    const re = /\{(.*?)\}/g;
    let res, ids = []
    while ((res = re.exec(template)) !== null) {
    if (!ids.includes(res[1])) ids.push(res[1]);
    }
    console.log(ids);
    return [
    ports.str({ name: "template", label: "Template", hidePort: true }),
    ...ids.map(id => ports.str({ name: id, label: id }))
    ];
}
""")

file_selector_control = Control(
    type=ControlType.select,
    name="file_selector",
    label="Select a File",
    options=[
        # List your files in here. Create this dictionary from the uploaded files.
        {"value": "file1.txt", "label": "this is file 1"},
        {"value": "file2.txt", "label": "this is file 2"},
    ],
)
file_selector_port = Port(
    type="file_selector",
    name="infile",
    label="Select File",
    controls=[file_selector_control],
)

portf_node = Node(
    type="file_selector",
    label="File Selector",
    method=file_selector,
    inputs=portf,
    # outputs=[file_selector_port]
)

app = dash.Dash(external_stylesheets=[dbc.themes.SLATE])

fconfig = Config.from_function_list(
    all_functions, extra_nodes=[portf_node]
)
# fconfig = Config.from_function_list(all_functions)
job_runner = JobRunner(fconfig)

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
                "z-index": "15",
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

app.layout = html.Div(
    dbc.Row(
        [
            dbc.Col(width=8, children=node_editor),
            dbc.Col(
                id="output", width=4, style={"height": "100vh", "overflow": "auto"}
            ),
        ],
    ),
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
    starttime = time.perf_counter()
    # output_dict = job_runner.run(nodes)
    nodes_output = job_runner.run(nodes)
    # nodes_output = {node_id: OutNode(**node) for node_id, node in output_dict.items()}
    endtime = time.perf_counter()
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
