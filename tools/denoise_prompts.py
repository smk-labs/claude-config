#!/usr/bin/env python3
"""Filter user_prompts.txt to keep only typed messages, remove pastes."""
import re
from pathlib import Path

src = Path.home() / ".claude/tools/user_prompts.txt"
out = Path.home() / ".claude/tools/user_prompts_clean.txt"

MAX_CHARS = 1200       # longer than this → likely paste
MAX_LINES = 15         # many lines → likely paste
CODE_DENSITY = 0.12    # >12% special chars → likely code paste

SPECIAL = set('{}[]()<>|=;\\/#@$%^&*')

def is_paste(text: str) -> bool:
    if len(text) > MAX_CHARS:
        return True
    lines = text.splitlines()
    if len(lines) > MAX_LINES:
        return True
    if "```" in text:
        return True
    # indented block (code/JSON/YAML)
    indented = sum(1 for l in lines if l.startswith(("    ", "\t")))
    if indented > 3:
        return True
    # special char density
    density = sum(1 for c in text if c in SPECIAL) / max(len(text), 1)
    if density > CODE_DENSITY:
        return True
    return False

kept, removed = 0, 0
with open(src) as f:
    raw = f.read()

blocks = re.split(r'(?=^=== \[)', raw, flags=re.MULTILINE)

with open(out, "w") as f:
    for block in blocks:
        if not block.strip():
            continue
        header, _, body = block.partition("\n")
        body = body.strip()
        if is_paste(body):
            removed += 1
            continue
        f.write(f"{header}\n{body}\n\n")
        kept += 1

print(f"Kept {kept}, removed {removed} (pastes/code)")
print(f"Clean file: {out.stat().st_size / 1024:.1f} KB")
