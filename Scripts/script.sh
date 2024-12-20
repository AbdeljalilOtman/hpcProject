#!/bin/bash
part=$1
totalCpus=0
available_gpus=0

# Get the info about idle/mixed nodes
info=$(sinfo -p $part --format="%G %C %T" | grep -E "idle|mixed")

# Process each line of the sinfo output to calculate available CPUs
while IFS= read -r line; do
    gres=$(echo "$line" | awk '{print $1}')
    cpus=$(echo "$line" | awk '{split($2, a, "/"); print a[2]}')

    if [[ "$gres" =~ gpu:([0-9]+) ]]; then
        gpus=${BASH_REMATCH[1]}
    else
        gpus=0
    fi

    totalCpus=$((totalCpus + cpus))
done <<< "$info"

if [ $# -ne 1 ]; then
    echo "Usage: $0 <partition>"
    echo "Example: $0 gpu"
    echo "Example: $0 visu"
    exit 1
fi
if [[ "$part" == "gpu" || "$part" == "visu" ]]; then

PARTITION=$1
if [[ "$part" == "gpu" ]]; then
    TOTAL_GPUS=12
else
    TOTAL_GPUS=1
fi

# Get list of nodes in this partition
# Extract the nodes field from the input
nodes=$(scontrol show partition $part | sed -n '6p' | grep -oP '(?<=Nodes=).*')
# Expand the node range
expanded_nodes=$(python test.py "$nodes")
# Format the list with braces and commas
formatted_list="${expanded_nodes// /, }"

# Initialize counter for allocated GPUs
total_allocated_gpus=0

# Check each node in the partition
for node in $formatted_list; do
    # Get node information
    node_info=$(scontrol show node "$node")
    
    # Extract GPU allocation from AllocTRES
    alloc_gpus=$(echo "$node_info" | grep "AllocTRES" | grep -oP 'gres/gpu=\K[0-9]+' || echo "0")
    
    # Add to total
    total_allocated_gpus=$((total_allocated_gpus + alloc_gpus))
    
done

# Calculate available GPUs
available_gpus=$((TOTAL_GPUS - total_allocated_gpus))


fi 

totalCpus=${totalCpus:-0}

# Output the totals in the required format: cpus,gpus
echo "$totalCpus,$available_gpus"

