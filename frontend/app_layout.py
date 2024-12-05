from dash import dcc, html

def get_layout(partitions):
    return html.Div([
        html.Link(rel='stylesheet', href='/frontend/assets/styles.css'),  # Link to the CSS file

        html.H1("Simlab Resource Manager"),

        html.Div([
            html.Label("Select a Partition:"),
            dcc.Dropdown(
                id="partition-dropdown",
                options=[{"label": p, "value": p} for p in partitions],
                placeholder="Select a partition"
            ),
        ]),

        html.Div([
            html.H3("Partition Details"),
            html.P(id="cpu-output"),
            html.P(id="gpu-output"),
        ])
    ])
