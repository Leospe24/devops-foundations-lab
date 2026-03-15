# Workstation Setup Guide

This module automates the deployment of the virtualized infrastructure used for the lab environment.

The goal is to create a **lightweight 3-node workstation** using Multipass to simulate a small infrastructure environment for practicing Linux, shell scripting, and automation workflows.

---

# 📋 Prerequisites

Before running the deployment script, ensure **Multipass** is installed on your Ubuntu host.

```bash
sudo snap install multipass
```

You can verify the installation with:

```bash
multipass version
```

---

# 🏗️ Lab Architecture

| Node Name    | RAM   | Role                                 |
| ------------ | ----- | ------------------------------------ |
| control-node | 1GB   | Management & Automation HQ           |
| web-node     | 512MB | Simulates a Web / Application Server |
| log-node     | 512MB | Centralized Log Storage              |

This architecture provides a **small but realistic multi-node environment** suitable for learning infrastructure concepts.

---

# 🚀 How to Use the Script

The `setup_fleet.sh` script automates the creation of the nodes and performs basic safety checks.

### 1. Set Script Permission

```bash
chmod +x setup_fleet.sh
```

### 2. Execute the Script

```bash
./setup_fleet.sh
```

The script will automatically deploy the nodes and display their status once deployment is complete.

---

# 🛠️ Script Features

The deployment script includes several safety and automation features:

- **Dependency Check**  
  Verifies that Multipass is installed before attempting deployment.

- **Safety Flags**  
  Uses `set -e` and `set -o pipefail` to ensure the script stops if errors occur.

- **Automation Loop**  
  Uses a loop to deploy multiple nodes efficiently.

- **Verification Output**  
  Displays the node list after deployment to confirm successful creation.

---

# 🔍 Verification

After running the script, you can verify the nodes manually using:

```bash
multipass list
```

This will display the **node name, state, IP address, and resource allocation**.

---

# 📁 Related Files

This module works alongside the following files:

```
setup_fleet.sh      # Infrastructure deployment script
journey.md          # High-level project progress log
```

---

# 🎯 Purpose of This Workstation

The workstation environment is used to:

- Practice Linux system administration
- Develop shell automation scripts
- Simulate multi-node infrastructure
- Build realistic DevOps learning scenarios
