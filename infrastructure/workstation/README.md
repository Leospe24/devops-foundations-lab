# Workstation Setup Guide

This module automates the deployment of the virtualized infrastructure used for the lab environment.

The goal is to create a **lightweight 3-node workstation** using Multipass to simulate a small infrastructure environment for practicing Linux, shell scripting, and automation workflows.

---

# 📋 Prerequisites

Before running the deployment scripts, ensure **Multipass** is installed on your Ubuntu host.

```bash
sudo snap install multipass
```

Verify installation:

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

# 🚀 Step 1 — Deploy the Infrastructure

The `setup_fleet.sh` script automatically creates the three nodes.

### Set script permissions

```bash
chmod +x setup_fleet.sh
```

### Run the deployment

```bash
./setup_fleet.sh
```

After execution, verify the nodes:

```bash
multipass list
```

Expected output:

```
control-node
web-node
log-node
```

---

# 🤝 Step 2 — Establish SSH Handshake

To enable automation, the **control-node must trust the worker nodes**.  
This is done by installing the control-node's **SSH public key** on the other nodes.

Instead of performing this manually, the process is automated using:

```
automate_handshake.sh
```

This script:

1. Retrieves the SSH public key from `control-node`
2. Installs the key on `web-node`
3. Installs the key on `log-node`
4. Configures correct SSH permissions

---

# ▶️ Run the Handshake Script

From the **host machine**, navigate to the workstation directory:

```bash
cd infrastructure/workstation
```

Make the script executable:

```bash
chmod +x automate_handshake.sh
```

Run the script:

```bash
./automate_handshake.sh
```

Expected output:

```
Fetching public key from control-node...
Injecting key into web-node...
Injecting key into log-node...
All handshakes complete!
```

---

# 🔍 Verification

Enter the control-node:

```bash
multipass shell control-node
```

Test SSH connectivity:

```bash
ssh ubuntu@web-node
```

```bash
ssh ubuntu@log-node
```

Successful login **without password prompts** confirms the handshake was successful.

---

# 🛠️ Script Features

### setup_fleet.sh

- Dependency check for Multipass
- Automated node creation
- Resource allocation
- Deployment verification

### automate_handshake.sh

- Retrieves SSH key from control-node
- Injects key into worker nodes
- Ensures correct `.ssh` permissions
- Enables passwordless SSH access

---

# 📁 Related Files

```
setup_fleet.sh
automate_handshake.sh
journey.md
```

---

# 🎯 Purpose of This Workstation

This workstation environment is used to:

- Practice Linux system administration
- Develop shell automation scripts
- Simulate multi-node infrastructure
- Build realistic DevOps learning scenarios
