# DevOps Foundations Hybrid Lab

A comprehensive journey into Linux, Python automation, and Shell scripting.  
This lab uses a 3-node virtualized environment to simulate real-world DevOps tasks.

---

## 📖 Before You Start

New to this lab? Start here:

- **[Roadmap](./roadmap.md)** — Overview of all phases and what you'll build
- **[Journey Log](./journey.md)** — Lessons learned and reflections along the way

These documents will help you understand the big picture before diving into the code.

---

## 🏗️ Lab Architecture

A 3-node virtualized environment that forms the foundation for all projects:

- **control-node**: Automation HQ (Python & Shell)
- **web-node**: Managed Web Server (simulates application server)
- **log-node**: Centralized Logging & Backups

**📁 Detailed Setup:** See [infrastructure/workstation/README.md](./infrastructure/workstation/README.md) for deployment instructions, SSH handshake, and verification steps.

---

## 🚀 Projects

Each project builds on the previous one, adding new skills and automation patterns.

### 1. Security Auditor

Automated user and permission scanning across all nodes.  
Detects duplicate root accounts, service shells, expired users, and insecure file permissions.  
Generates a structured report with remediation commands.

**📁 Details:** [projects/01-security-auditor/README.md](./projects/01-security-auditor/README.md)

---

### 2. Resource Sentinel _(Planned)_

System health monitoring and automated cleanup.  
Collects disk, memory, and CPU metrics.  
Automates log rotation and cross-node backups.

---

### 3. Health Dashboard _(Planned)_

Multi-node connectivity and status visualization.  
Aggregates system metrics into a simple dashboard.

---

### 4. Log Centralizer _(Planned)_

Cross-node log aggregation and analysis.  
Centralizes logs from all nodes for easier troubleshooting.

---

## 🧭 How to Navigate This Repository

| Path                                 | What You'll Find                             |
| ------------------------------------ | -------------------------------------------- |
| [infrastructure/](./infrastructure/) | Setup scripts for the 3-node lab environment |
| [projects/](./projects/)             | All project code and documentation           |
| [roadmap.md](./roadmap.md)           | High-level plan and learning objectives      |
| [journey.md](./journey.md)           | Personal reflections and lessons learned     |

---

## 🎯 Prerequisites

- Multipass installed on Ubuntu host
- Basic familiarity with Linux command line
- Curiosity to build and break things

---

## 📚 Learning Outcomes

By completing this lab, you will demonstrate experience with:

- Linux system administration
- Shell scripting automation
- Python tooling
- Multi-node orchestration
- Security auditing
- Infrastructure monitoring

---

## 🧪 Ready to Start?

1. Read the **[Roadmap](./roadmap.md)** to understand the journey
2. Follow the **[Infrastructure Setup](./infrastructure/workstation/README.md)** to build your lab
3. Explore the **[Security Auditor](./projects/01-security-auditor/README.md)** to see the first project in action
4. Check the **[Journey Log](./journey.md)** for insights and lessons learned

Happy building! 🚀
