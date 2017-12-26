#!/bin/bash

PORT=$1 || 8080
P=$(lsof -i:$PORT -t)
set -f;PIDS=(${P})
for PID in ${PIDS[@]}
do
    echo "Current Process with ID $PID is being killed"
    kill $PID
done
