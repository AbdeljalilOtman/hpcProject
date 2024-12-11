from dash import dcc, html

def get_layout(partitions):
    return html.Div([
        
        html.Div(
            html.H1("Simlab Resource Manager"),
            style={"marginBottom": "20px , font-family:Calibri"}
        ),

        html.Div([
            html.Label("Select a Partition:"),
            dcc.Dropdown(
                id="partition-dropdown",
                options=[{"label": p, "value": p} for p in partitions],
                placeholder="Select a partition"
            ),
        ], id="partition-dropdown-container"),

        html.Div([
            html.H3("Partition Details"),
            html.P(id="cpu-output"),
            html.P(id="gpu-output"),
        ], id="partition-details"),
    ])
