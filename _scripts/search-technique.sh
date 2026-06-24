#!/usr/bin/env bash
# search-technique.sh — Search the vault for MITRE ATT&CK techniques or keywords.
#
# Usage:
#   ./search-technique.sh T1055              # find by MITRE ID
#   ./search-technique.sh "pass the hash"    # full-text keyword search
#   ./search-technique.sh -t lateral-movement # search by tag/category
#   ./search-technique.sh -l                 # list all technique IDs
#
set -euo pipefail

VAULT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RED='\033[0;31m'
GRN='\033[0;32m'
AMB='\033[0;33m'
CYN='\033[0;36m'
DIM='\033[2m'
RST='\033[0m'

banner() {
  echo -e "${RED}"
  echo "  ██████╗ ████████╗    ███████╗███████╗ █████╗ ██████╗  ██████╗██╗  ██╗"
  echo "  ██╔══██╗╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██║  ██║"
  echo "  ██████╔╝   ██║       ███████╗█████╗  ███████║██████╔╝██║     ███████║"
  echo "  ██╔══██╗   ██║       ╚════██║██╔══╝  ██╔══██║██╔══██╗██║     ██╔══██║"
  echo "  ██║  ██║   ██║       ███████║███████╗██║  ██║██║  ██║╚██████╗██║  ██║"
  echo "  ╚═╝  ╚═╝   ╚═╝       ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝"
  echo -e "${DIM}  Red Team Tactics & Techniques — Vault Search${RST}"
  echo ""
}

usage() {
  echo -e "${AMB}Usage:${RST}"
  echo "  $0 <MITRE-ID>              e.g. T1055, t1003"
  echo "  $0 \"<keyword>\"            e.g. \"process hollowing\""
  echo "  $0 -t <tag/category>       e.g. lateral-movement, kerberos"
  echo "  $0 -l                      list all MITRE technique IDs found in vault"
  echo "  $0 -h                      show this help"
  exit 0
}

list_techniques() {
  echo -e "${GRN}[ MITRE ATT&CK Technique Index ]${RST}"
  echo ""
  find "$VAULT_ROOT" -name 't[0-9]*.md' -not -path '*/.git/*' | sort | while read -r f; do
    id=$(basename "$f" .md | grep -oiE 't[0-9]+' | head -1 | tr '[:lower:]' '[:upper:]')
    title=$(grep -m1 '^#' "$f" 2>/dev/null | sed 's/^#\+\s*//' || echo "(no title)")
    category=$(echo "$f" | sed "s|$VAULT_ROOT/||" | cut -d'/' -f1)
    printf "  ${CYN}%-10s${RST} ${AMB}%-35s${RST} ${DIM}%s${RST}\n" "$id" "$title" "$category"
  done
}

search_by_id() {
  local id="${1,,}"   # lowercase
  echo -e "${GRN}[ Searching for technique: ${AMB}${id^^}${GRN} ]${RST}"
  echo ""
  find "$VAULT_ROOT" -name "${id}*.md" -not -path '*/.git/*' | sort | while read -r f; do
    rel="${f#$VAULT_ROOT/}"
    title=$(grep -m1 '^#' "$f" 2>/dev/null | sed 's/^#\+\s*//' || echo "(no title)")
    echo -e "  ${GRN}▶${RST} ${title}"
    echo -e "    ${DIM}${rel}${RST}"
    echo ""
  done
}

search_fulltext() {
  local query="$1"
  echo -e "${GRN}[ Full-text search: ${AMB}\"${query}\"${GRN} ]${RST}"
  echo ""
  grep -ril "$query" "$VAULT_ROOT" \
    --include="*.md" \
    --exclude-dir=".git" \
    --exclude-dir="_scripts" \
    --exclude-dir="_templates" | sort | while read -r f; do
    rel="${f#$VAULT_ROOT/}"
    title=$(grep -m1 '^#' "$f" 2>/dev/null | sed 's/^#\+\s*//' || echo "(no title)")
    # Show matched lines with context
    matches=$(grep -in "$query" "$f" | head -3 | sed 's/^/    /')
    echo -e "  ${GRN}▶${RST} ${title}"
    echo -e "    ${DIM}${rel}${RST}"
    echo -e "${CYN}${matches}${RST}"
    echo ""
  done
}

search_by_tag() {
  local tag="$1"
  echo -e "${GRN}[ Searching by category/tag: ${AMB}${tag}${GRN} ]${RST}"
  echo ""
  find "$VAULT_ROOT" -path "*${tag}*" -name "*.md" -not -path '*/.git/*' | sort | while read -r f; do
    rel="${f#$VAULT_ROOT/}"
    title=$(grep -m1 '^#' "$f" 2>/dev/null | sed 's/^#\+\s*//' || echo "(no title)")
    echo -e "  ${GRN}▶${RST} ${title}"
    echo -e "    ${DIM}${rel}${RST}"
    echo ""
  done
  # Also grep tags in frontmatter
  grep -ril "#${tag}" "$VAULT_ROOT" --include="*.md" --exclude-dir=".git" | sort | while read -r f; do
    rel="${f#$VAULT_ROOT/}"
    title=$(grep -m1 '^#' "$f" 2>/dev/null | sed 's/^#\+\s*//' || echo "(no title)")
    echo -e "  ${GRN}▶${RST} [tagged] ${title}"
    echo -e "    ${DIM}${rel}${RST}"
    echo ""
  done
}

# ── Main ──────────────────────────────────────────────────────────
banner

case "${1:-}" in
  -h|--help) usage ;;
  -l|--list) list_techniques ;;
  -t|--tag)
    [[ -z "${2:-}" ]] && { echo "Error: -t requires a tag argument"; exit 1; }
    search_by_tag "$2"
    ;;
  "")
    usage
    ;;
  *)
    query="$1"
    if [[ "$query" =~ ^[Tt][0-9]{4} ]]; then
      search_by_id "$query"
    else
      search_fulltext "$query"
    fi
    ;;
esac
