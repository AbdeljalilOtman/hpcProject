#!/bin/bash
part=$1
totalCpus=0
totalGpus=0

# Get the info about idle/mixed nodes
info=$(sinfo -p $part --format="%G %C %T" | grep -E "idle|mixed")

# Process each line of the sinfo output to calculate available CPUs
while IFS= read -r line; do
    cpus=$(echo "$line" | awk '{split($2, a, "/"); print a[2]}') # Extract idle CPUs (second part)
    totalCpus=$((totalCpus + cpus))
done <<< "$info"

gpuspernode=1
cpuspernode=44

# Generate the gpusinfo output
gpusinfo=$((
  squeue -t RUNNING -o "%N %b %C" | awk '
    NR>1 {
      split($2, gpuArray, ":");
      nodes[$1] += $2;
      gpus[$1] += gpuArray[2];
      cpus[$1] += $3;
    }
    END {
      for (node in nodes) {
        print node, ('$gpuspernode' - gpus[node]), ('$cpuspernode' - cpus[node]);
      }
    }
  ' &&
  sinfo -p gpu --states=idle --noheader -o "%n %G %c" |
  grep -v -e "maint" -e "drain" -e "resv" |
  awk '{ gsub(/[^0-9]/, "", $2); print $1, $2, $3; }'
) | grep -F "$(sinfo -o "%n %G" | grep "gpu" | awk '{print $1}')" | column -t)

if [[ "$part" == "visu" ]]; then
    # Calculate total GPUs for the visu partition, considering $3
    read -r totalGpus < <(echo "$gpusinfo" | awk '$3 != 0 && index($1, "visu01") {visu_gpus += $2} END {print visu_gpus}')
elif [[ "$part" == "gpu" ]]; then
    # Calculate total GPUs for the gpu partition, considering $3
    read -r totalGpus < <(echo "$gpusinfo" | awk '$3 != 0 && !index($1, "visu01") {gpu_gpus += $2} END {print gpu_gpus}')
fi
# Output the totals in the required format: cpus,gpus
echo "$totalCpus,$totalGpus"