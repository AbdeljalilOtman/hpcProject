from dash import Dash, Input, Output, State, dcc, html
import paramiko
from frontend import get_layout  # Import the layout from the frontend module
from backend import Connector  # Import the backend connector

################################################################################
# Utilities for SSH/Paramiko
################################################################################
def create_ssh_client(host, username, password):
    """
    Creates and returns a paramiko SSH client connected to the given host.
    Raises a ValueError if the connection fails.
    """
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)
        return client
    except Exception as e:
        raise ValueError(f"Failed to connect to {host} with user {username}: {e}")

################################################################################
# Dash App Class
################################################################################
class DashApp:
    def __init__(self, app):
        self.app = app
        self.connector = Connector()
        self.partitions = ['defq', 'gpu', 'shortq', 'longq', 'visu', 'special']
        self.setup_layout()
        self.setup_callbacks()

    def setup_layout(self):
        """Define the layout of the Dash app."""
        self.app.layout = html.Div([
            dcc.Store(id='credentials-store'),  # Store credentials in browser memory

            # --- Login Section ---
            html.Div([
                html.H2("Login to Simlab Cluster", style={'textAlign': 'center', 'color': '#333', 'marginBottom': '20px'}),
                dcc.Input(
                    id='username-input',
                    type='text',
                    placeholder='Username',
                    style={
                        'width': '100%',
                        'padding': '10px',
                        'marginBottom': '10px',
                        'border': '1px solid #ccc',
                        'borderRadius': '4px'
                    }
                ),
                dcc.Input(
                    id='password-input',
                    type='password',
                    placeholder='Password',
                    style={
                        'width': '100%',
                        'padding': '10px',
                        'marginBottom': '20px',
                        'border': '1px solid #ccc',
                        'borderRadius': '4px'
                    }
                ),
                html.Button(
                    'Login',
                    id='login-button',
                    style={
                        'width': '100%',
                        'padding': '10px',
                        'backgroundColor': '#007BFF',
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': '4px',
                        'cursor': 'pointer'
                    }
                ),
                html.Div(
                    id='login-status',
                    style={
                        'color': 'red',
                        'marginTop': '10px',
                        'textAlign': 'center'
                    }
                ),
            ],
            id='login-section',
            style={
                'maxWidth': '400px',
                'margin': '50px auto',
                'padding': '20px',
                'border': '1px solid #ddd',
                'borderRadius': '8px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
                'backgroundColor': '#f9f9f9'
            }),

            # --- Main App Section ---
            html.Div(get_layout(self.partitions), id='main-app-section', style={'display': 'none'})
        ])

    def setup_callbacks(self):
        """Set up the callbacks to handle login and update UI."""
        @self.app.callback(
            [Output('login-status', 'children'),
             Output('credentials-store', 'data'),
             Output('login-section', 'style'),
             Output('main-app-section', 'style')],
            [Input('login-button', 'n_clicks')],
            [State('username-input', 'value'), State('password-input', 'value')],
            prevent_initial_call=True
        )
        def login_user(n_clicks, username, password):
            if not username or not password:
                return "Please enter both username and password.", None, {}, {'display': 'none'}

            host = "simlab-cluster.um6p.ma"
            try:
                ssh_client = create_ssh_client(host, username, password)
                ssh_client.close()
                return "", {'host': host, 'username': username, 'password': password}, {'display': 'none'}, {'display': 'block'}
            except ValueError as e:
                return f"Login failed: {str(e)}", None, {}, {'display': 'none'}

        @self.app.callback(
            [Output("cpu-output", "children"),
             Output("gpu-output", "children")],
            [Input("partition-dropdown", "value")],
            [State('credentials-store', 'data')]
        )
        def update_resources(selected_partition, credentials):
            if not selected_partition or not credentials:
                return "Available CPUs: -", "Available GPUs: -"

            partition_data = self.connector.get_resources(selected_partition)
            if partition_data:
                return (
                    f"Available CPUs: {partition_data[0]}",
                    f"Available GPUs: {partition_data[1]}"
                )
            else:
                return "Failed to retrieve CPUs", "Failed to retrieve GPUs"

# Create Dash app and run
if __name__ == "__main__":
    app = Dash(__name__, external_stylesheets=["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"])
    DashApp(app)  # Initialize the DashApp
    app.run_server(debug=False)
