
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

required_files = [
    "README.md",
    "requirements.txt",
    "backend/app.py",
    "backend/recommendation_service.py",
    "backend/recommendation_routes.py",
    "frontend/index.html",
    "frontend/style.css",
    "frontend/app.js",
    "data/raw/Womens Clothing E-Commerce Reviews.csv",
    "data/processed/clothing_products_modeling_ready.csv",
    "notebooks/step21_setup_verification.py",
    "notebooks/step22_dependency_test.py",
    "notebooks/step22_clean_environment_app_test.py",
]

print("=" * 55)
print("STYLESENSE AI - FINAL SUBMISSION READINESS AUDIT")
print("=" * 55)

passed = 0
failed = 0

for relative_path in required_files:
    path = ROOT / relative_path
    if path.is_file():
        print(f"PASS: {relative_path}")
        passed += 1
    else:
        print(f"FAIL: {relative_path} - file not found")
        failed += 1

print("\n--- Dataset checks ---")

dataset = ROOT / "data/processed/clothing_products_modeling_ready.csv"

if dataset.is_file():
    try:
        df = pd.read_csv(dataset)
        print(f"Dataset shape: {df.shape}")
        print(f"Unique Clothing IDs: {df['Clothing ID'].nunique()}"
              if "Clothing ID" in df.columns
              else "WARNING: Clothing ID column not found")

        if len(df) == 1206 and "Clothing ID" in df.columns:
            print("PASS: Modeling dataset has expected row count and ID column")
            passed += 1
        else:
            print("FAIL: Modeling dataset differs from expected structure")
            failed += 1
    except Exception as error:
        print(f"FAIL: Could not read modeling dataset: {error}")
        failed += 1
else:
    print("SKIP: Modeling dataset is missing")

print("\n--- Raw dataset count ---")
raw_folder = ROOT / "data/raw"
if raw_folder.is_dir():
    csv_files = list(raw_folder.glob("*.csv"))
    print(f"CSV files in data/raw: {len(csv_files)}")
    for path in csv_files:
        print(f"  - {path.name}")

    if len(csv_files) == 1:
        print("PASS: Exactly one raw CSV dataset is present")
        passed += 1
    else:
        print("REVIEW: Expected one raw CSV dataset")
else:
    print("FAIL: data/raw folder not found")
    failed += 1

print("\n--- Final result ---")
print(f"Checks passed: {passed}")
print(f"Checks failed: {failed}")

if failed == 0:
    print("AUDIT PASSED: All required-file and dataset checks passed.")
else:
    print("AUDIT NEEDS REVIEW: Fix the FAIL items before submission.")
