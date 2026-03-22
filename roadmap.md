# 🗺️ DevOps Foundations Roadmap

## 🎯 The Vision

Build a **fully automated multi-node lab environment** that simulates a small data center.

The objective is to practice:

- Linux system administration
- Shell scripting automation
- Python-based tooling
- Infrastructure monitoring
- Security auditing
- Cross-node automation
- Infrastructure reporting

The lab environment consists of a **3-node infrastructure**:

- control-node (automation control center)
- web-node (simulated application server)
- log-node (centralized logging & analysis)

**📁 Infrastructure Setup:** [infrastructure/workstation/README.md](./infrastructure/workstation/README.md)

---

# 🏁 Phase 1 — Infrastructure & Handshake ✅

Establish the foundation of the lab environment.

Focus areas:

- Infrastructure provisioning
- SSH automation
- Node verification
- Documentation standards

### Tasks

- [x] Create GitHub Repository & Documentation Standards
- [x] Deploy 3-node Multipass Fleet
- [x] Configure SSH Key-based Authentication
- [x] Script: Infrastructure Connectivity Verification

### Result

A **fully operational multi-node environment** where the control-node can securely execute commands across all worker nodes.

**📁 Detailed Guide:** [infrastructure/workstation/README.md](./infrastructure/workstation/README.md)

---

# 🔐 Phase 2 — Project: The Security Auditor ✅

Build a tool that audits infrastructure security risks across nodes.

Focus areas:

- Linux user management
- File permission auditing
- Security reporting
- Remediation guidance

### Tasks

- [x] Create Test Users & Risky File Scenarios
- [x] Audit System Users Across Nodes (Shell)
- [x] Detect Permission Risks & World-Writable Files (Shell)
- [x] Generate Automated Security Audit Report (Python)
- [x] Add Remediation Suggestions to Report

### Result

A **multi-node security scanner** that identifies identity risks, permission vulnerabilities, and generates a structured report with actionable fix commands.

**📁 Project Details:** [projects/01-security-auditor/README.md](./projects/01-security-auditor/README.md)

---

# 🛰️ Phase 3 — Project: The Resource Sentinel

Goal: Monitor infrastructure resources and automate maintenance tasks.

Focus areas:

- System monitoring
- Resource inspection
- Log maintenance
- Backup automation

### Tasks

- [ ] Collect Disk, Memory, and CPU Metrics (Shell)
- [ ] Implement Log Archive & Cleanup Logic (Python)
- [ ] Automate Cross-node Backup Execution

### Result

A lightweight **infrastructure monitoring and maintenance system**.

---

# 📊 Phase 4 — Project: The Infrastructure Dashboard

Goal: Create a simple observability system that visualizes infrastructure health.

Focus areas:

- Multi-node data aggregation
- Infrastructure reporting
- Visualization

### Tasks

- [ ] Implement Multi-node Data Collection
- [ ] Generate HTML Infrastructure Dashboard (Python)
- [ ] Automate Monitoring via Cron Scheduling

### Result

A **dashboard displaying real-time infrastructure status**.

---

# ⚙️ Phase 5 — Project: The Infrastructure Enforcer

Goal: Ensure all nodes maintain a consistent configuration baseline.

Focus areas:

- Infrastructure standardization
- Configuration drift detection
- Automated environment enforcement

### Tasks

- [ ] Verify Required Packages Across Nodes
- [ ] Check and Maintain Critical Services
- [ ] Detect Configuration Drift Between Nodes

### Result

A system that **automatically enforces infrastructure consistency across nodes**.

---

# 📚 Related Documentation

| Document                                                       | Purpose                                         |
| -------------------------------------------------------------- | ----------------------------------------------- |
| [Journey Log](./journey.md)                                    | Lessons learned and reflections from each phase |
| [Infrastructure Setup](./infrastructure/workstation/README.md) | Detailed guide for building the 3-node lab      |
| [Security Auditor](./projects/01-security-auditor/README.md)   | Complete project documentation                  |

---

# 🧠 Learning Outcomes

By completing this roadmap, the lab will demonstrate experience with:

- Linux system administration
- Shell scripting automation
- Python automation
- Infrastructure monitoring
- Security auditing
- Cross-node orchestration
- Configuration management concepts

The completed lab will simulate **real-world DevOps infrastructure workflows in a controlled environment**.
