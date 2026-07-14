#!/usr/bin/env python3
"""Extract clean user-typed text from Claude Code conversation history."""
import json, re
from pathlib import Path

projects = Path.home() / ".claude/projects"
out = Path.home() / ".claude/tools/user_prompts_clean.txt"

SPECIAL = set('{}[]<>;\\|=')

SKIP_PREFIXES = (
    "Base directory for this skill:",
    "<ide_opened_file>",
    "<task-notification>",
    "<command-name>",
    "<local-command",
    "Please analyze this codebase",
    "#!/",
    "---\nname:",
    "Stop hook feedback:",
    "[Before finishing",
    "This session is being continued from a previous conversation",
    "The user just ran /",
    "Here is the full insights",
)

# Skip entire block if it contains these patterns (pasted transcripts, eval logs)
SKIP_BLOCK_PATTERNS = re.compile(
    r'"text":\s*"'                  # pasted JSON transcript
    r'|\[\d+/\d+\]'                 # eval log [1/18]
    r'|→ 💬'                        # eval result line
    r'|transcriptHtml'              # raw transcript field
    r'|\[Action [a-f0-9\-]+ approved' # action approval log
)

# Always-noise line patterns regardless of message length
NOISE_LINE = re.compile(
    r'^[📦🧪🤖📁━▶✅❌🔗⬆⬇]'
    r'|^https?://'
    r'|curl\s+-[A-Z]'               # curl commands anywhere in line
    r'|^wget\b|^mkdir\b|^sudo\b'
    r'|^ERROR\[|^WARN\[|^INFO\[|^cp:\s|^mv:\s|^rm:\s|^ls:\s'
    r'|^>{4,}'                      # >>>> profile lines
    r'|^-[A-Z]\s'                   # CLI flags: -H, -d, -X, -L
    r'|\d{3,}ms\b'
)

def is_prose(line):
    s = line.strip()
    if not s:
        return False
    # Reject log lines outright
    if re.match(r'^(ERROR|WARN|INFO|DEBUG)\[', s):
        return False
    words = re.findall(r'[a-zA-Z\u0600-\u06FF]{3,}', s)
    if len(words) < 5:
        return False
    # Letters only (no spaces) must dominate
    letter_ratio = sum(1 for c in s if c.isalpha()) / len(s)
    return letter_ratio >= 0.60

MAX_LINES = 3  # max content lines per message

def always_noise(line):
    s = line.strip()
    if not s:
        return True
    if NOISE_LINE.search(s):
        return True
    if s.startswith('"') or s.startswith("'"):          # JSON strings
        return True
    if s.startswith('[') or s.startswith('{'):          # JSON arrays/objects
        return True
    if re.match(r'^\w+@[\w\-]+', s):                   # shell prompt
        return True
    if re.match(r'^->\s', s):                           # shell output
        return True
    if re.match(r'^<[a-z\-]+[\s>/]', s):               # XML tags
        return True
    if re.search(r'https?://', s):                      # any URL in line
        return True
    if any(len(tok) > 25 for tok in s.split()):         # token >25 chars = hash/key/path
        return True
    if ' ' not in s and len(s) > 30:                    # long no-space fragment
        return True
    if len(re.findall(r'[a-zA-Z]{2,}', s)) < 2:
        return True
    return False

def clean(text):
    text = re.sub(r'```[\s\S]*?```', '', text)
    # Apply always-noise filter to every line unconditionally
    lines = [l for l in text.splitlines() if not always_noise(l)]
    non_empty = [l for l in lines if l.strip()]
    if not non_empty:
        return ''
    # Short messages pass through (already noise-filtered above)
    if len(non_empty) <= 2:
        return '\n'.join(non_empty).strip()
    # Multi-line: prose filter + cap
    kept = [l for l in lines if is_prose(l)][:MAX_LINES]
    return '\n'.join(kept).strip()

def extract(content):
    """From array content, take only user-typed text blocks."""
    if isinstance(content, str):
        return content.strip()
    parts = []
    for b in content:
        if not isinstance(b, dict) or b.get("type") != "text":
            continue
        t = b.get("text", "").strip()
        if not t.startswith("<ide_"):
            parts.append(t)
    return "\n".join(parts).strip()

seen, kept, skipped = set(), 0, 0
with open(out, "w") as f:
    for jsonl in sorted(projects.glob("**/*.jsonl")):
        if "subagents" in str(jsonl):
            continue
        for line in open(jsonl, errors="ignore"):
            try:
                msg = json.loads(line)
                if msg.get("type") != "user":
                    continue
                raw = extract(msg.get("message", {}).get("content", ""))
                if not raw or raw in seen:
                    continue
                seen.add(raw)

                if any(raw.startswith(p) for p in SKIP_PREFIXES):
                    skipped += 1; continue
                if SKIP_BLOCK_PATTERNS.search(raw):
                    skipped += 1; continue

                cleaned = clean(raw)
                if not cleaned or len(cleaned) < 15:
                    skipped += 1; continue

                if len(cleaned) < 20:   # skip trivial one-word messages
                    skipped += 1; continue
                f.write(f"{cleaned}\n\n")
                kept += 1
            except Exception:
                continue

print(f"Kept {kept}, skipped {skipped}")
print(f"Output: {out} ({out.stat().st_size/1024:.1f} KB)")
