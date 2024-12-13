from dash import dcc, html

def get_layout(partitions):
    return html.Div(
        children=[
            html.Header(
                children=[
                    html.Img(
                        src="assets/logo.png",
                        alt="UM6P Logo",
                        style={"height": "50px"}
                    ),
                    html.H1("HPC Resource Manager")
                ]
            ),
            html.Main(
                children=[
                    html.Section(
                        children=[
                            html.Label(
                                "Select a Partition:",
                                style={
                                    "fontSize": "18px",
                                    "color": "#D65127",
                                    "marginBottom": "10px",
                                    "display": "block"
                                }
                            ),
                            dcc.Dropdown(
                                id="partition-dropdown",
                                options=[{"label": p, "value": p} for p in partitions],
                                placeholder="Select a partition",
                                style={
                                    "borderRadius": "8px",
                                    "padding": "10px",
                                    "fontSize": "16px",
                                    "backgroundColor": "#FFFFFF",
                                    "color": "#333333",
                                    "border": "1px solid #D65127",
                                    "width": "100%"
                                },
                            )
                        ],
                        id="partition-dropdown-container"
                    ),
                    dcc.Loading(
                        id="loading",
                        type="circle",
                        children=html.Section(
                            children=[
                                html.H3(
                                    "Partition Details",
                                    style={
                                        "color": "#D65127",
                                        "marginBottom": "10px"
                                    }
                                ),
                                html.P(
                                    id="cpu-output",
                                    children="Available CPUs: -",
                                    style={
                                        "margin": "10px 0",
                                        "fontSize": "16px"
                                    }
                                ),
                                html.P(
                                    id="gpu-output",
                                    children="Available GPUs: -",
                                    style={
                                        "margin": "10px 0",
                                        "fontSize": "16px"
                                    }
                                ),
                            ],
                            id="partition-details"
                        )
                    )
                ]
            ),
            html.Footer(
                children=[
                    html.Img(
                        src="/assets/um6p_logo.jpeg",
                        alt="UM6P Logo",
                        style={"height": "50px", "marginBottom": "10px"}
                    ),
                    html.P("Powered by the College of Computing - Shaping the Next Era of Computing"),
                    html.P(
                        [
                            "Visit the ",
                            html.A(
                                "College of Computing Website",
                                href="https://cc.um6p.ma/home",
                                target="_blank",
                                style={"textDecoration": "none"}
                            )
                        ]
                    ),
                    html.P("HPC Manager © 2024 - Enhancing High-Performance Computing")
                ]
            )
        ]
    )
