#!/usr/bin/env python3
"""
convert-gitbook.py — Convert GitBook syntax to Obsidian-compatible markdown.

Transforms:
  - {% hint style="X" %}...{% endhint %}  → > [!X] callouts
  - {% embed url="..." %}                 → markdown link
  - {% code title="..." %}...{% endcode %} → fenced code with title comment
  - YAML frontmatter `description:` field → Obsidian `description:` property
  - Image paths  ../../.gitbook/assets/   → attachments relative to vault
  - Wiki-link generation for same-folder .md references
"""

import os
import re
import sys
import argparse
from pathlib import Path

VAULT_ROOT = Path(__file__).parent.parent

HINT_STYLE_MAP = {
    "warning": "WARNING",
    "danger":  "DANGER",
    "info":    "INFO",
    "success": "SUCCESS",
}


def convert_hints(text: str) -> str:
    """Convert {% hint style="X" %}...{% endhint %} to Obsidian callout blocks."""
    def replacer(m):
        style   = m.group(1).lower()
        content = m.group(2).strip()
        callout = HINT_STYLE_MAP.get(style, style.upper())
        lines   = content.splitlines()
        body    = "\n".join(f"> {line}" for line in lines)
        return f"> [!{callout}]\n{body}"

    pattern = r'\{%\s*hint\s+style=["\'](\w+)["\']\s*%\}(.*?)\{%\s*endhint\s*%\}'
    return re.sub(pattern, replacer, text, flags=re.DOTALL)


def convert_embeds(text: str) -> str:
    """Convert {% embed url="..." %} to a markdown external link."""
    def replacer(m):
        url = m.group(1).strip()
        # derive a readable label from the URL hostname + path
        label = re.sub(r'^https?://', '', url).rstrip('/')
        return f"[{label}]({url})"

    pattern = r'\{%\s*embed\s+url=["\']([^"\']+)["\']\s*%\}'
    return re.sub(pattern, replacer, text)


def convert_code_blocks(text: str) -> str:
    """Convert {% code title="X" %}...{% endcode %} to standard fenced code blocks.

    The title is preserved as a comment on the first line of the block so
    Obsidian renders it cleanly without breaking the fence.
    """
    def replacer(m):
        title   = m.group(1).strip()
        content = m.group(2)
        # find and strip the inner fences (``` ... ```)
        inner   = re.sub(r'^```[a-zA-Z]*\n', '', content.lstrip('\n'), count=1)
        inner   = re.sub(r'\n```\s*$', '', inner)
        lang_m  = re.search(r'^```([a-zA-Z]*)', content.lstrip('\n'))
        lang    = lang_m.group(1) if lang_m else ''
        title_comment = f"// {title}\n" if title else ""
        return f"```{lang}\n{title_comment}{inner}\n```"

    pattern = r'\{%\s*code\s+title=["\']([^"\']*?)["\']\s*%\}(.*?)\{%\s*endcode\s*%\}'
    return re.sub(pattern, replacer, text, flags=re.DOTALL)


def convert_image_paths(text: str, md_file: Path) -> str:
    """Rewrite .gitbook/assets paths to ![[filename]] Obsidian embeds."""
    # Standard markdown images: ![alt](path)
    def md_img_replacer(m):
        alt      = m.group(1)
        img_path = m.group(2)
        filename = Path(img_path.strip('<>')).name
        if alt:
            return f"![[{filename}|{alt}]]"
        return f"![[{filename}]]"

    pattern_md = r'!\[([^\]]*)\]\(<?((?:\.\./)*\.gitbook/assets/[^>)\s]+)>?\)'
    text = re.sub(pattern_md, md_img_replacer, text)

    # HTML <img src="path" ...> tags
    def html_img_replacer(m):
        img_path = m.group(1)
        filename = Path(img_path).name
        return f"![[{filename}]]"

    pattern_html = r'<img\s+src=["\']([^"\']*\.gitbook/assets/[^"\']+)["\'][^>]*/?>(?:\\)?'
    text = re.sub(pattern_html, html_img_replacer, text)

    # cover: in frontmatter
    def cover_replacer(m):
        img_path = m.group(1)
        filename = Path(img_path).name
        return f"cover: [[{filename}]]"

    pattern_cover = r'cover:\s+((?:\.\./)*\.gitbook/assets/[^\s\n]+)'
    text = re.sub(pattern_cover, cover_replacer, text)

    return text


def convert_frontmatter(text: str) -> str:
    """Ensure YAML frontmatter has standard Obsidian fields.

    Adds `tags:` from the description field when it maps to a known category.
    """
    if not text.startswith('---'):
        return text

    fm_end = text.find('\n---', 3)
    if fm_end == -1:
        return text

    fm_block  = text[3:fm_end]
    rest      = text[fm_end + 4:]

    desc_match = re.search(r'^description:\s*(.+)$', fm_block, re.MULTILINE | re.IGNORECASE)
    if not desc_match:
        return text

    description = desc_match.group(1).strip()

    category_tag_map = {
        "credential access":    "#credential-access",
        "defense evasion":      "#defense-evasion",
        "lateral movement":     "#lateral-movement",
        "privilege escalation": "#privilege-escalation",
        "persistence":          "#persistence",
        "code execution":       "#code-execution",
        "initial access":       "#initial-access",
        "active directory":     "#active-directory",
        "process injection":    "#process-injection",
        "kerberos":             "#active-directory",
        "enumeration":          "#enumeration",
        "exfiltration":         "#exfiltration",
        "reversing":            "#reversing",
        "kernel":               "#kernel",
    }

    tags = []
    for keyword, tag in category_tag_map.items():
        if keyword in description.lower():
            tags.append(tag)

    if tags:
        if 'tags:' not in fm_block:
            fm_block += f"\ntags: [{', '.join(tags)}]"

    return f"---{fm_block}\n---{rest}"


def remove_gitbook_residue(text: str) -> str:
    """Remove any remaining GitBook template tags that weren't caught above."""
    # Remove any remaining {%...%} tags
    text = re.sub(r'\{%[^%]*%\}', '', text)
    return text


def process_file(md_file: Path, dry_run: bool = False) -> bool:
    """Process a single markdown file. Returns True if changes were made."""
    try:
        original = md_file.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        print(f"  [SKIP] {md_file.relative_to(VAULT_ROOT)}: {e}", file=sys.stderr)
        return False

    text = original
    text = convert_hints(text)
    text = convert_embeds(text)
    text = convert_code_blocks(text)
    text = convert_image_paths(text, md_file)
    text = convert_frontmatter(text)
    text = remove_gitbook_residue(text)

    if text == original:
        return False

    if not dry_run:
        md_file.write_text(text, encoding='utf-8')
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--dry-run', action='store_true', help='Show what would change without writing')
    parser.add_argument('--path', default=str(VAULT_ROOT), help='Path to scan (default: vault root)')
    args = parser.parse_args()

    root   = Path(args.path)
    files  = list(root.rglob('*.md'))
    # Skip hidden dirs and scripts/templates dirs
    files  = [f for f in files if not any(p.startswith('.') or p == '_scripts' for p in f.parts)]

    changed = 0
    for f in sorted(files):
        rel = f.relative_to(VAULT_ROOT)
        did_change = process_file(f, dry_run=args.dry_run)
        if did_change:
            changed += 1
            status = "[DRY]" if args.dry_run else "[OK] "
            print(f"  {status} {rel}")

    mode = " (dry run)" if args.dry_run else ""
    print(f"\nDone{mode}: {changed}/{len(files)} files updated.")


if __name__ == '__main__':
    main()
