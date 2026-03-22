# 📝 Journey Log

## Stage 1 — Building the Workstation (Complete)

**Goal:** Establish a 3-node virtualized lab for safe experimentation.

### Progress

- [x] Deployed 3-node Multipass fleet (control-node, web-node, log-node)
- [x] Configured SSH key-based authentication between nodes
- [x] Created `setup_fleet.sh` and `automate_handshake.sh`

### Reflection

Multipass enabled a lightweight lab on 8GB RAM. SSH trust established passwordless automation from control-node to workers, forming the foundation for all future projects.

---

## Stage 2 — Security Auditor (Complete)

**Goal:** Build a multi-node scanner to detect identity and permission risks.

### Progress

- [x] Created test users: `hacker-0` (UID 0), `deploy-svc` (service shell), `old-dev` (expired)
- [x] Created test files: `.env` (644), `app_config.yml` (666), `id_rsa.bak` (644), `debug.log` (777)
- [x] Built `security_auditor.sh` to collect user/file data across nodes
- [x] Built `analyze_audit.py` to classify findings and generate fix commands

### Reflection

**Separation of concerns** proved valuable: shell handled SSH/system commands, Python handled parsing and reporting. **Severity classification** (CRITICAL/HIGH/MEDIUM/INFO) helped prioritize remediation. **Actionable reporting** with exact fix commands made the output immediately useful. **Test data** validated detection before automation.

### Key Skills

- Multi-node SSH automation
- User and permission auditing
- Shell-to-Python data handoff
- Remediation-first reporting

---

## Stage 3 — Resource Sentinel (Planned)

**Goal:** Monitor infrastructure resources and automate maintenance.

### Next Steps

- Collect disk, memory, and CPU metrics across nodes
- Implement log archive and cleanup automation
- Automate cross-node backup execution

---

## Stage 4 — Infrastructure Dashboard (Planned)

**Goal:** Visualize infrastructure health through a dashboard.

### Next Steps

- Aggregate multi-node metrics
- Generate HTML dashboard
- Schedule automated monitoring

---

## Stage 5 — Infrastructure Enforcer (Planned)

**Goal:** Maintain consistent configuration across all nodes.

### Next Steps

- Verify required packages
- Check critical services
- Detect and correct configuration drift
