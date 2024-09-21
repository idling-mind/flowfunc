from datetime import date
from enum import Enum
import json
from pathlib import Path
import dash
from dash import Input, Output, State, html
from flowfunc import Flowfunc, config, jobrunner
from methods import add_async_with_sleep, add_str_inspect, divide_numbers

app = dash.Dash(__name__)
fconfig = config.Config.from_function_list(
    [divide_numbers, add_async_with_sleep, add_str_inspect]
)
runner = jobrunner.JobRunner(fconfig)

app.layout = html.Div(
    [
        html.Button(id="btn_run", children=["Run"]),
        html.Button(id="btn_addnode", children=["Add a node"]),
        html.Div(
            Flowfunc(
                id="someid",
                config=fconfig.dict(),
                disable_zoom=True,
                type_safety=False,
            ),
            style={"height": "600px", "width": "100%"},
        ),
        html.Div(id="output"),
    ]
)


@app.callback(
    [Output("output", "children"), Output("someid", "nodes_status")],
    Input("btn_run", "n_clicks"),
    State("someid", "nodes"),
    State("someid", "comments"),
)
def run(nclicks, nodes, comments):
    if not nodes:
        return [], {}
    Path("nodes_async.node").write_text(json.dumps(nodes))
    output = runner.run(nodes)
    output_html = []
    nodes_status = {}
    for node in output.values():
        output_html.append(html.Div(f"{node.type}: {node.result}"))
        if node.error:
            output_html.append(html.Div(f"{node.error}"))
        nodes_status[node.id] = node.status
    return output_html, nodes_status


if __name__ == "__main__":
    app.run_server(debug=True)
