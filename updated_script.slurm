#!/bin/bash

# Default values (can be overridden by environment variables or arguments)
PARTITION=${PARTITION:-gpu}    # Partition to check (default: GPU partition)
MIN_CPUS=${MIN_CPUS:-4}        # Minimum number of idle CPUs required
MIN_GPUS=${MIN_GPUS:-1}        # Minimum number of idle GPUs required
REFRESH_INTERVAL=${REFRESH_INTERVAL:-5}  # Time (in seconds) between checks

# Function to check resources in real time
check_resources() {
    echo "Monitoring available resources in partition: $PARTITION..."
    echo "Press Ctrl+C to stop monitoring."

    # Trap to gracefully handle termination
    trap 'echo "Stopping monitoring..."; exit 0' SIGINT

    # Infinite loop to monitor resources
    while true; do
        # Get the total number of idle CPUs and GPUs in the specified partition
        sinfo -p $PARTITION -o "%N %c %G %T" | awk -v min_cpus=$MIN_CPUS -v min_gpus=$MIN_GPUS '
        BEGIN {
            idle_cpus = 0;
            idle_gpus = 0;
        }
        $4 == "idle" || $4 == "mixed" {  # Check nodes in idle or mixed state
            # Sum up CPUs and GPUs for idle/mixed nodes
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

        # Wait for the refresh interval
        sleep $REFRESH_INTERVAL
    done
}

# Run the resource monitoring function
check_resources

