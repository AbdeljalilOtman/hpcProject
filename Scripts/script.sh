#!/bin/bash
part=$1

totalCpus=0
totalGpus=0

info=$(sinfo -p $part --format="%G %C %T" | grep -E "idle|mixed")

while IFS= read -r line; do
    gres=$(echo "$line" | awk '{print $1}')
    cpus=$(echo "$line" | awk '{split($2, a, "/"); print a[2]}') 
    
    if [[ "$gres" =~ gpu:([0-9]+) ]]; then
        gpus=${BASH_REMATCH[1]}  
    else
        gpus=0  
    fi

    totalCpus=$((totalCpus + cpus))
    totalGpus=$((totalGpus + gpus))

done <<< "$info"

echo "Total available CPUs: $totalCpus, Total available GPUs: $totalGpus"
