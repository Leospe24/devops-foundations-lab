# Journey Log

## Stage 1 — Building the Workstation (Current)

**Goal:** Establish a 3-node virtualized lab for safe experimentation.

**Detailed Documentation:**  
See `infrastructure/workstation/README.md` for the full setup process and architecture.

### Progress

- [x] Defined lab architecture (Control, Web, Log nodes)
- [x] Configured GitHub repository structure
- [x] Created `setup_fleet.sh` to automate node creation
- [x] Established SSH "Handshake" (Trust) between nodes using `setup_ssh_trust.sh`

### Reflection

Choosing **Multipass** instead of heavier virtualization platforms allowed the lab to run efficiently on an **8GB RAM system** while still simulating a realistic multi-node infrastructure.

The SSH handshake step establishes **passwordless communication from the control-node to worker nodes**, enabling future automation tasks such as remote command execution and configuration management.
