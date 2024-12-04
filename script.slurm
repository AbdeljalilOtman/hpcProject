#!/bin/bash


PARTITION=${PARTITION:-gpu}    
MIN_CPUS=${MIN_CPUS:-4}        
MIN_GPUS=${MIN_GPUS:-1}        
REFRESH_INTERVAL=${REFRESH_INTERVAL:-5}  


check_resources() {
    echo "Monitoring available resources in partition: $PARTITION..."
    echo "Press Ctrl+C to stop monitoring."

    
    trap 'echo "Stopping monitoring..."; exit 0' SIGINT

    
    while true; do
        
        sinfo -p $PARTITION -o "%N %c %G %T" | awk -v min_cpus=$MIN_CPUS -v min_gpus=$MIN_GPUS '
        BEGIN {
            idle_cpus = 0;
            idle_gpus = 0;
        }
        $4 == "idle" || $4 == "mixed" {  # Check nodes in idle or mixed state
            
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

        
        sleep $REFRESH_INTERVAL
    done
}


check_resources
