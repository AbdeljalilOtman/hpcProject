#!/bin/bash

# Default values (can be overridden by environment variables or arguments)
PARTITION=${PARTITION:-gpu}          # Partition to check (default: "gpu")
MIN_CPUS=${MIN_CPUS:-4}              # Minimum number of idle CPUs required
MIN_GPUS=${MIN_GPUS:-1}              # Minimum number of idle GPUs required
REFRESH_INTERVAL=${REFRESH_INTERVAL:-5}  # Time (in seconds) between checks

# Function to check if required commands are available
check_commands() {
    for cmd in sinfo awk; do
        if ! command -v "$cmd" &> /dev/null; then
            echo "Error: Command '$cmd' not found. Please install it before running the script."
            exit 1
        fi
    done
}

# Function to validate inputs
validate_inputs() {
    if ! [[ $MIN_CPUS =~ ^[0-9]+$ ]] || [[ $MIN_CPUS -lt 1 ]]; then
        echo "Error: MIN_CPUS must be a positive integer."
        exit 1
    fi
    if ! [[ $MIN_GPUS =~ ^[0-9]+$ ]] || [[ $MIN_GPUS -lt 0 ]]; then
        echo "Error: MIN_GPUS must be a non-negative integer."
        exit 1
    fi
    if ! [[ $REFRESH_INTERVAL =~ ^[0-9]+$ ]] || [[ $REFRESH_INTERVAL -lt 1 ]]; then
        echo "Error: REFRESH_INTERVAL must be a positive integer."
        exit 1
    fi
}

# Function to check resources in real time
check_resources() {
    echo "Monitoring available resources in partition: $PARTITION..."
    echo "Minimum CPUs: $MIN_CPUS | Minimum GPUs: $MIN_GPUS"
    echo "Refresh interval: $REFRESH_INTERVAL seconds"
    echo "Press Ctrl+C to stop monitoring."

    # Trap to gracefully handle termination
    trap 'echo "Stopping monitoring..."; exit 0' SIGINT

    # Infinite loop to monitor resources
    while true; do
        sinfo -p "$PARTITION" -o "%N %c %G %T" 2>/dev/null | awk -v min_cpus="$MIN_CPUS" -v min_gpus="$MIN_GPUS" '
        BEGIN {
            idle_cpus = 0;
            idle_gpus = 0;
        }
        $4 == "idle" || $4 == "mixed" {
            idle_cpus += $2;
            if ($3 ~ /gpu:/) {
                split($3, g, ":");
                idle_gpus += g[2];
            }
        }
        END {
            print "-----------------------------";
            print "Available Idle CPUs: " idle_cpus;
            print "Available Idle GPUs: " idle_gpus;
            print "-----------------------------";

            if (idle_cpus >= min_cpus && idle_gpus >= min_gpus) {
                print "Sufficient resources are available.";
            } else {
                print "Insufficient resources.";
            }
        }'
        
        # Check if sinfo command or awk parsing failed
        if [[ $? -ne 0 ]]; then
            echo "Error: Unable to fetch partition information. Please verify the partition name and SLURM configuration."
            exit 1
        fi
        
        sleep "$REFRESH_INTERVAL"
    done
}

# Run checks and start monitoring
check_commands
validate_inputs
check_resources
