#!/usr/bin/env python3
"""
fix-malformed-embeds.py — Fix ![[image (N]].ext>)  patterns left by the
parenthesis-in-filename edge case in convert-gitbook.py.

Malformed:  ![[image (334]].png>)
            ![[image (344|Token stealing / swapping process]].png>)
Fixed:      ![[image (334).png]]
            ![[image (344).png|Token stealing / swapping process]]
"""
import re
import sys
from pathlib import Path

VAULT_ROOT = Path(__file__).parent.parent


def fix_embeds(text: str) -> str:
    # Pattern: ![[stem|optional_alt]].ext>)
    # We need to reconstruct: ![[stem).ext]] or ![[stem).ext|alt]]
    def replacer(m):
        stem    = m.group(1)  # e.g. "image (334"  or  "image (344|Some caption"
        ext     = m.group(2)  # e.g. ".png" or ".gif"

        # Split stem into name part and alt-text part on the LAST pipe
        if '|' in stem:
            # e.g. "image (344|Token stealing" → name="image (344", alt="Token stealing"
            pipe_idx = stem.index('|')
            name_part = stem[:pipe_idx]
            alt_part  = stem[pipe_idx+1:]
            full_name = f"{name_part}){ext}"
            return f"![[{full_name}|{alt_part}]]"
        else:
            full_name = f"{stem}){ext}"
            return f"![[{full_name}]]"

    # Matches: ![[...  (no closing ]])  then ]].ext>)
    pattern = r'!\[\[([^\]]*?)\]\](\.\w+)>?\)'
    return re.sub(pattern, replacer, text)


def process_file(md_file: Path) -> bool:
    try:
        original = md_file.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        print(f"  [SKIP] {md_file.name}: {e}", file=sys.stderr)
        return False

    fixed = fix_embeds(original)
    if fixed == original:
        return False

    md_file.write_text(fixed, encoding='utf-8')
    return True


def main():
    files = [
        f for f in VAULT_ROOT.rglob('*.md')
        if not any(p.startswith('.') or p in ('_scripts', '_templates')
                   for p in f.relative_to(VAULT_ROOT).parts)
    ]
    changed = 0
    for f in sorted(files):
        if process_file(f):
            changed += 1
            print(f"  [OK]  {f.relative_to(VAULT_ROOT)}")

    print(f"\nFixed {changed} files.")


if __name__ == '__main__':
    main()
