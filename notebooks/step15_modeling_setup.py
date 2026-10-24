import pandas as pd


print("=" * 60)
print("STEP 15.1 - MODELING SETUP")
print("=" * 60)


# ============================================================
# 1. LOAD FEATURE-ENGINEERED DATA
# ============================================================

input_file = "data/processed/clothing_reviews_feature_engineered.csv"

df = pd.read_csv(
    input_file,
    keep_default_na=False
)

print("\n1. INPUT DATA")
print("-" * 60)

print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")


# ============================================================
# 2. CHECK CLOTHING ID
# ============================================================

print("\n2. PRODUCT IDENTIFICATION")
print("-" * 60)

print(f"Unique Clothing IDs: {df['Clothing ID'].nunique()}")

print(
    f"Average reviews per product: "
    f"{len(df) / df['Clothing ID'].nunique():.2f}"
)


# ============================================================
# 3. CREATE PRODUCT-LEVEL DATASET
# ============================================================

print("\n3. CREATING PRODUCT-LEVEL DATASET")
print("-" * 60)


product_df = (
    df.groupby("Clothing ID")
    .agg(
        Review_Count=("Clothing ID", "size"),
        Average_Rating=("Rating", "mean"),
        Recommendation_Rate=("Recommended IND", "mean"),
        Average_Sentiment=("Sentiment Polarity", "mean"),
        Average_Positive_Feedback=(
            "Positive Feedback Count",
            "mean"
        ),
        Division_Name=("Division Name", "first"),
        Department_Name=("Department Name", "first"),
        Class_Name=("Class Name", "first")
    )
    .reset_index()
)


# ============================================================
# 4. CONVERT RECOMMENDATION RATE TO PERCENTAGE
# ============================================================

product_df["Recommendation_Rate"] = (
    product_df["Recommendation_Rate"] * 100
)


# ============================================================
# 5. ROUND NUMERICAL FEATURES
# ============================================================

product_df["Average_Rating"] = (
    product_df["Average_Rating"].round(2)
)

product_df["Recommendation_Rate"] = (
    product_df["Recommendation_Rate"].round(2)
)

product_df["Average_Sentiment"] = (
    product_df["Average_Sentiment"].round(4)
)

product_df["Average_Positive_Feedback"] = (
    product_df["Average_Positive_Feedback"].round(2)
)


# ============================================================
# 6. DISPLAY PRODUCT DATASET
# ============================================================

print(f"Unique products: {len(product_df)}")
print(f"Product-level columns: {len(product_df.columns)}")

print("\nProduct-level dataset:")
print(product_df.head(10).to_string(index=False))


# ============================================================
# 7. PRODUCT DATASET INFORMATION
# ============================================================

print("\n4. PRODUCT DATASET INFORMATION")
print("-" * 60)

print(product_df.info())


# ============================================================
# 8. CHECK MISSING VALUES
# ============================================================

print("\n5. MISSING VALUE CHECK")
print("-" * 60)

missing_values = product_df.isna().sum()

print(missing_values)

print(
    f"\nTotal missing values: "
    f"{missing_values.sum()}"
)


# ============================================================
# 9. CHECK DUPLICATES
# ============================================================

print("\n6. DUPLICATE CHECK")
print("-" * 60)

duplicate_count = product_df.duplicated(
    subset=["Clothing ID"]
).sum()

print(f"Duplicate Clothing IDs: {duplicate_count}")


# ============================================================
# 10. PRODUCT STATISTICS
# ============================================================

print("\n7. PRODUCT STATISTICS")
print("-" * 60)

print(
    product_df[
        [
            "Review_Count",
            "Average_Rating",
            "Recommendation_Rate",
            "Average_Sentiment",
            "Average_Positive_Feedback"
        ]
    ].describe().round(2)
)


# ============================================================
# 11. TOP PRODUCTS BY RATING
# ============================================================

print("\n8. TOP PRODUCTS BY AVERAGE RATING")
print("-" * 60)

top_rating = (
    product_df
    .sort_values(
        ["Average_Rating", "Review_Count"],
        ascending=[False, False]
    )
    .head(10)
)

print(
    top_rating[
        [
            "Clothing ID",
            "Review_Count",
            "Average_Rating",
            "Recommendation_Rate",
            "Department_Name",
            "Class_Name"
        ]
    ].to_string(index=False)
)


# ============================================================
# 12. TOP PRODUCTS BY RECOMMENDATION RATE
# ============================================================

print("\n9. TOP PRODUCTS BY RECOMMENDATION RATE")
print("-" * 60)

top_recommendation = (
    product_df
    .sort_values(
        ["Recommendation_Rate", "Review_Count"],
        ascending=[False, False]
    )
    .head(10)
)

print(
    top_recommendation[
        [
            "Clothing ID",
            "Review_Count",
            "Average_Rating",
            "Recommendation_Rate",
            "Department_Name",
            "Class_Name"
        ]
    ].to_string(index=False)
)


# ============================================================
# 13. SAVE PRODUCT-LEVEL DATASET
# ============================================================

output_file = (
    "data/processed/"
    "clothing_products_modeling.csv"
)

product_df.to_csv(
    output_file,
    index=False
)


# ============================================================
# FINAL STATUS
# ============================================================

print("\n" + "=" * 60)
print("PRODUCT-LEVEL MODELING DATASET CREATED")
print("=" * 60)

print(f"Output file: {output_file}")
print(f"Products: {len(product_df)}")
print(f"Features: {len(product_df.columns)}")

print("\nSTEP 15.1 STATUS: COMPLETE")
print("=" * 60)