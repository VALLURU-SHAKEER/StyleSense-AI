
from pathlib import Path
import json
import urllib.request
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent

print("=== STEP 21: SETUP VERIFICATION ===")

checks = []

readme = ROOT / "README.md"
requirements = ROOT / "requirements.txt"

checks.append(("README exists", readme.is_file()))
checks.append(("requirements.txt exists", requirements.is_file()))

if readme.is_file():
    content = readme.read_text(encoding="utf-8")
    checks.append((
        "README installation command updated",
        "pip install -r requirements.txt" in content
    ))

if requirements.is_file():
    lines = [
        line.strip()
        for line in requirements.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    checks.append((
        "Seven pinned dependencies listed",
        len(lines) == 7 and all("==" in line for line in lines)
    ))

result = subprocess.run(
    [sys.executable, "-m", "pip", "check"],
    capture_output=True,
    text=True
)

checks.append(("Package dependency check", result.returncode == 0))
print("\nPIP CHECK:")
print((result.stdout + result.stderr).strip())

try:
    with urllib.request.urlopen(
        "http://127.0.0.1:5000/api/health", timeout=5
    ) as response:
        data = json.loads(response.read().decode("utf-8"))
        checks.append((
            "Flask health endpoint",
            response.status == 200 and data.get("status") == "ok"
        ))
        print("\nHealth response:", data)
except Exception as error:
    checks.append(("Flask health endpoint", False))
    print("\nHealth endpoint error:", error)

print("\n=== RESULTS ===")
for name, ok in checks:
    print(f'{"PASS" if ok else "FAIL"} | {name}')

print(f"\nSUMMARY: {sum(ok for _, ok in checks)}/{len(checks)} checks passed")
