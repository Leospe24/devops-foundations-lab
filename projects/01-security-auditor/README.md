# Project 01: Security Auditor

## Overview

The Security Auditor is a multi-node security scanning tool that identifies identity risks and permission vulnerabilities across infrastructure. It simulates real-world security auditing scenarios in a controlled lab environment.

The auditor runs from the control-node, connects to worker nodes via SSH, collects user and file permission data, and generates a structured report with remediation commands.

## Project Objectives

- Audit system users across multiple nodes
- Detect suspicious or risky account configurations
- Identify privileged users
- Detect insecure file permissions
- Generate structured security reports with fix suggestions

## Infrastructure Context

This project operates within the lab infrastructure created in Phase 1.

### Lab Nodes

- **control-node**: Runs automation and audit scripts
- **web-node**: Simulates an application server
- **log-node**: Simulates centralized logging infrastructure

The control-node acts as the audit controller, collecting information from worker nodes using SSH.

## Prerequisites

Before running the Security Auditor, ensure:

- Phase 1 infrastructure is deployed and running
- SSH handshake is established between control-node and worker nodes
- You are inside the control-node shell

### Commands

```bash
multipass shell control-node
cd /path/to/projects/01-security-auditor
```

## Test Environment Setup

To validate the auditor, test users and insecure files were intentionally created across nodes. These represent real-world security risks.

### Web-Node Test Users

| User       | Description                      | Severity |
| ---------- | -------------------------------- | -------- |
| hacker-0   | Duplicate UID 0 account          | CRITICAL |
| deploy-svc | Service account with login shell | HIGH     |
| old-dev    | Expired/stale account            | MEDIUM   |
| web-user   | Regular user baseline            | INFO     |

### Web-Node Test Files

| File           | Permissions | Description           |
| -------------- | ----------- | --------------------- |
| .env           | 644         | Exposed credentials   |
| app_config.yml | 666         | World-writable config |
| id_rsa.bak     | 644         | Exposed SSH key       |
| safe_file.txt  | 600         | Control file (safe)   |

### Log-Node Test Users

| User          | Description                         | Severity             |
| ------------- | ----------------------------------- | -------------------- |
| patrick-admin | Privileged admin with sudo          | HIGH                 |
| temp-intern   | Temporary user                      | INFO                 |
| contractor-x  | Locked service account with nologin | INFO (best practice) |

### Log-Node Test Files

| File              | Permissions | Description             |
| ----------------- | ----------- | ----------------------- |
| debug.log         | 777         | World-writable log      |
| shadow_backup.old | 644         | Exposed password hashes |

## How to Run the Auditor

### Step 1: Enter Control-Node

```bash
multipass shell control-node
cd /path/to/projects/01-security-auditor
```

### Step 2: Run the Shell Auditor

```bash
chmod +x security_auditor.sh
./security_auditor.sh
```

This script:

- Connects to web-node and log-node via SSH
- Collects user account information
- Collects file permission data
- Saves raw output to `reports/audit_report_YYYYMMDD.txt`

### Step 3: Generate Final Report

```bash
python3 analyze_audit.py
```

This script:

- Finds the latest raw audit report
- Parses findings by node and severity
- Adds remediation commands
- Saves formatted report to `reports/final_audit_report_YYYYMMDD_HHMMSS.txt`

## Audit Capabilities

### Identity Inventory

- **Duplicate UID 0 accounts**: hacker-0 (UID 0 - duplicate root)
- **Service accounts with login shells**: deploy-svc (service account with login shell)
- **Expired/stale accounts**: old-dev (expired)
- **Privileged sudo users**: patrick-admin

### Permission Risks

- **World-writable files**: app_config.yml (666)
- **Exposed .env files**: .env (644)
- **Exposed SSH keys**: id_rsa.bak (644)
- **World-writable logs**: debug.log (777)
- **Exposed password hashes**: shadow_backup.old (644)

## Sample Output

```
================================================================================
SECURITY AUDIT REPORT WITH REMEDIATION
================================================================================
Generated: 2026-03-22 10:30:00
Source: audit_report_20260322.txt
================================================================================

================================================================================
NODE: WEB-NODE
================================================================================

[ USERS ]

→ hacker-0 (UID 0 - duplicate root)
SEVERITY: CRITICAL
FIX: sudo userdel hacker-0
NOTE: Unauthorized root account must be removed immediately

→ deploy-svc (service account with login shell: /bin/bash) UID: 1001
SEVERITY: HIGH
FIX: sudo usermod -s /usr/sbin/nologin deploy-svc
NOTE: Service accounts should not have interactive login shells

→ old-dev (expired: Jan 01, 2023)
SEVERITY: MEDIUM
FIX: sudo userdel old-dev
NOTE: Stale account expired: remove or re-enable with: sudo usermod -e "" old-dev

[ FILES & PERMISSIONS ]

→ -rw-rw-rw- 1 ubuntu ubuntu 0 Mar 21 18:05 /home/ubuntu/audit_test/app_config.yml
SEVERITY: MEDIUM
FIX: chmod 644 /home/ubuntu/audit_test/app_config.yml
NOTE: World-writable files can be modified by any system user

→ -rw-r--r-- 1 ubuntu ubuntu 27 Mar 21 18:08 /home/ubuntu/audit_test/.env
SEVERITY: HIGH
FIX: chmod 600 /home/ubuntu/audit_test/.env
NOTE: Environment files contain sensitive credentials like passwords and API keys

================================================================================
NODE: LOG-NODE
================================================================================

[ USERS ]

→ patrick-admin (regular user)
SEVERITY: INFO
FIX: No action needed
NOTE: Standard user account with normal permissions

→ contractor-x is properly locked with shell: /usr/sbin/nologin
SEVERITY: INFO
FIX: No action needed
NOTE: This service account is correctly configured with nologin shell

[ FILES & PERMISSIONS ]

→ -rwxrwxrwx 1 ubuntu ubuntu 0 Mar 21 18:13 /var/log/audit_test/debug.log
SEVERITY: MEDIUM
FIX: chmod 640 /var/log/audit_test/debug.log
NOTE: Log files should not be world-writable to prevent tampering

→ -rw-r--r-- 1 ubuntu ubuntu 0 Mar 21 18:13 /home/ubuntu/shadow_backup.old
SEVERITY: HIGH
FIX: sudo rm /home/ubuntu/shadow_backup.old
NOTE: Shadow file backups expose password hashes and should be deleted immediately

================================================================================
SUMMARY
================================================================================

Total Nodes Scanned: 2
CRITICAL Issues: 1
HIGH Issues: 3
MEDIUM Issues: 2
INFO: 4

================================================================================
AUDIT COMPLETE
================================================================================
```

## Scripts Overview

### security_auditor.sh (Shell)

**Purpose:** Collects raw audit data from all nodes.

**What it does:**

- Connects to web-node and log-node via SSH
- Runs user audit commands (UID 0, service shells, expired accounts, sudo users)
- Runs file permission checks (world-writable, .env, SSH keys, backups)
- Saves output to `reports/audit_report_YYYYMMDD.txt`

**Key commands used:**

#### User checks

```bash
awk -F: '$3 == 0 && $1 != "root" {print "CRITICAL: " $1 " (UID 0)"}' /etc/passwd
awk -F: '($3 < 1000 || $1 ~ /svc|service/) && $7 ~ /bash|sh/ {print "HIGH: " $1}' /etc/passwd
```

#### File checks

```bash
find /home -type f -perm -002 2>/dev/null
find /home -name ".env" -perm -004 2>/dev/null
```

### analyze_audit.py (Python)

**Purpose:** Parses raw audit data and generates remediation report.

**What it does:**

- Finds the latest raw audit report
- Parses nodes and sections (USERS, FILES)
- Classifies findings by severity (CRITICAL, HIGH, MEDIUM, INFO)
- Matches each finding to a remediation command
- Generates formatted final report with fix suggestions

**Key functions:**

- `parse_nodes_and_sections()` # Splits report by node and section
- `classify_finding()` # Determines severity
- `get_fix_suggestion()` # Returns remediation command
- `generate_final_report()` # Writes formatted output

## Project Structure

```
projects/01-security-auditor/
├── README.md # This documentation
├── security_auditor.sh # Shell data collector
├── analyze_audit.py # Python report generator
├── reports/
│ ├── audit_report_20260322.txt # Raw shell output
│ └── final_audit_report_20260322_*.txt # Formatted report
└── journey.md # Learning reflections
```

## Key Learning Outcomes

- **Linux Administration**: User management, file permissions, system commands
- **Shell Scripting**: SSH automation, command chaining, output redirection
- **Python**: File parsing, data structures, conditional logic
- **Security Auditing**: Risk classification, severity assessment, remediation
- **Multi-Node Automation**: SSH trust, cross-node data collection

## Key Commands Reference

### Find UID 0 duplicates

```bash
awk -F: '$3 == 0 && $1 != "root" {print $1}' /etc/passwd
```

### Find service accounts with login shells

```bash
awk -F: '($3 < 1000 || $1 ~ /svc|service/) && $7 ~ /bash|sh/ {print $1}' /etc/passwd
```

### Find expired accounts

```bash
chage -l username | grep 'Account expires' | grep -v never
```

### Find world-writable files

```bash
find /path -type f -perm -002 2>/dev/null
```

### Find exposed .env files

```bash
find /home -name ".env" -perm -004 2>/dev/null
```

### Fix file permissions

```bash
chmod 600 /path/to/file
```

### Disable service account login

```bash
usermod -s /usr/sbin/nologin username
```

## Next Steps

After completing the Security Auditor, proceed to:

- Phase 3: Resource Sentinel — Monitor infrastructure resources
- Phase 4: Infrastructure Dashboard — Visualize system health
- Phase 5: Infrastructure Enforcer — Enforce configuration consistency

## Related Documentation

- [Infrastructure Workstation Guide](../../infrastructure/workstation/README.md)
- [Journey Log](./journey.md)
- [DevOps Foundations Roadmap](../../README.md)
