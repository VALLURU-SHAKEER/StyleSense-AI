
import pandas as pd
import numpy as np

print("=" * 65)
print("STEP 15.8 - FINAL RECOMMENDATION ROBUSTNESS EVALUATION")
print("=" * 65)

# ============================================================
# 1. LOAD DATA
# ============================================================

input_file = (
    "data/processed/"
    "clothing_products_modeling_ready.csv"
)

df = pd.read_csv(input_file, keep_default_na=False)

print("\n1. DATASET OVERVIEW")
print("-" * 65)
print(f"Products: {len(df)}")
print(f"Departments: {df['Department_Name'].nunique()}")
print(f"Classes: {df['Class_Name'].nunique()}")

required_columns = [
    "Clothing ID",
    "Review_Count",
    "Average_Rating",
    "Recommendation_Rate",
    "Average_Sentiment",
    "Review_Confidence",
    "Rating_Score",
    "Sentiment_Score",
    "Weighted_Score",
    "Department_Name",
    "Class_Name",
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(f"Required columns missing: {missing_columns}")

if df["Clothing ID"].duplicated().any():
    raise ValueError("Duplicate Clothing IDs found.")

# ============================================================
# 2. CREATE A REUSABLE RANKING FUNCTION
# ============================================================

def rank_products(
    department=None,
    product_class=None,
    minimum_rating=4.0,
    minimum_recommendation_rate=80.0,
    minimum_reviews=1,
    top_n=5,
):
    candidates = df.copy()

    if department is not None:
        candidates = candidates[
            candidates["Department_Name"].str.casefold()
            == department.casefold()
        ]

    if product_class is not None:
        candidates = candidates[
            candidates["Class_Name"].str.casefold()
            == product_class.casefold()
        ]

    candidates = candidates[
        (candidates["Average_Rating"] >= minimum_rating)
        & (
            candidates["Recommendation_Rate"]
            >= minimum_recommendation_rate
        )
        & (candidates["Review_Count"] >= minimum_reviews)
    ].copy()

    if candidates.empty:
        return candidates

    # Apply the existing product score and review confidence.
    candidates["Final_Robust_Score"] = (
        0.40 * candidates["Rating_Score"]
        + 0.30 * (candidates["Recommendation_Rate"] / 100)
        + 0.20 * candidates["Sentiment_Score"]
        + 0.10 * candidates["Review_Confidence"]
    )

    candidates = candidates.sort_values(
        ["Final_Robust_Score", "Review_Count"],
        ascending=[False, False],
    )

    return candidates.head(top_n).copy()


# ============================================================
# 3. TEST MULTIPLE PREFERENCE COMBINATIONS
# ============================================================

print("\n2. MULTIPLE PREFERENCE TESTS")
print("-" * 65)

test_cases = [
    {
        "name": "Tops / Knits",
        "department": "Tops",
        "product_class": "Knits",
    },
    {
        "name": "Dresses / Dresses",
        "department": "Dresses",
        "product_class": "Dresses",
    },
    {
        "name": "Bottoms / Jeans",
        "department": "Bottoms",
        "product_class": "Jeans",
    },
    {
        "name": "Jackets / Jackets",
        "department": "Jackets",
        "product_class": "Jackets",
    },
    {
        "name": "Intimate / Lounge",
        "department": "Intimate",
        "product_class": "Lounge",
    },
]

results = []

for case in test_cases:
    recs = rank_products(
        department=case["department"],
        product_class=case["product_class"],
        minimum_rating=4.0,
        minimum_recommendation_rate=80.0,
        minimum_reviews=1,
        top_n=5,
    )

    if recs.empty:
        results.append({
            "Test_Case": case["name"],
            "Products_Returned": 0,
            "Average_Rating": np.nan,
            "Average_Recommendation_Rate": np.nan,
            "Average_Reviews": np.nan,
            "Minimum_Review_Count": np.nan,
            "Preference_Match": False,
        })
        print(f"{case['name']}: No products matched.")
        continue

    preference_match = (
        recs["Department_Name"].str.casefold().eq(
            case["department"].casefold()
        ).all()
        and recs["Class_Name"].str.casefold().eq(
            case["product_class"].casefold()
        ).all()
    )

    results.append({
        "Test_Case": case["name"],
        "Products_Returned": len(recs),
        "Average_Rating": recs["Average_Rating"].mean(),
        "Average_Recommendation_Rate": (
            recs["Recommendation_Rate"].mean()
        ),
        "Average_Reviews": recs["Review_Count"].mean(),
        "Minimum_Review_Count": recs["Review_Count"].min(),
        "Preference_Match": preference_match,
    })

    print(f"\n{case['name']}")
    print(f"Products returned: {len(recs)}")
    print(f"Average rating: {recs['Average_Rating'].mean():.2f}")
    print(
        "Average recommendation rate: "
        f"{recs['Recommendation_Rate'].mean():.2f}%"
    )
    print(f"Minimum reviews among results: {recs['Review_Count'].min()}")
    print(f"Preferences satisfied: {preference_match}")

results_df = pd.DataFrame(results)

# ============================================================
# 4. COMPARE LOW-REVIEW AND HIGHER-REVIEW RANKINGS
# ============================================================

print("\n3. REVIEW COUNT ROBUSTNESS TEST")
print("-" * 65)

test_department = "Tops"
test_class = "Knits"

normal_results = rank_products(
    department=test_department,
    product_class=test_class,
    minimum_rating=4.0,
    minimum_recommendation_rate=80.0,
    minimum_reviews=1,
    top_n=5,
)

more_review_results = rank_products(
    department=test_department,
    product_class=test_class,
    minimum_rating=4.0,
    minimum_recommendation_rate=80.0,
    minimum_reviews=5,
    top_n=5,
)

print("Top products with at least 1 review:")
if normal_results.empty:
    print("No products matched.")
else:
    print(
        normal_results[
            ["Clothing ID", "Review_Count", "Average_Rating",
             "Recommendation_Rate", "Final_Robust_Score"]
        ].to_string(index=False)
    )

print("\nTop products with at least 5 reviews:")
if more_review_results.empty:
    print("No products matched.")
else:
    print(
        more_review_results[
            ["Clothing ID", "Review_Count", "Average_Rating",
             "Recommendation_Rate", "Final_Robust_Score"]
        ].to_string(index=False)
    )

# ============================================================
# 5. GENERAL DATA QUALITY CHECKS
# ============================================================

print("\n4. DATA QUALITY CHECKS")
print("-" * 65)

print(f"Missing values: {df.isna().sum().sum()}")
print(f"Duplicate Clothing IDs: {df['Clothing ID'].duplicated().sum()}")
print(
    "Invalid ratings: "
    f"{((df['Average_Rating'] < 1) | (df['Average_Rating'] > 5)).sum()}"
)
print(
    "Invalid recommendation rates: "
    f"{((df['Recommendation_Rate'] < 0) | (df['Recommendation_Rate'] > 100)).sum()}"
)
print(
    "Invalid review counts: "
    f"{(df['Review_Count'] < 1).sum()}"
)

# ============================================================
# 6. SAVE RESULTS
# ============================================================

results_file = (
    "data/processed/"
    "final_recommendation_robustness.csv"
)

results_df.to_csv(results_file, index=False)

print("\n5. EVALUATION SUMMARY")
print("-" * 65)
print(f"Preference combinations tested: {len(results_df)}")
print(
    "Combinations returning products: "
    f"{(results_df['Products_Returned'] > 0).sum()}"
)
print(
    "Combinations satisfying exact preferences: "
    f"{results_df['Preference_Match'].sum()}"
)

print(f"\nResults saved to: {results_file}")

print("\n" + "=" * 65)
print("STEP 15.8 STATUS: COMPLETE")
print("=" * 65)