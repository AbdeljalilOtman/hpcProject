import paramiko

def create_ssh_client(host, username, password):
    """
    Creates and returns a paramiko SSH client connected to the given host.
    Raises an exception if the connection fails.
    """
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)
        return client
    except Exception as e:
        raise ValueError(f"Failed to connect to {host} with user {username}: {str(e)}")

def execute_simlab_command(ssh_client, command):
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
        print(f"Failed to execute command: {e}")
        return None
