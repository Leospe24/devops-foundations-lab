#!/bin/bash

# Author: Patrick
# Description: Infrastructure Smoke Test to verify Node Connectivity
# Date: 15/03/2026

# Colors for better readability
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

TARGETS=("web-node" "log-node")

echo -e "${BLUE}🚀 Starting Infrastructure Smoke Test...${NC}"
echo "-----------------------------------------------"

for node in "${TARGETS[@]}"; do
    echo -e "Testing connection to: ${GREEN}$node${NC}"
    
    # Run a block of commands remotely over SSH
    ssh -o ConnectTimeout=5 ubuntu@$node << 'EOF'
    echo -n "  👤 User: " && whoami
    echo -n "  🏠 Hostname: " && hostname
    echo -n "  📅 Date/Time: " && date
EOF

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $node is fully reachable and responsive.${NC}"
    else
        echo -e "\033[0;31m❌ $node failed the smoke test. Check IP and SSH keys.\033[0m"
    fi
    echo "-----------------------------------------------"
done

echo -e "${BLUE}Test Complete.${NC}"