#!/usr/bin/env bash
# new-technique.sh — Scaffold a new technique note from the template.
#
# Usage:
#   ./new-technique.sh "Process Hollowing" T1055 "Defense Evasion"
#   ./new-technique.sh                    (interactive mode)
#
set -euo pipefail

VAULT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE="$VAULT_ROOT/_templates/New Technique.md"
RED='\033[0;31m'
GRN='\033[0;32m'
AMB='\033[0;33m'
CYN='\033[0;36m'
RST='\033[0m'

echo -e "${RED}[ Red Team Vault — New Technique ]${RST}"
echo ""

# ── Arguments or interactive prompts ──────────────────────────
if [[ $# -ge 1 ]]; then
  TITLE="$1"
else
  read -rp "$(echo -e ${AMB})Technique name: $(echo -e ${RST})" TITLE
fi

if [[ $# -ge 2 ]]; then
  MITRE_ID="${2^^}"
else
  read -rp "$(echo -e ${AMB})MITRE ATT&CK ID (e.g. T1055, or leave blank): $(echo -e ${RST})" MITRE_ID
  MITRE_ID="${MITRE_ID^^}"
fi

if [[ $# -ge 3 ]]; then
  CATEGORY="$3"
else
  echo -e "${CYN}Categories:${RST}"
  echo "  1) credential-access-and-credential-dumping"
  echo "  2) defense-evasion"
  echo "  3) lateral-movement"
  echo "  4) privilege-escalation"
  echo "  5) persistence"
  echo "  6) code-execution"
  echo "  7) initial-access"
  echo "  8) enumeration-and-discovery"
  echo "  9) code-injection-process-injection"
  echo " 10) red-team-infrastructure"
  echo " 11) miscellaneous-reversing-forensics"
  read -rp "$(echo -e ${AMB})Pick category (number or type full name): $(echo -e ${RST})" cat_input
  case "$cat_input" in
    1) CATEGORY="offensive-security/credential-access-and-credential-dumping" ;;
    2) CATEGORY="offensive-security/defense-evasion" ;;
    3) CATEGORY="offensive-security/lateral-movement" ;;
    4) CATEGORY="offensive-security/privilege-escalation" ;;
    5) CATEGORY="offensive-security/persistence" ;;
    6) CATEGORY="offensive-security/code-execution" ;;
    7) CATEGORY="offensive-security/initial-access" ;;
    8) CATEGORY="offensive-security/enumeration-and-discovery" ;;
    9) CATEGORY="offensive-security/code-injection-process-injection" ;;
   10) CATEGORY="offensive-security/red-team-infrastructure" ;;
   11) CATEGORY="miscellaneous-reversing-forensics" ;;
    *) CATEGORY="$cat_input" ;;
  esac
fi

# ── Derive filename ────────────────────────────────────────────
slug=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')
if [[ -n "$MITRE_ID" ]]; then
  filename="${MITRE_ID,,}-${slug}.md"
else
  filename="${slug}.md"
fi

TARGET_DIR="$VAULT_ROOT/$CATEGORY"
TARGET_FILE="$TARGET_DIR/$filename"

mkdir -p "$TARGET_DIR"

if [[ -f "$TARGET_FILE" ]]; then
  echo -e "${RED}[!] File already exists: $TARGET_FILE${RST}"
  exit 1
fi

# ── Populate template ──────────────────────────────────────────
TODAY=$(date +%Y-%m-%d)
MITRE_URL=""
if [[ -n "$MITRE_ID" ]]; then
  num="${MITRE_ID#T}"
  MITRE_URL="https://attack.mitre.org/techniques/${MITRE_ID}/"
fi

cat > "$TARGET_FILE" << MDEOF
---
title: ${TITLE}
mitre-id: ${MITRE_ID}
date: ${TODAY}
tags: []
status: draft
---

# ${TITLE}

## Overview

> Brief description of what this technique does and why it matters.

## MITRE ATT&CK

| Field       | Value |
|-------------|-------|
| Technique   | [${MITRE_ID} — ${TITLE}](${MITRE_URL}) |
| Tactic      | |
| Platform    | Windows / Linux / macOS |
| Permissions | |
| Data Source | |

## Prerequisites

- [ ] Access level required
- [ ] Tools / implants needed
- [ ] Network conditions

## Execution

### Step 1 — Enumerate / Prepare

\`\`\`powershell
# command here
\`\`\`

### Step 2 — Execute

\`\`\`powershell
# command here
\`\`\`

### Step 3 — Verify / Exfil

\`\`\`powershell
# command here
\`\`\`

## Detection

> [!DETECTION]
> Describe how defenders detect this technique.

| Data Source | Event ID | Indicator |
|-------------|----------|-----------|
| | | |

## OPSEC Considerations

> [!OPSEC]
> What artefacts does this leave? How to minimise footprint?

## Tools

| Tool | Notes |
|------|-------|
| | |

## References

-
MDEOF

echo -e "${GRN}[+] Created: ${TARGET_FILE#$VAULT_ROOT/}${RST}"
echo ""
echo -e "${CYN}Open in Obsidian or run:${RST}"
echo "  code \"$TARGET_FILE\""
