from pprint import pprint
import time
import dash_flume
from dash_flume.config import Config
from dash_flume.jobrunner import JobRunner
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from dash import html, dcc
import json
import base64
from redis import Redis

from dash_flume.models import OutNode, OutNodes
from dash_flume.distributed import NodeJob, NodeQueue

from nodes import all_functions

external_stylesheets = [
    "https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css",
    "https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Lato:wght@300&family=Roboto&display=swap",
    "https://use.fontawesome.com/releases/v5.8.1/css/all.css",
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

rconn = Redis(host="localhost", port=6379)
q = NodeQueue(connection=rconn)
q_win = NodeQueue("win", connection=rconn)

fconfig = Config.from_function_list(all_functions)

job_runner = JobRunner(fconfig, method="distributed", default_queue=q)

app.layout = html.Div(
    [
        dcc.Interval(
            id="status_interval",
            interval=60 * 60 * 1000,  # in milliseconds
            n_intervals=0,
        ),
        dcc.Store(id="job_store"),
        html.Div(
            children=[
                html.Button(id="run", children="Run"),
                html.Button(id="save", children="Save"),
                dash.dcc.Download(id="download"),
                html.Button(id="clear", children="Clear"),
                html.Button(id="change", children="Change Config"),
                dcc.Upload(
                    id="uploader",
                    children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
                    style={
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                        "margin": "10px",
                    },
                ),
            ]
        ),
        html.Div(id="output"),
        html.Div(
            id="nodeeditor_container",
            style={"height": "90vh"},
            children=dash_flume.DashFlume(
                id="input",
                # config=inconfig,
                config=fconfig.dict(),
                context={"context": "initial"},
            ),
        ),
    ],
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
def run_nodes(runclicks, nodes):
    # Run
    starttime = time.perf_counter()
    if not nodes:
        return {}
    job = job_runner.run(nodes)
    job_nodes = OutNodes.parse_obj(job)
    store = {}
    for nodeid, node in job.items():
        store[nodeid] = OutNode.parse_obj(node).dict(
            exclude={"run_event", "job", "repr_method"}
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
        job = NodeJob.fetch(OutNode.parse_obj(node).job_id, connection=rconn)
        status[nodeid] = job.get_status()
        if job.result:
            result.append(str(job.result))
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
    Output("input", "config"),
    [
        Input("change", "n_clicks"),
        State("input", "config"),
    ],
    prevent_initial_call=True,
)
def func(n_clicks, config):
    return config


@app.callback(
    Output("input", "selected_nodes"),
    [
        Input("input", "selected_nodes"),
        Input("input", "nodes"),
    ],
    prevent_initial_call=True,
)
def func(selected, nodes):
    if not selected or not nodes:
        raise PreventUpdate
    for node in selected:
        print(nodes[node])
    return selected


@app.callback(
    [Output("input", "nodes"), Output("input", "editor_status")],
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
