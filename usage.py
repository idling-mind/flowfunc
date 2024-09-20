import dash
from dash import Input, Output, State, html
from flowfunc import Flowfunc, config, jobrunner

def add(a: int, b: int):
    """Add two numbers"""
    return a + b

def subtract(a: int, b: int):
    """Subtract one number from another"""
    return a - b


flist = [
    add,
    subtract,
]
app = dash.Dash(__name__)
fconfig = config.Config.from_function_list(flist)
runner = jobrunner.JobRunner(fconfig)
print(fconfig)

app.layout = html.Div(
    [
        html.Button(id="btn_run", children=["Run"]),
        html.Div(
            Flowfunc(
                id="nodeeditor",
                config=fconfig.json(),
                disable_zoom=True,
                type_safety=False,
            ),
            style={"height": "500px", "width": "100%"},
        ),
        html.Div(id="output"),
    ]
)


@app.callback(
    [Output("output", "children"), Output("nodeeditor", "nodes_status")],
    Input("btn_run", "n_clicks"),
    State("nodeeditor", "nodes"),
)
def run(nclicks, nodes):
    if not nodes:
        return [], {}
    print(nodes)
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
