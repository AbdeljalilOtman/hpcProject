from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)
cluster_data = {
    "partition1": {"CPUs": 128, "GPUs": 8},
    "partition2": {"CPUs": 64, "GPUs": 4},
    "partition3": {"CPUs": 32, "GPUs": 2},
    "partition4": {"CPUs": 256, "GPUs": 16},
    "partition5": {"CPUs": 0, "GPUs": 0},  # Represents an inactive partition
}

app.layout = html.Div([
    html.H1("Cluster Partition Resource Manager"),
    dcc.Dropdown(
        id='partition-dropdown',
        options=[{'label': p, 'value': p} for p in cluster_data.keys()],
        placeholder="Select a partition"
    ),
    html.Div(id='resource-display', style={'marginTop': '20px'})
])

@app.callback(
    Output('resource-display', 'children'),
    Input('partition-dropdown', 'value')
)
def update_resources(partition):
    if partition:
        resources = cluster_data[partition]
        return f"Available CPUs: {resources['CPUs']}, GPUs: {resources['GPUs']}"
    return "Select a partition to view resources."

if __name__ == '__main__':
    app.run_server(debug=True)
