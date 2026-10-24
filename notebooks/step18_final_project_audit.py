
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

required_files = [
    "backend/app.py",
    "backend/recommendation_service.py",
    "backend/recommendation_routes.py",
    "frontend/index.html",
    "frontend/style.css",
    "frontend/app.js",
    "data/processed/clothing_reviews_cleaned.csv",
    "data/processed/clothing_reviews_feature_engineered.csv",
    "data/processed/clothing_reviews_ml_ready.csv",
    "data/processed/clothing_products_modeling_ready.csv",
    "data/processed/product_similarity_matrix.npy",
    "data/processed/product_similarity_index.csv",
    "data/processed/recommendation_evaluation.csv",
    "data/processed/final_user_recommendations.csv",
    "data/processed/final_recommendation_robustness.csv",
    "notebooks/step17_4_api_tests.py",
    "notebooks/step17_5_ranking_tests.py",
    "notebooks/step17_6_frontend_tests.py",
]

print("=== STYLESENSE AI: FINAL PROJECT AUDIT ===")
print("Project folder:", ROOT)
print()

passed = 0
missing = []

for relative_path in required_files:
    exists = (ROOT / relative_path).is_file()

    if exists:
        passed += 1
        print(f"PASS | {relative_path}")
    else:
        missing.append(relative_path)
        print(f"MISSING | {relative_path}")

print()
print("=== DATASET AND MODEL ARTIFACT CHECK ===")

model_path = ROOT / "data/processed/clothing_products_modeling_ready.csv"

if model_path.is_file():
    try:
        products = pd.read_csv(model_path)
        print("Product dataset shape:", products.shape)
        print("Required columns present:",
              all(c in products.columns for c in [
                  "Clothing ID",
                  "Department_Name",
                  "Class_Name",
                  "Average_Rating",
                  "Recommendation_Rate",
              ]))
        print("Unique Clothing IDs:", products["Clothing ID"].nunique())
    except Exception as error:
        print("DATA READ ERROR:", error)

raw_folder = ROOT / "data/raw"
raw_csvs = list(raw_folder.glob("*.csv")) if raw_folder.exists() else []
print("CSV files in raw data folder:", len(raw_csvs))
for file in raw_csvs:
    print("Raw CSV:", file.name)

print()
print("=== FINAL SUMMARY ===")
print(f"Required files present: {passed}/{len(required_files)}")
print("Missing required files:", len(missing))

if not missing:
    print("FILE AUDIT: PASS")
else:
    print("FILE AUDIT: NEEDS REVIEW")
