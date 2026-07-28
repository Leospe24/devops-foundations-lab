# DevOps Foundations Hybrid Lab

A hands-on Linux, Bash, and Python automation lab built on a 3-node virtualized environment.  
Designed to practice real-world DevOps workflows from first principles — before moving to the cloud.

---

## 🏗️ Lab Architecture

A 3-node Multipass fleet simulating a small data center:

```
control-node  ──SSH──►  web-node   (simulated application server)
              ──SSH──►  log-node   (simulated centralized logging)
```

- **control-node** — Automation HQ: runs all scripts and orchestrates worker nodes
- **web-node** — Simulated application server (managed target)
- **log-node** — Centralized logging and backup target

SSH key-based trust is established from control-node to all workers, enabling passwordless cross-node automation.

**📁 Infrastructure Setup:** [infrastructure/workstation/README.md](./infrastructure/workstation/README.md)

---

## ✅ What's Built

### Phase 1 — Infrastructure & Handshake

Established the foundation of the lab environment.

- Deployed 3-node Multipass fleet (control-node, web-node, log-node)
- Configured SSH key-based authentication between all nodes
- Scripted infrastructure connectivity verification (`setup_fleet.sh`, `automate_handshake.sh`)

**Result:** A fully operational multi-node environment where control-node executes commands across all workers without manual authentication.

---

### Phase 2 — Security Auditor

**📁 Project:** [projects/01-security-auditor/](./projects/01-security-auditor/)

A multi-node security scanner that detects identity and permission risks across all nodes.

**`security_auditor.sh` (Bash):**
- SSH-connects to each worker node and collects raw audit data
- Detects: duplicate UID 0 accounts, service accounts with login shells, expired/stale users, world-writable files, exposed `.env` files, exposed SSH keys

**`analyze_audit.py` (Python):**
- Parses shell output, classifies findings by severity
- Maps each finding to a remediation command
- Generates a structured report with node-by-node breakdown

**Severity classification:**

| Finding | Severity | Remediation |
|---|---|---|
| Duplicate UID 0 account | CRITICAL | `sudo userdel hacker-0` |
| Service account with login shell | HIGH | `sudo usermod -s /usr/sbin/nologin` |
| `.env` file with 644 permissions | HIGH | `chmod 600 .env` |
| World-writable log file (777) | MEDIUM | `chmod 640 debug.log` |

**Result:** A multi-node security scanner that identifies identity risks and permission vulnerabilities, generating a structured report with actionable fix commands.

---

## 🔑 Key Skills Demonstrated

- **Multi-node SSH orchestration** — SSH key-based trust across a fleet; control-node drives all worker operations
- **Bash scripting** — Cross-node data collection, system checks, and automation
- **Python automation** — Log parsing, severity classification, remediation-first reporting
- **Security auditing** — Linux user management, file permission auditing, defense-in-depth test scenarios
- **Separation of concerns** — Shell handles SSH/system commands; Python handles parsing and structured output

---

## ☁️ Cloud Evolution

The infrastructure patterns built in this lab were taken to production in two cloud projects:

### [OpsTicket — Cloud Infrastructure Platform](https://github.com/Leospe24/ops-ticket-devops-lab)
The 3-node lab architecture maps directly to OpsTicket's AWS deployment:

| Lab Simulation | OpsTicket Cloud Equivalent |
|---|---|
| 3 Multipass nodes (control/web/log) | ECS Fargate containers in private subnets |
| SSH cross-node communication | ALB + VPC private subnet networking |
| Manual log collection | CloudWatch Logs (`/ecs/opsticket`) |
| Infrastructure scripts | Terraform IaC + GitHub Actions CI/CD |

### [SRE Assistant — AIOps Incident Pipeline](https://github.com/Leospe24/sre-assistant)
The monitoring and alerting concepts from this lab (resource collection, log analysis, reporting) evolved into a serverless cloud pipeline:

| Lab Concept | SRE Assistant Cloud Equivalent |
|---|---|
| Resource Sentinel (metrics collection) | CloudWatch Subscription Filters |
| Infrastructure Dashboard (HTML report) | Slack Block Kit incident reports |
| Manual alerting | Amazon Bedrock AI root-cause + automated Slack notifications |

---

## 📁 Repository Structure

| Path | What You'll Find |
|---|---|
| [infrastructure/](./infrastructure/) | Setup scripts for the 3-node Multipass fleet |
| [projects/01-security-auditor/](./projects/01-security-auditor/) | Security Auditor — Bash + Python multi-node scanner |

---

## 🎯 Prerequisites

- Multipass installed on Ubuntu host
- Basic familiarity with Linux command line

---

## 🔭 What's Next

- **Resource Sentinel** — Collect disk, memory, and CPU metrics across nodes; automate log rotation and cross-node backups
- **Infrastructure Dashboard** — Aggregate multi-node metrics into an HTML dashboard via cron
- **Infrastructure Enforcer** — Detect and correct configuration drift across all nodes
