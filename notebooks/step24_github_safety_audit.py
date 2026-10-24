
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

SKIP_DIRS = {
    ".git", ".venv", ".venv_test", "venv", "env",
    "__pycache__", ".ipynb_checkpoints"
}

SUSPICIOUS_NAMES = {
    ".env", "credentials.json", "secrets.json",
    "id_rsa", "id_ed25519"
}

SECRET_PATTERNS = [
    re.compile(r"(?i)\b(api[_-]?key|secret[_-]?key|access[_-]?token|password)\b\s*[:=]\s*['\"]?([^\s'\"]{8,})"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
]

LARGE_FILE_BYTES = 25 * 1024 * 1024
suspicious_names = []
possible_secrets = []
large_files = []
unreadable = []

for path in ROOT.rglob("*"):
    if not path.is_file():
        continue

    relative = path.relative_to(ROOT)
    if any(part in SKIP_DIRS for part in relative.parts):
        continue

    if path.name.lower() in SUSPICIOUS_NAMES or path.name.lower().startswith(".env."):
        suspicious_names.append(str(relative))

    try:
        size = path.stat().st_size
        if size > LARGE_FILE_BYTES:
            large_files.append((str(relative), size))

        if path.suffix.lower() not in {
            ".py", ".txt", ".md", ".json", ".html", ".css",
            ".js", ".yml", ".yaml", ".toml", ".ini", ".cfg"
        }:
            continue

        content = path.read_text(encoding="utf-8", errors="ignore")
        for line_number, line in enumerate(content.splitlines(), 1):
            if any(pattern.search(line) for pattern in SECRET_PATTERNS):
                possible_secrets.append((str(relative), line_number))
    except OSError:
        unreadable.append(str(relative))

print("=== GitHub Safety Audit ===")
print("\nSuspicious filenames:")
if suspicious_names:
    for item in suspicious_names:
        print("REVIEW:", item)
else:
    print("None found")

print("\nPossible hard-coded secrets (values hidden):")
if possible_secrets:
    for filename, line_number in possible_secrets:
        print(f"REVIEW: {filename}, line {line_number}")
else:
    print("None detected by these patterns")

print("\nFiles larger than 25 MB:")
if large_files:
    for filename, size in large_files:
        print(f"REVIEW: {filename} ({size / (1024 * 1024):.1f} MB)")
else:
    print("None found")

print("\nUnreadable files:", len(unreadable))
for item in unreadable:
    print("REVIEW:", item)

print("\nAudit complete. Review any REVIEW entries before publishing.")
