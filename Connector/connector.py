import paramiko
from tools import read_properties_file

class Connector:
    __instance = None  # Private class variable to hold the single instance

    def __new__(cls, *args, **kwargs):
        """Override the __new__ method to ensure only one instance is created"""
        if cls.__instance is None:
            # If instance doesn't exist, create it
            cls.__instance = super(Connector, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        """Initialize the credentials and host info"""
        if not hasattr(self, '__initialized'):  # To ensure that __init__ is not called more than once
            # Load credentials from properties file
            credentials = read_properties_file("Connector/simlab.properties")
            self.__SIMLAB_USERNAME = credentials.get('simlab.username')
            self.__SIMLAB_PASSWORD = credentials.get('simlab.password')
            self.__SIMLAB_HOST = 'simlab-cluster.um6p.ma'
            self.__initialized = True  # Mark the initialization as complete

    def execute_simlab_command(self, command):
        try:
            # Create an SSH client
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print(f"Connecting to {self.__SIMLAB_USERNAME}")
            # Connect to Simlab using password-based authentication
            client.connect(self.__SIMLAB_HOST, username=self.__SIMLAB_USERNAME, password=self.__SIMLAB_PASSWORD)

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

if __name__ == "__main__":
    # Both calls will return the same instance
    connector_instance_1 = Connector()


    # Fetch available partitions
    print("Fetching available partitions...")
    output = connector_instance_1.execute_simlab_command("sinfo --format='%P'")
    if output:
        print("Available partitions:")
        print(output)
