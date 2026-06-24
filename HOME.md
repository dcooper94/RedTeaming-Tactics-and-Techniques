---
title: Red Team Vault
tags: [#home, #moc]
---

# Red Team Tactics & Techniques

> A living knowledge base of offensive security research, attack patterns, and operational notes.
> Organised by MITRE ATT&CK. Built for speed, not ceremony.

---

## Tactics Index

### Initial Foothold

| Tactic | Notes |
|--------|-------|
| [[offensive-security/initial-access/README\|Initial Access]] | Phishing, OWA spraying, forced auth |
| [[offensive-security/code-execution/README\|Code Execution]] | LOLBins, AppLocker bypass, macro exec |

### Escalate

| Tactic | Notes |
|--------|-------|
| [[offensive-security/privilege-escalation/README\|Privilege Escalation]] | Token abuse, DLL hijacking, named pipes |
| [[offensive-security/credential-access-and-credential-dumping/README\|Credential Access]] | LSASS, DPAPI, SAM, DCSync |

### Move & Persist

| Tactic | Notes |
|--------|-------|
| [[offensive-security/lateral-movement/README\|Lateral Movement]] | WMI, SMB, DCOM, RDP, tunneling |
| [[offensive-security/persistence/README\|Persistence]] | Registry, WMI subscriptions, scheduled tasks |

### Evade & Exfil

| Tactic | Notes |
|--------|-------|
| [[offensive-security/defense-evasion/README\|Defense Evasion]] | Process injection, AV bypass, EDR evasion |
| [[offensive-security/exfiltration/README\|Exfiltration]] | DNS tunneling, exfil over HTTPS |
| [[offensive-security/enumeration-and-discovery/README\|Enumeration & Discovery]] | COM, user/network enum, Sysmon detection |

### Infrastructure

| Tactic | Notes |
|--------|-------|
| [[offensive-security/red-team-infrastructure/README\|Red Team Infrastructure]] | Redirectors, C2 setup, Cobalt Strike |

---

## Deep Dive — Experiments

| Area | Notes |
|------|-------|
| [[offensive-security-experiments/active-directory-kerberos-abuse/README\|Active Directory & Kerberos]] | Golden/Silver tickets, Kerberoasting, AS-REP, DCSync |
| [[offensive-security-experiments/offensive-security-cheetsheets/README\|Cheatsheets]] | Quick reference |

---

## Kernel & Internals

| Area | Notes |
|------|-------|
| [[miscellaneous-reversing-forensics/windows-kernel-internals/README\|Windows Kernel Internals]] | Drivers, SSDT, token abuse, ETW bypass |
| [[miscellaneous-reversing-forensics/windows-kernel/README\|Kernel Exploitation (Legacy)]] | Older exploit techniques |
| [[miscellaneous-reversing-forensics/README\|Forensics & Reversing]] | Memory, PE parsing, encryption, Neo4j |

---

## Technique Spotlights

- [[offensive-security-experiments/active-directory-kerberos-abuse/kerberos-golden-tickets|Golden Tickets]]
- [[offensive-security-experiments/active-directory-kerberos-abuse/t1208-kerberoasting|Kerberoasting]]
- [[offensive-security-experiments/active-directory-kerberos-abuse/pass-the-hash-with-machine-accounts|Pass the Hash — Machine Accounts]]
- [[offensive-security/credential-access-and-credential-dumping/t1003-credential-dumping-lsass|LSASS Credential Dumping]]
- [[offensive-security/defense-evasion/parent-process-id-ppid-spoofing|PPID Spoofing]]
- [[offensive-security/code-injection-process-injection/process-doppelganging|Process Doppelgänging]]
- [[miscellaneous-reversing-forensics/windows-kernel-internals/how-kernel-exploits-abuse-tokens-for-privilege-escalation|Kernel Token Abuse]]

---

## Lab Infrastructure

- [[lab/sysmonconfig-export|Sysmon Config]]
- [[lab/winlogbeat|Winlogbeat / ELK]]

---

## Vault Tools

| Script | Purpose |
|--------|---------|
| `_scripts/convert-gitbook.py` | Convert remaining GitBook syntax to Obsidian |
| `_scripts/search-technique.sh` | CLI search by MITRE ID or keyword |
| `_scripts/vault-stats.py` | Coverage stats and health check |
| `_scripts/new-technique.sh` | Scaffold a new technique note |

```bash
# Quick search from terminal
bash _scripts/search-technique.sh T1055
bash _scripts/search-technique.sh "pass the hash"
python3 _scripts/vault-stats.py
```

---

## Templates

| Template | Use for |
|----------|---------|
| [[_templates/New Technique\|New Technique]] | Documenting a new ATT&CK technique |
| [[_templates/Engagement Notes\|Engagement Notes]] | Active engagement tracking |
| [[_templates/Target Profile\|Target Profile]] | Per-host documentation |
| [[_templates/Daily Ops\|Daily Ops]] | Day-by-day ops logging |

---

> [!WARNING]
> All techniques documented here are for **authorised security testing and research only**.
> Ensure you have written permission before conducting any offensive activity.
