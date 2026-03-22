#!/bin/bash

################################################################################
# Script Name:  security_auditor.sh
# Author:       [Patrick]
# Date:         2026-03-21
# Description:  Multi-node security scanner for Identity (Users/Groups) 
#               and Access (File Permissions) risks.
# Version:      1.0 (Phase 2 - Identity & Access)
################################################################################

# --- SAFETY SETTINGS ---
set -e          # Exit immediately if a command fails
set -u          # Exit if an unset variable is used
set -o pipefail # Exit if any command in a pipe fails

# --- CONTROL-NODE CHECK ---
if [ "$(hostname)" != "control-node" ]; then
    # Get the absolute path of the script even if run from outside
    SCRIPT_PATH=$(realpath "$0")
    
    echo "------------------------------------------------"
    echo "❌ ERROR: WRONG ENVIRONMENT"
    echo "This script must run INSIDE the control-node."
    echo "------------------------------------------------"
    echo "Step 1: multipass shell control-node"
    echo "Step 2: cd $(dirname "$SCRIPT_PATH")"
    echo "Step 3: ./$(basename "$0")"
    echo "------------------------------------------------"
    exit 1
fi
# --- TARGET NODES ---
WEB_NODE="ubuntu@web-node"
LOG_NODE="ubuntu@log-node"

# --- SSH COMMAND PREFIXES ---
WEB_SSH="ssh $WEB_NODE"
LOG_SSH="ssh $LOG_NODE"

# --- AUDIT SETTINGS ---
mkdir -p reports
REPORT_FILE="reports/audit_report_$(date +%Y%m%d).txt"

# Create/Clear the file before starting
> "$REPORT_FILE"



# --- HEADER ---
echo "------------------------------------------------" | tee -a "$REPORT_FILE"
echo "        SECURITY AUDIT REPORT - $(date)       " | tee -a "$REPORT_FILE"
echo "------------------------------------------------" | tee -a "$REPORT_FILE"

# ============================================================================
# SECTION 1: WEB-NODE AUDIT
# ============================================================================

# --- WEB-NODE USER AUDIT ---
echo "" | tee -a "$REPORT_FILE"
echo "[+] Starting Audit on: $WEB_NODE" | tee -a "$REPORT_FILE"
echo "========================================" | tee -a "$REPORT_FILE"

# 1. UID 0 (Critical) - Exclude root itself
echo "Checking for unauthorized Root (UID 0) accounts..." | tee -a "$REPORT_FILE"
$WEB_SSH "awk -F: '\$3 == 0 && \$1 != \"root\" {print \"CRITICAL: \" \$1 \" (UID 0 - duplicate root)\"}' /etc/passwd" | tee -a "$REPORT_FILE"

# 2. Service accounts with login shells (High)
echo "Checking for service accounts with login shells..." | tee -a "$REPORT_FILE"
$WEB_SSH "awk -F: '\$3 > 0 && (\$3 < 1000 || \$1 ~ /svc|service|daemon/) && \$7 ~ /bash|sh/ {print \"HIGH: \" \$1 \" (service account with login shell: \" \$7 \") UID: \" \$3}' /etc/passwd" | tee -a "$REPORT_FILE"

# 3. Expired/stale accounts (Medium) - Shows expiry date
echo "Checking for expired accounts..." | tee -a "$REPORT_FILE"
$WEB_SSH "for user in \$(awk -F: '\$3 >= 1000 {print \$1}' /etc/passwd); do expiry=\$(sudo chage -l \$user 2>/dev/null | grep 'Account expires' | cut -d: -f2 | sed 's/^ //'); if [ \"\$expiry\" != \"never\" ] && [ \"\$expiry\" != \"\" ]; then echo \"MEDIUM: \$user (expired: \$expiry)\"; fi; done" | tee -a "$REPORT_FILE"

# 4. Sudo users (Info)
echo "Checking for sudo/administrative users..." | tee -a "$REPORT_FILE"
$WEB_SSH "getent group sudo 2>/dev/null | cut -d: -f4 | tr ',' '\n'" | tee -a "$REPORT_FILE"

# --- WEB-NODE FILE PERMISSION AUDIT ---
echo "" | tee -a "$REPORT_FILE"
echo "[+] File Permission Audit on: $WEB_NODE" | tee -a "$REPORT_FILE"
echo "----------------------------------------" | tee -a "$REPORT_FILE"

# 1. World-writable files (Medium)
echo "Checking for world-writable files..." | tee -a "$REPORT_FILE"
$WEB_SSH "find /home/ubuntu/audit_test -type f -perm -002 2>/dev/null -exec ls -l {} \;" | tee -a "$REPORT_FILE"

# 2. Exposed .env files (High)
echo "Checking for exposed .env files..." | tee -a "$REPORT_FILE"
$WEB_SSH "find /home/ubuntu/audit_test -name '.env' -perm -004 2>/dev/null -exec ls -l {} \;" | tee -a "$REPORT_FILE"

# 3. Exposed SSH keys/backups (High)
echo "Checking for exposed SSH keys or backups..." | tee -a "$REPORT_FILE"
$WEB_SSH "find /home/ubuntu/audit_test \( -name '*.bak' -o -name 'id_rsa*' \) -perm -004 2>/dev/null -exec ls -l {} \;" | tee -a "$REPORT_FILE"

# ============================================================================
# SECTION 2: LOG-NODE AUDIT
# ============================================================================

# --- LOG-NODE USER AUDIT ---
echo "" | tee -a "$REPORT_FILE"
echo "[+] Starting Audit on: $LOG_NODE" | tee -a "$REPORT_FILE"
echo "========================================" | tee -a "$REPORT_FILE"

# 1. Privileged users (sudo group) (High)
echo "Checking for privileged (sudo) users..." | tee -a "$REPORT_FILE"
$LOG_SSH "getent group sudo 2>/dev/null | cut -d: -f4 | tr ',' '\n'" | tee -a "$REPORT_FILE"

# 2. Standard users (UID >= 1000 with login shell) (Info)
echo "Checking for standard users..." | tee -a "$REPORT_FILE"
$LOG_SSH "awk -F: '\$3 >= 1000 && \$7 ~ /bash|sh/ {print \"INFO: \" \$1 \" (regular user)\"}' /etc/passwd" | tee -a "$REPORT_FILE"

# 3. Best Practice Check: Locked Accounts (Info)
echo "Verifying locked service accounts (nologin)..." | tee -a "$REPORT_FILE"
$LOG_SSH "grep 'contractor-x' /etc/passwd | awk -F: '\$7 ~ /nologin/ {print \"CONFIRMED: \" \$1 \" is properly locked with shell: \" \$7}'" | tee -a "$REPORT_FILE"

# --- LOG-NODE FILE PERMISSION AUDIT ---
echo "" | tee -a "$REPORT_FILE"
echo "[+] File Permission Audit on: $LOG_NODE" | tee -a "$REPORT_FILE"
echo "----------------------------------------" | tee -a "$REPORT_FILE"

# 1. World-writable log files (Medium)
echo "Checking for world-writable log files..." | tee -a "$REPORT_FILE"
$LOG_SSH "find /var/log/audit_test -type f -perm -002 2>/dev/null -exec ls -l {} \;" | tee -a "$REPORT_FILE"

# 2. Exposed backup files (High)
echo "Checking for exposed backup files..." | tee -a "$REPORT_FILE"
$LOG_SSH "find /home/ubuntu -name 'shadow_backup.old' -perm -004 2>/dev/null -exec ls -l {} \;" | tee -a "$REPORT_FILE"

# ============================================================================
# FOOTER
# ============================================================================
echo "" | tee -a "$REPORT_FILE"
echo "------------------------------------------------" | tee -a "$REPORT_FILE"
echo "        AUDIT COMPLETE - $(date)              " | tee -a "$REPORT_FILE"
echo "------------------------------------------------" | tee -a "$REPORT_FILE"
echo "Report saved to: $REPORT_FILE" | tee -a "$REPORT_FILE"