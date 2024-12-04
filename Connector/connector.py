import paramiko
import os

def read_properties_file(file_path):
    """Reads a .properties file and returns a dictionary of key-value pairs."""
    properties = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Skip empty lines or comments
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # Split key and value at the first '='
                key, value = line.split('=', 1)
                properties[key.strip()] = value.strip()

    except Exception as e:
        print(f"Error reading properties file: {e}")
    
    return properties

# Path to the properties file
properties_file = "simlab.properties"
# Load credentials from the properties file
credentials = read_properties_file(properties_file)
# Extract credentials
SIMLAB_USERNAME = credentials.get('simlab.username')
SIMLAB_PASSWORD = credentials.get('simlab.password')
SIMLAB_HOST = 'simlab-cluster.um6p.ma'

# Check if the credentials are loaded
if not SIMLAB_USERNAME or not SIMLAB_PASSWORD:
    raise ValueError("Username or password is missing in the properties file.")

# Print to confirm that credentials are loaded
print(f"Loaded credentials for user: {SIMLAB_USERNAME}")

def execute_simlab_command(command):
    try:
        # Create an SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to Simlab using password-based authentication
        client.connect(SIMLAB_HOST, username=SIMLAB_USERNAME, password=SIMLAB_PASSWORD)

        # Execute the command
        stdin, stdout, stderr = client.exec_command(command)

        # Read the output and error
        output = stdout.read().decode()
        error = stderr.read().decode()

        # Close the connection
        client.close()

        if error:
            print(f"Error: {error}")
        return output
    except Exception as e:
        print(f"Failed to execute command: {e}")
        return None

