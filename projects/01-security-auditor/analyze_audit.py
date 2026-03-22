#!/usr/bin/env python3
"""
Security Audit Report Analyzer
Parses the output from security_auditor.sh and generates a formatted report with fix suggestions
Follows the exact structure of the original audit report
"""

import sys
from pathlib import Path
from datetime import datetime


# ============================================================================
# 1. FILE & DIRECTORY UTILITIES
# ============================================================================

def find_latest_report(report_dir="reports"):
    """Find the most recent audit report file"""
    report_path = Path(report_dir)
    
    if not report_path.exists():
        print(f"Error: Reports directory '{report_dir}' not found")
        return None
    
    report_files = list(report_path.glob("audit_report_*.txt"))
    
    if not report_files:
        print(f"No audit report files found in '{report_dir}'")
        return None
    
    latest_file = max(report_files, key=lambda f: f.stat().st_mtime)
    print(f"Found latest report: {latest_file}")
    return latest_file


def read_audit_file(filepath):
    """Read the audit report file"""
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        print(f"Read {len(lines)} lines from {filepath.name}")
        return lines
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


# ============================================================================
# 2. PARSING & CLASSIFICATION LOGIC
# ============================================================================

def parse_nodes_and_sections(lines):
    """
    Parse the audit report into nodes and sections (Users vs Files)
    Returns a structured dictionary
    """
    nodes = {}
    current_node = None
    current_section = None
    current_lines = []
    
    for line in lines:
        line_stripped = line.strip()
        
        # Detect node start (User Audit)
        if "[+] Starting Audit on: ubuntu@" in line:
            # Save previous node/section if exists
            if current_node and current_section and current_lines:
                if current_node not in nodes:
                    nodes[current_node] = {"USERS": [], "FILES": []}
                nodes[current_node][current_section].extend(current_lines)
            
            # Start new node
            current_node = line.split("ubuntu@")[1].strip()
            current_section = "USERS"
            current_lines = []
            continue
        
        # Detect File Permission Audit section
        if "[+] File Permission Audit on: ubuntu@" in line:
            # Save previous section
            if current_node and current_section and current_lines:
                if current_node not in nodes:
                    nodes[current_node] = {"USERS": [], "FILES": []}
                nodes[current_node][current_section].extend(current_lines)
            
            current_section = "FILES"
            current_lines = []
            continue
        
        # Collect lines for current section
        if current_node and current_section:
            current_lines.append(line_stripped)
    
    # Save the last section
    if current_node and current_section and current_lines:
        if current_node not in nodes:
            nodes[current_node] = {"USERS": [], "FILES": []}
        nodes[current_node][current_section].extend(current_lines)
    
    print(f"Found {len(nodes)} nodes: {', '.join(nodes.keys())}")
    return nodes


def classify_finding(line, section):
    """
    Determine severity and extract finding details
    """
    line = line.strip()
    
    # Skip empty lines and separators
    if not line or line.startswith("==") or line.startswith("--"):
        return None
    
    # Skip check headers
    if line.startswith("Checking for"):
        return None
    
    # Skip sudo users output (these are not findings)
    if line == "ubuntu" and "sudo" in section.lower():
        return None
    
    # CRITICAL findings
    if "CRITICAL:" in line:
        return {
            "severity": "CRITICAL",
            "finding": line.replace("CRITICAL:", "").strip(),
            "raw": line
        }
    
    # HIGH findings
    if "HIGH:" in line:
        return {
            "severity": "HIGH",
            "finding": line.replace("HIGH:", "").strip(),
            "raw": line
        }
    
    # MEDIUM findings
    if "MEDIUM:" in line:
        return {
            "severity": "MEDIUM",
            "finding": line.replace("MEDIUM:", "").strip(),
            "raw": line
        }
    
    # INFO findings
    if "INFO:" in line:
        return {
            "severity": "INFO",
            "finding": line.replace("INFO:", "").strip(),
            "raw": line
        }
    
    # CONFIRMED findings (Best Practice)
    if "CONFIRMED:" in line:
        return {
            "severity": "INFO",
            "finding": line.replace("CONFIRMED:", "").strip(),
            "raw": line
        }
    
    # File permission lines (ls -l output)
    if line.startswith("-rw") or line.startswith("drwx") or line.startswith("-rwx"):
        # Skip if it's just a header
        if "Checking for" in line:
            return None
        return {
            "severity": "MEDIUM",
            "finding": line,
            "raw": line
        }
    
    return None


# ============================================================================
# 3. REMEDIATION ENGINE
# ============================================================================

def get_fix_suggestion(finding, severity):
    """Generate fix command and explanation for each finding"""
    finding_lower = finding.lower()
    
    # Extract username or filepath from finding
    parts = finding.split()
    first_word = parts[0] if parts else ""
    
    # CRITICAL fixes
    if severity == "CRITICAL":
        if "uid 0" in finding_lower or "duplicate root" in finding_lower:
            return {
                "command": f"sudo userdel {first_word}",
                "note": "Unauthorized root account must be removed immediately"
            }
    
    # HIGH fixes
    if severity == "HIGH":
        if "service account with login shell" in finding_lower:
            return {
                "command": f"sudo usermod -s /usr/sbin/nologin {first_word}",
                "note": "Service accounts should not have interactive login shells"
            }
        
        if ".env" in finding_lower:
            # Extract filepath from ls -l output
            filepath = finding.split()[-1] if "/" in finding else "/home/ubuntu/audit_test/.env"
            return {
                "command": f"chmod 600 {filepath}",
                "note": "Environment files contain sensitive credentials like passwords and API keys"
            }
        
        if "id_rsa" in finding_lower or ".bak" in finding_lower:
            filepath = finding.split()[-1] if "/" in finding else "/home/ubuntu/audit_test/id_rsa.bak"
            return {
                "command": f"chmod 600 {filepath}",
                "note": "SSH private keys and backup files must be readable only by the owner"
            }
        
        if "shadow_backup" in finding_lower:
            filepath = finding.split()[-1] if "/" in finding else "/home/ubuntu/shadow_backup.old"
            return {
                "command": f"sudo rm {filepath}",
                "note": "Shadow file backups expose password hashes and should be deleted immediately"
            }
    
    # MEDIUM fixes
    if severity == "MEDIUM":
        if "expired" in finding_lower:
            return {
                "command": f"sudo userdel {first_word}",
                "note": f"Stale account expired: remove or re-enable with: sudo usermod -e \"\" {first_word}"
            }
        
        if "world-writable" in finding_lower or "rw-rw-rw-" in finding_lower or "rwxrwxrwx" in finding_lower:
            filepath = finding.split()[-1] if "/" in finding else "/path/to/file"
            return {
                "command": f"chmod 644 {filepath}",
                "note": "World-writable files can be modified by any system user"
            }
        
        if "debug.log" in finding_lower:
            filepath = finding.split()[-1] if "/" in finding else "/var/log/audit_test/debug.log"
            return {
                "command": f"chmod 640 {filepath}",
                "note": "Log files should not be world-writable to prevent tampering"
            }
    
    # INFO (no fix needed, just confirmation)
    if severity == "INFO":
        if "properly locked" in finding_lower:
            return {
                "command": "No action needed",
                "note": "This service account is correctly configured with nologin shell"
            }
        if "regular user" in finding_lower:
            return {
                "command": "No action needed",
                "note": "Standard user account with normal permissions"
            }
    
    # Default
    return {
        "command": "Manual review required",
        "note": "Investigate this finding manually"
    }


# ============================================================================
# 4. REPORT GENERATION
# ============================================================================

def generate_final_report(nodes_data, source_file, output_dir="reports"):
    """Generate a formatted report following the original structure"""
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_path / f"final_audit_report_{timestamp}.txt"
    
    # Count totals
    total_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "INFO": 0}
    
    with open(output_file, 'w') as f:
        # Header
        f.write("=" * 80 + "\n")
        f.write("                    SECURITY AUDIT REPORT WITH REMEDIATION\n")
        f.write("=" * 80 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Source: {source_file.name}\n")
        f.write("=" * 80 + "\n\n")
        
        # Process each node
        for node_name in sorted(nodes_data.keys()):
            node = nodes_data[node_name]
            
            f.write("=" * 80 + "\n")
            f.write(f"NODE: {node_name.upper()}\n")
            f.write("=" * 80 + "\n\n")
            
            # USERS SECTION
            f.write("[ USERS ]\n")
            f.write("-" * 40 + "\n\n")
            
            user_findings = []
            for finding in node["USERS"]:
                classified = classify_finding(finding, "USERS")
                if classified:
                    user_findings.append(classified)
            
            for finding in user_findings:
                total_counts[finding["severity"]] += 1
                fix = get_fix_suggestion(finding["finding"], finding["severity"])
                
                f.write(f"→ {finding['finding']}\n")
                f.write(f"  SEVERITY: {finding['severity']}\n")
                f.write(f"  FIX: {fix['command']}\n")
                f.write(f"  NOTE: {fix['note']}\n\n")
            
            if not user_findings:
                f.write("No user findings detected.\n\n")
            
            # FILES SECTION
            f.write("[ FILES & PERMISSIONS ]\n")
            f.write("-" * 40 + "\n\n")
            
            file_findings = []
            for finding in node["FILES"]:
                classified = classify_finding(finding, "FILES")
                if classified:
                    file_findings.append(classified)
            
            for finding in file_findings:
                total_counts[finding["severity"]] += 1
                fix = get_fix_suggestion(finding["finding"], finding["severity"])
                
                f.write(f"→ {finding['finding']}\n")
                f.write(f"  SEVERITY: {finding['severity']}\n")
                f.write(f"  FIX: {fix['command']}\n")
                f.write(f"  NOTE: {fix['note']}\n\n")
            
            if not file_findings:
                f.write("No file permission issues detected.\n\n")
            
            f.write("\n")
        
        # SUMMARY SECTION
        f.write("=" * 80 + "\n")
        f.write("SUMMARY\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total Nodes Scanned: {len(nodes_data)}\n\n")
        f.write(f"CRITICAL Issues: {total_counts['CRITICAL']}\n")
        f.write(f"HIGH Issues: {total_counts['HIGH']}\n")
        f.write(f"MEDIUM Issues: {total_counts['MEDIUM']}\n")
        f.write(f"INFO: {total_counts['INFO']}\n\n")
        
        f.write("=" * 80 + "\n")
        f.write("                    AUDIT COMPLETE\n")
        f.write("=" * 80 + "\n")
    
    return output_file


# ============================================================================
# 5. MAIN ORCHESTRATOR
# ============================================================================

def main():
    """Main function to orchestrate the audit analysis"""
    print("=" * 50)
    print("Security Audit Report Analyzer")
    print("=" * 50)
    print()
    
    # Step 1: Find the latest report
    report_file = find_latest_report()
    if not report_file:
        print("Exiting.")
        return
    
    # Step 2: Read the file
    lines = read_audit_file(report_file)
    if not lines:
        print("Exiting.")
        return
    
    # Step 3: Parse nodes and sections
    nodes_data = parse_nodes_and_sections(lines)
    
    # Step 4: Generate final report
    output_file = generate_final_report(nodes_data, report_file)
    
    print("\n" + "=" * 50)
    print(f"Final report saved to: {output_file}")
    print("=" * 50)


if __name__ == "__main__":
    main()