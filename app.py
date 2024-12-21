import dash
from dash import dcc, html, Input, Output, State
import paramiko
import re

################################################################################
# 1. Utilities for SSH/Paramiko
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

def execute_command(ssh_client, command):
    """
    Execute a command on the given SSH client and return its stdout as a string.
    Prints stderr if there's an error.
    """
    try:
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        if error:
            print(f"Error: {error}")
        return output
    except Exception as e:
        print(f"Failed to execute command '{command}': {e}")
        return None

################################################################################
# 2. Dash App Setup
################################################################################
app = dash.Dash(__name__)

app.layout = html.Div([
    # Store credentials in browser memory (once logged in)
    dcc.Store(id='credentials-store'),

    # --- (A) LOGIN SECTION ---
    html.Div([
        html.H2("Login to Simlab Cluster"),
        dcc.Input(
            id='username-input',
            type='text',
            placeholder='Username',
            style={'marginRight': '10px'}
        ),
        dcc.Input(
            id='password-input',
            type='password',
            placeholder='Password',
            style={'marginRight': '10px'}
        ),
        html.Button('Login', id='login-button'),
        html.Div(id='login-status', style={'color': 'red', 'marginTop': '10px'}),
    ], id='login-section', style={'marginBottom': '40px'}),

    # --- (B) RESOURCE MANAGER SECTION ---
    html.Div([
        html.H1("Cluster Partition Resource Manager", style={'marginBottom': '20px'}),

        # Dropdown for partitions
        html.Label("Select a Partition:"),
        dcc.Dropdown(
            id='partition-dropdown',
            placeholder="Loading partitions...",
            style={'width': '300px'}
        ),

        html.Div(id='resource-display', style={'marginTop': '20px', 'fontSize': '16px'})
    ], id='resource-section', style={'display': 'none'})  # hidden by default
])

################################################################################
# 3. Callback: Attempt Login
################################################################################
@app.callback(
    Output('login-status', 'children'),       # Show error or success message
    Output('credentials-store', 'data'),      # If login success, store credentials
    Output('login-section', 'style'),         # Hide login section on success
    Output('resource-section', 'style'),      # Show resource manager on success
    Input('login-button', 'n_clicks'),
    State('username-input', 'value'),
    State('password-input', 'value'),
    prevent_initial_call=True
)
def login_user(n_clicks, username, password):
    """
    Attempts to login to the cluster (SSH) using provided credentials.
    If successful, we store them in 'credentials-store' (dcc.Store),
    then hide the login section and show the resource manager.
    """
    if not username or not password:
        return "Please enter both username and password.", None, {}, {'display': 'none'}

    # Adjust to your HPC cluster's hostname
    host = "simlab-cluster.um6p.ma"

    try:
        # Test connection
        ssh_client = create_ssh_client(host, username, password)
        ssh_client.close()
        return (
            "",  # no error
            {'host': host, 'username': username, 'password': password},
            {'display': 'none'},       # hide login section
            {'display': 'block'}       # show resource manager
        )
    except ValueError as e:
        return (f"Login failed: {str(e)}", None, {}, {'display': 'none'})

################################################################################
# 4. Callback: Populate Partition Dropdown
################################################################################
@app.callback(
    Output('partition-dropdown', 'options'),
    Input('credentials-store', 'data'),
    prevent_initial_call=True
)
def update_partitions(credentials):
    """
    Once the user is logged in and we have credentials,
    fetch all partitions from the cluster using 'sinfo'
    and populate the dropdown.
    """
    if not credentials:
        return []

    host = credentials['host']
    username = credentials['username']
    password = credentials['password']

    ssh_client = create_ssh_client(host, username, password)

    # Fetch unique partitions
    command = "sinfo -h -o '%P' | sort | uniq"
    output = execute_command(ssh_client, command)
    ssh_client.close()

    if not output:
        # Could not fetch partitions or cluster is empty
        return []

    # Each line might contain partition names, sometimes with '*' for default
    partitions = [p.replace('*', '').strip() for p in output.splitlines() if p.strip()]

    # Return a list of {label, value} dicts
    return [{'label': p, 'value': p} for p in partitions]

################################################################################
# 5. Callback: Fetch Resource Availability
################################################################################
@app.callback(
    Output('resource-display', 'children'),
    Input('partition-dropdown', 'value'),
    State('credentials-store', 'data')
)
def fetch_partition_resources(selected_partition, credentials):
    """
    When the user selects a partition, we run a fresh 'sinfo -p <partition>'
    and parse CPU/GPU for nodes in 'idle' or 'mixed' states.
    """
    if not selected_partition or not credentials:
        return "Select a partition to view resources."

    host = credentials['host']
    username = credentials['username']
    password = credentials['password']

    ssh_client = create_ssh_client(host, username, password)
    command = f"sinfo -p {selected_partition} -o '%N %c %G %T'"
    output = execute_command(ssh_client, command)
    ssh_client.close()

    if not output:
        return f"No data returned for partition '{selected_partition}'. Possibly inactive or unreachable."

    lines = output.splitlines()
    idle_cpus = 0
    idle_gpus = 0

    # Each line has: NodeName CPUCount GRES State
    for line in lines:
        parts = line.split()
        if len(parts) < 4:
            continue
        node_name, cpu_count, gres, state = parts[0], parts[1], parts[2], parts[3]

        # Convert CPU count
        try:
            cpu_count = int(cpu_count)
        except ValueError:
            cpu_count = 0

        # Count resources only if state is 'idle' or 'mixed'
        if state in ['idle', 'mixed']:
            idle_cpus += cpu_count
            # Parse GPUs from gres if it matches "gpu:<num>"
            match = re.search(r'gpu:(\d+)', gres)
            if match:
                idle_gpus += int(match.group(1))

    return (f"Partition: {selected_partition}\n"
            f"Idle CPUs: {idle_cpus}\n"
            f"Idle GPUs: {idle_gpus}")

################################################################################
# 6. Run the Dash Server
################################################################################
if __name__ == '__main__':
    app.run_server(debug=True)
