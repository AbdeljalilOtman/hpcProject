from dash import dcc, html

def get_layout(partitions):
    return html.Div([
        # Header Section
        html.Div(
            html.H1("Simlab Resource Manager", className="header-title"),
            className="header"
        ),

        # Dropdown Section
        html.Div([
            html.Label("Select a Partition:", className="dropdown-label"),
            dcc.Dropdown(
                id="partition-dropdown",
                options=[{"label": p, "value": p} for p in partitions],
                placeholder="Select a partition",
                className="dropdown"
            ),
        ], className="dropdown-container"),

        # Partition Details Section with Loading
        dcc.Loading(
            id="loading-details",
            type="circle",
            children=html.Div([
                html.H3("Partition Details", className="details-header"),
                html.P("CPU Details: ", id="cpu-output", className="details-text"),
                html.P("GPU Details: ", id="gpu-output", className="details-text"),
            ], className="details-container"),
        ),
    ], className="app-container")
