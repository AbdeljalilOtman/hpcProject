from dash import dcc, html

def get_layout(partitions):
    return html.Div(
        className="dashboard-container",
        children=[
            html.Header(
                className="header",
                children=[
                    html.Img(
                        src="assets/logo.png",
                        alt="UM6P Logo",
                        className="header-logo"
                    ),
                    html.H1(
                        "HPC Resource Manager",
                        className="header-title"
                    )
                ]
            ),
            html.Main(
                className="main-content",
                children=[
                    # Flex container to center the content and align dropdown and result to left/right
                    html.Div(
                        className="content-flex-container",
                        children=[
                            # Left section for the dropdown
                            html.Section(
                                className="partition-dropdown-container",
                                children=[
                                    html.Label(
                                        "Select a Partition:",
                                        className="partition-dropdown-label"
                                    ),
                                    dcc.Dropdown(
                                        id="partition-dropdown",
                                        options=[{"label": p, "value": p} for p in partitions],
                                        placeholder="Select a partition",
                                        className="partition-dropdown"
                                    )
                                ],
                                id="partition-dropdown-container"
                            ),
                            # Right section for the partition details
                            dcc.Loading(
                                id="loading",
                                type="circle",
                                children=html.Section(
                                    className="partition-details",
                                    children=[
                                        html.H3(
                                            "Partition Details",
                                            className="partition-details-title"
                                        ),
                                        html.Div(
                                            className="item",
                                            children=[
                                                html.Img(
                                                    src="assets/processor.png",
                                                    alt="CPU Icon",
                                                    className="partition-details-icon"
                                                ),
                                                html.P(
                                                    id="cpu-output",
                                                    children="Available CPUs: -",
                                                    className="partition-details-text"
                                                )
                                            ]
                                        ),
                                        html.Div(
                                            className="item",
                                            children=[
                                                html.Img(
                                                    src="assets/graphic-card.png",
                                                    alt="GPU Icon",
                                                    className="partition-details-icon"
                                                ),
                                                html.P(
                                                    id="gpu-output",
                                                    children="Available GPUs: -",
                                                    className="partition-details-text"
                                                )
                                            ]
                                        )
                                    ],
                                    id="partition-details"
                                )
                            )
                        ]
                    )
                ]
            ),
            html.Footer(
                className="footer",
                children=[
                    html.Img(
                        src="/assets/um6p_logo.jpeg",
                        alt="UM6P Logo",
                        className="footer-logo"
                    ),
                    html.P(
                        "Powered by the College of Computing - Shaping the Next Era of Computing",
                        className="footer-text"
                    ),
                    html.P(
                        [
                            "Visit the ",
                            html.A(
                                "College of Computing Website",
                                href="https://cc.um6p.ma/home",
                                target="_blank",
                                className="footer-link"
                            )
                        ]
                    ),
                    html.P("HPC Manager © 2024 - Enhancing High-Performance Computing")
                ]
            )
        ]
    )
