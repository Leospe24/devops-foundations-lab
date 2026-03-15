#!/bin/bash

# Author: Patrick
# Description: Automates SSH key injection from control-node to worker nodes

set -e
set -o pipefail

echo "🔑 Fetching public key from control-node..."

# Ensure key exists
multipass exec control-node -- test -f /home/ubuntu/.ssh/id_rsa.pub || {
    echo "❌ SSH key not found on control-node. Generate it first."
    exit 1
}

# Fetch key
PUB_KEY=$(multipass exec control-node -- cat /home/ubuntu/.ssh/id_rsa.pub)

# Target nodes
NODES=("web-node" "log-node")

# Inject key
for NODE in "${NODES[@]}"; do
    echo "📡 Injecting key into $NODE..."

    multipass exec "$NODE" -- bash -c "
        mkdir -p ~/.ssh
        chmod 700 ~/.ssh
        grep -qxF '$PUB_KEY' ~/.ssh/authorized_keys || echo '$PUB_KEY' >> ~/.ssh/authorized_keys
        chmod 600 ~/.ssh/authorized_keys
    "

    echo "✅ $NODE is now trusted by control-node."
done

echo "🎉 All handshakes complete!"