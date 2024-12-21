import re
import sys

def parse_nodes(input_string):
    # Extract the base name and range part
    match = re.match(r'(\w+)\[(.+)\]', input_string)
    if not match:
        return [input_string]
    
    base_name, ranges = match.groups()
    nodes = []

    # Split the ranges by commas
    for rng in ranges.split(','):
        if '-' in rng:
            # Handle range (e.g., 01-05)
            start, end = map(int, rng.split('-'))
            for i in range(start, end + 1):
                nodes.append(f"{base_name}{i:02d}")
        else:
            # Single node (e.g., 14)
            nodes.append(f"{base_name}{int(rng):02d}")

    return nodes

if __name__ == "__main__":
    # Ensure an argument is provided
    if len(sys.argv) != 2:
        print("Usage: python test.py 'node[01-05,14,15]'")
        sys.exit(1)

    # Get the input string from the command-line argument
    input_string = sys.argv[1]
    node_list = parse_nodes(input_string)

    # Print the result space-separated for Bash
    print(" ".join(node_list))
