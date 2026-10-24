
from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parent.parent
SEARCH_DIRS = ["backend", "notebooks"]
SKIP_DIRS = {"__pycache__", ".venv", "venv"}

standard_library = set()

try:
    import sys
    standard_library = set(sys.stdlib_module_names)
except AttributeError:
    pass

imports = {}
files_scanned = 0

for folder in SEARCH_DIRS:
    base = ROOT / folder
    if not base.exists():
        continue

    for path in base.rglob("*.py"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue

        try:
            tree = ast.parse(
                path.read_text(encoding="utf-8-sig"),
                filename=str(path),
            )
        except (SyntaxError, UnicodeDecodeError) as error:
            print(f"PARSE WARNING | {path.relative_to(ROOT)} | {error}")
            continue

        files_scanned += 1

        for node in ast.walk(tree):
            module = None

            if isinstance(node, ast.Import):
                for alias in node.names:
                    module = alias.name.split(".")[0]
                    imports.setdefault(module, set()).add(
                        str(path.relative_to(ROOT))
                    )

            elif isinstance(node, ast.ImportFrom) and node.module:
                module = node.module.split(".")[0]
                imports.setdefault(module, set()).add(
                    str(path.relative_to(ROOT))
                )

print("=== STEP 20.1: PYTHON DEPENDENCY AUDIT ===")
print("Project:", ROOT)
print("Python files scanned:", files_scanned)
print("\nImported top-level modules:")

for module in sorted(imports):
    if module not in standard_library:
        print(f"EXTERNAL OR LOCAL | {module}")

print("\n=== IMPORT LOCATIONS ===")
for module in sorted(imports):
    if module not in standard_library:
        locations = ", ".join(sorted(imports[module]))
        print(f"{module}: {locations}")

print("\nAudit complete. No project files were modified.")
