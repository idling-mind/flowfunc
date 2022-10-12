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
from redis import Redis

from flowfunc.models import OutNode
from flowfunc.distributed import NodeJob, NodeQueue
from nodes import all_functions

app = dash.Dash(external_stylesheets=[dbc.themes.SLATE])

rconn = Redis(host="localhost", port=6379)
q = NodeQueue(connection=rconn)

fconfig = Config.from_function_list(all_functions)
job_runner = JobRunner(fconfig, method="distributed", default_queue=q)

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
    [
        dcc.Interval(
            id="status_interval",
            interval=60 * 60 * 1000,  # in milliseconds
            n_intervals=0,
        ),
        dcc.Store(id="job_store"),
        dbc.Row(
            [
                dbc.Col(width=8, children=node_editor),
                dbc.Col(
                    id="output", width=4, style={"height": "100vh", "overflow": "auto"}
                ),
            ],
        ),
    ],
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
    Output("job_store", "data"),
    [
        Input("run", "n_clicks"),
        State("input", "nodes"),
    ],
)
def display_output(runclicks, nodes):
    if not nodes:
        return {}
    nodes_output = job_runner.run(nodes)
    store = {}
    for nodeid, node in nodes_output.items():
        store[nodeid] = node.dict(
            exclude={"run_event", "job"}
        )

    return store

@app.callback(
    [
        Output("output", "children"),
        Output("input", "nodes_status"),
        Output("status_interval", "interval"),
    ],
    [
        Input("status_interval", "n_intervals"),
        Input("job_store", "data"),
    ],
)
def get_status(ninterval, data):
    interval = 60 * 60 * 1000
    if not data:
        return "", {}, interval
    status = {}
    result = []
    for nodeid, node in data.items():
        node = OutNode.parse_obj(node)
        job = NodeJob.fetch(OutNode.parse_obj(node).job_id, connection=rconn)
        status[nodeid] = job.get_status()
        if not job.result is None and "display" in node.type:
            result.append(job.result)
    if any([x in ["started", "deferred"] for x in status.values()]):
        interval = 1000
    return result, status, interval


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
