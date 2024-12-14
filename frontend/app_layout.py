from dash import dcc, html

def get_layout(partitions):
    return html.Div(
        className="dashboard-container",
        children=[
            # Header Section
            html.Header(
                className="header",
                children=[
                    html.Img(
                        src="assets/logo.png",
                        alt="UM6P Logo",
                        className="logo"
                    ),
                    html.H1("HPC Resource Manager", className="title")
                ],
                className="header"
            ),
            # Main Content Section
            html.Main(
                className="main-content",
                children=[
                    # SimLab Introduction Section
                    html.Section(
                        children=[
                            html.H2(
                                children=[
                                    html.I(className="fas fa-server"),  # Icon for "Server"
                                    " Introducing SimLab"
                                ],
                                className="section-title"
                            ),
                            html.P(
                                "SimLab is a development cluster maintained by the College of Computing, offering a wide range of computing and storage resources for researchers, students, and faculty.",
                                className="description"
                            ),
                            # Optimized Numbers Section
                            html.Div(
                                children=[
                                    html.Div(
                                        children=[
                                            html.I(className="fas fa-microchip"),  # CPU Icon
                                            html.P("784 CPUs", className="stat-number"),
                                            html.P("Compute Resources", className="stat-label")
                                        ],
                                        className="stat-card"
                                    ),
                                    html.Div(
                                        children=[
                                            html.I(className="fas fa-memory"),  # RAM Icon
                                            html.P("128 GB - 382 GB", className="stat-number"),
                                            html.P("Memory per Node", className="stat-label")
                                        ],
                                        className="stat-card"
                                    ),
                                    html.Div(
                                        children=[
                                            html.I(className="fas fa-gpu"),  # GPU Icon
                                            html.P("7 Pascal 40, 5 Volta 100", className="stat-number"),
                                            html.P("GPU Resources", className="stat-label")
                                        ],
                                        className="stat-card"
                                    ),
                                    html.Div(
                                        children=[
                                            html.I(className="fas fa-hdd"),  # Storage Icon
                                            html.P("Hundreds of Terabytes", className="stat-number"),
                                            html.P("Storage Resources", className="stat-label")
                                        ],
                                        className="stat-card"
                                    ),
                                    html.Div(
                                        children=[
                                            html.I(className="fas fa-network-wired"),  # Node Icon
                                            html.P("17 Nodes", className="stat-number"),
                                            html.P("Cluster Nodes", className="stat-label")
                                        ],
                                        className="stat-card"
                                    )
                                ],
                                className="stats-grid"
                            )
                        ],
                        id="simlab-introduction",
                        className="intro-section"
                    ),
                    # Partition Table Section
                    html.Section(
                        children=[
                            html.H3(
                                children=[
                                    html.I(className="fas fa-table"),  # Icon for "Table"
                                    " Partition Details"
                                ],
                                className="section-title"
                            ),
                            html.Table(
                                children=[
                                    html.Thead(
                                        children=html.Tr(
                                            children=[
                                                html.Th([html.I(className="fas fa-folder"), " Partition"]),
                                                html.Th([html.I(className="fas fa-clock"), " Max. CPU Time"]),
                                                html.Th([html.I(className="fas fa-server"), " Nodes Available"]),
                                                html.Th([html.I(className="fas fa-layer-group"), " Max Nodes per Job"]),
                                                html.Th([html.I(className="fas fa-tasks"), " Min-Max Cores per Job"])
                                            ]
                                        ),
                                        className="table-header"
                                    ),
                                    html.Tbody(
                                        children=[
                                            html.Tr(children=[
                                                html.Td("defq"),
                                                html.Td("1 hour"),
                                                html.Td("7 (node[01-05], node14, node15)"),
                                                html.Td("1"),
                                                html.Td("1-44")
                                            ]),
                                            html.Tr(children=[
                                                html.Td("shortq"),
                                                html.Td("4 hours"),
                                                html.Td("7 (node[01-05], node14, node15)"),
                                                html.Td("2"),
                                                html.Td("1-88")
                                            ]),
                                            html.Tr(children=[
                                                html.Td("longq"),
                                                html.Td("30 days"),
                                                html.Td("7 (node[01-05], node14, node15)"),
                                                html.Td("1"),
                                                html.Td("1-44")
                                            ]),
                                            html.Tr(children=[
                                                html.Td("special"),
                                                html.Td("30 minutes"),
                                                html.Td("17 (all nodes)"),
                                                html.Td("17"),
                                                html.Td("1-740")
                                            ]),
                                            html.Tr(children=[
                                                html.Td("visu"),
                                                html.Td("24 hours"),
                                                html.Td("1 (visu01)"),
                                                html.Td("1"),
                                                html.Td("1-44")
                                            ]),
                                            html.Tr(children=[
                                                html.Td("gpu"),
                                                html.Td("48 hours"),
                                                html.Td("12 (node[06-17])"),
                                                html.Td("2"),
                                                html.Td("1-88")
                                            ])
                                        ]
                                    )
                                ],
                                className="partition-table"
                            )
                        ],
                        id="partition-details-section",
                        className="details-section"
                    ),
                    # Dropdown and Partition Details
                    html.Div(
                        className="content-flex-container",
                        children=[
                            # Left Section: Dropdown
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
                            # Right Section: Partition Details
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
            # Footer Section
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
                        ],
                        className="footer-text"
                    ),
                    html.P(
                        "HPC Manager © 2024 - Enhancing High-Performance Computing",
                        className="footer-text"
                    )
                ],
                className="footer"
            )
        ],
        className="app-container"
    )
