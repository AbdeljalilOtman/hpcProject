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