#!/bin/bash

# Author: Patrick
# Description: Script to create 3 workstation or node (control, web, log)
# Date: 15/03/2025

set -e
set -o pipefail

# Variables
MEM_SMALL="512M"
MEM_LARGE="1G"
NODES=("control-node" "web-node" "log-node")

# Check if multipass is installed
if ! command -v multipass &> /dev/null
then
    echo "Error: Multipass not installed. Run: sudo snap install multipass"
    exit 1
fi

echo "Starting Fleet Deployment..."

# Creating nodes
for node in "${NODES[@]}"; do

  if multipass list | grep -q "$node"; then
      echo "$node already exists. Skipping..."
      continue
  fi

  echo "Deploying $node..."

  if [ "$node" = "control-node" ]; then
      multipass launch --name "$node" --cpus 1 --memory "$MEM_LARGE"
  else
      multipass launch --name "$node" --cpus 1 --memory "$MEM_SMALL"
  fi

done

echo "Deployment complete"

multipass list