import time
import dash_flume
from dash_flume.config import Config
from dash_flume.jobrunner import JobRunner
import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc
import json
import base64

from dash_flume.models import OutNode
from nodes import all_functions
import numpy as np

app = dash.Dash(__name__)

fconfig = Config.from_function_list(all_functions)
job_runner = JobRunner(fconfig)

app.layout = html.Div(
    [
        html.Button(id="run", children="Run"),
        html.Button(id="save", children="Save"),
        html.Button(id="clear", children="Clear"),
        html.Button(id="change", children="Change Config"),
        dcc.Upload(id="uploader", children=html.Button(id="load", children="Load")),
        html.Div(id="output"),
        dash.dcc.Download(id="download"),
        html.Div(
            id="nodeeditor_container",
            style={"height": "800px", "width": "100%"},
            children=dash_flume.DashFlume(
                id="input",
                style={"height": "800px"},
                # config=inconfig,
                config=fconfig.dict(),
                context={"context": "initial"},
            ),
        ),
    ]
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
    # Run
    if not nodes:
        return [], {}
    starttime = time.perf_counter()
    # output_dict = job_runner.run(nodes)
    nodes_output = job_runner.run(nodes)
    # nodes_output = {node_id: OutNode(**node) for node_id, node in output_dict.items()}
    endtime = time.perf_counter()
    print(starttime - endtime)
    outdiv = html.Div(children=[])
    for node in nodes_output.values():
        if node.error:
            outdiv.children.append(str(node.error))
            continue
        if "pandas_to_plot" in node.type:
            outdiv.children.append(node.value["Plot"])
        if "display_markdown" in node.type:
            outdiv.children.append(node.value["markdown"])
        if "dataframe_to_datatable" in node.type:
            outdiv.children.append(node.value["Datatable"])
    return outdiv, {node_id: node.status for node_id, node in nodes_output.items()}


@app.callback(
    Output("download", "data"),
    [Input("save", "n_clicks"), State("input", "nodes")],
    prevent_initial_call=True,
)
def func(n_clicks, nodes):
    return dict(content=json.dumps(nodes), filename="nodes.json")


@app.callback(
    Output("input", "config"),
    [Input("change", "n_clicks")],
    prevent_initial_call=True,
)
def func(n_clicks):
    config = Config(all_functions[:2]).dict()
    return config


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
