# Journey Log

## Stage 1 — Building the Workstation (Current)

**Goal:** Establish a 3-node virtualized lab for safe experimentation.

**Detailed Documentation:**  
See `infrastructure/workstation/README.md` for the full setup process and architecture.

### Progress:

- [x] Defined lab architecture (Control, Web, Log nodes).
- [x] Configured GitHub repository structure.
- [x] Created `setup_fleet.sh` to automate node creation.
- [ ] Establish SSH "Handshake" (Trust) between nodes.

**Reflection:**  
Choosing Multipass over VirtualBox was a key decision to preserve 8GB RAM while maintaining a multi-node simulation.
