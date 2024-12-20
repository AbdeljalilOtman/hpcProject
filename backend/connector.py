import paramiko
from .credentials_manager import CredentialsManager

class Connector:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Connector, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, '__initialized'):
            self.__SIMLAB_HOST = 'simlab-cluster.um6p.ma'
            self.__credentials_manager = CredentialsManager()
            self.__initialized = True
            self.__client = paramiko.SSHClient()


    def __execute_command(self, command):
        SIMLAB_USERNAME = self.__credentials_manager.get_username()
        SIMLAB_PASSWORD = self.__credentials_manager.get_password()
        client = self.__client
        try:
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.__SIMLAB_HOST, username=SIMLAB_USERNAME, password=SIMLAB_PASSWORD)

            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()

            if error:
                print(f"Error: {error}")
                return None
            return output
        except Exception as e:
            print(f"Failed to execute command: {e}")
            return None

    def get_resources(self, partition):
        output = self.__execute_command(f"cd project && ./proj.sh {partition}")
        print(output)
        out = output.split(",")
        return tuple(map(lambda x: int(x), out))
    def close(self):
        self.__client.close()



if __name__ == "__main__":
    connector = Connector()
    output = connector.get_resources("special")



