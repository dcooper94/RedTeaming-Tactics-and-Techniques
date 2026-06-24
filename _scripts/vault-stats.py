#!/usr/bin/env python3
"""
vault-stats.py — Print statistics about the red team vault.

Shows technique counts by category, MITRE coverage, orphan notes, etc.
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

VAULT_ROOT = Path(__file__).parent.parent

GREEN  = "\033[32m"
RED    = "\033[31m"
AMBER  = "\033[33m"
CYAN   = "\033[36m"
DIM    = "\033[2m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def col(text, color):
    return f"{color}{text}{RESET}"


def scan_vault():
    md_files = [
        f for f in VAULT_ROOT.rglob("*.md")
        if not any(p.startswith(".") or p in ("_scripts", "_templates")
                   for p in f.relative_to(VAULT_ROOT).parts)
    ]
    return md_files


def category_breakdown(files):
    cats = defaultdict(int)
    for f in files:
        parts = f.relative_to(VAULT_ROOT).parts
        if len(parts) >= 2:
            cats[parts[0]] += 1
        else:
            cats["(root)"] += 1
    return dict(sorted(cats.items(), key=lambda x: -x[1]))


def mitre_techniques(files):
    techniques = []
    for f in files:
        name = f.stem
        m = re.match(r'^(t\d{4})', name, re.IGNORECASE)
        if m:
            techniques.append((m.group(1).upper(), f))
    return sorted(techniques, key=lambda x: x[0])


def count_gitbook_residue(files):
    residue = 0
    for f in files:
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
            if re.search(r'\{%', content):
                residue += 1
        except Exception:
            pass
    return residue


def count_broken_images(files):
    broken = []
    for f in files:
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
            imgs = re.findall(r'!\[.*?\]\(([^)]+)\)', content)
            for img in imgs:
                if ".gitbook/assets" in img:
                    broken.append((f, img))
        except Exception:
            pass
    return broken


def print_banner():
    print(col("""
  ╔═══════════════════════════════════════════════════════╗
  ║     RED TEAM VAULT — STATISTICS                       ║
  ╚═══════════════════════════════════════════════════════╝""", RED))
    print()


def main():
    print_banner()
    files = scan_vault()

    # ── Overview ──────────────────────────────────────────────
    print(col("  [ OVERVIEW ]", AMBER))
    print(f"  {'Total notes:':<30} {col(len(files), GREEN)}")
    techniques = mitre_techniques(files)
    print(f"  {'MITRE-tagged techniques:':<30} {col(len(techniques), GREEN)}")
    residue_count = count_gitbook_residue(files)
    residue_color = RED if residue_count > 0 else GREEN
    print(f"  {'GitBook syntax remaining:':<30} {col(residue_count, residue_color)}")
    broken = count_broken_images(files)
    broken_color = RED if broken else GREEN
    print(f"  {'Unconverted image links:':<30} {col(len(broken), broken_color)}")
    print()

    # ── Category Breakdown ────────────────────────────────────
    print(col("  [ NOTES BY CATEGORY ]", AMBER))
    cats = category_breakdown(files)
    for cat, count in cats.items():
        bar = col("█" * min(count, 40), GREEN) + col("░" * max(0, 40 - count), DIM)
        print(f"  {cat:<50} {bar} {col(count, CYAN)}")
    print()

    # ── MITRE Technique List ──────────────────────────────────
    print(col("  [ MITRE ATT&CK TECHNIQUES ]", AMBER))
    if techniques:
        for tid, path in techniques:
            title = ""
            try:
                content = path.read_text(encoding="utf-8", errors="replace")
                m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                if m:
                    title = m.group(1).strip()
            except Exception:
                pass
            rel = path.relative_to(VAULT_ROOT)
            print(f"  {col(tid, CYAN):<20} {title[:45]:<46} {col(str(rel.parent), DIM)}")
    print()

    # ── Residue Warning ───────────────────────────────────────
    if residue_count > 0:
        print(col(f"  [!] {residue_count} files still contain GitBook template tags.", RED))
        print(col("      Run: python3 _scripts/convert-gitbook.py", AMBER))
        print()

    if broken:
        print(col(f"  [!] {len(broken)} unconverted image references found.", RED))
        print(col("      Run: python3 _scripts/convert-gitbook.py", AMBER))
        print()

    print(col("  ─────────────────────────────────────────────────────────", DIM))
    print(col("  Vault root: " + str(VAULT_ROOT), DIM))
    print()


if __name__ == "__main__":
    main()
