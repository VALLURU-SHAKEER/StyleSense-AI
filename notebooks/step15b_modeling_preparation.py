import pandas as pd
import numpy as np


print("=" * 60)
print("STEP 15.2 - MODELING DATASET PREPARATION")
print("=" * 60)


# ============================================================
# 1. LOAD PRODUCT-LEVEL DATASET
# ============================================================

input_file = (
    "data/processed/"
    "clothing_products_modeling.csv"
)

df = pd.read_csv(
    input_file,
    keep_default_na=False
)

print("\n1. INPUT DATA")
print("-" * 60)

print(f"Products: {len(df)}")
print(f"Columns: {len(df.columns)}")


# ============================================================
# 2. REVIEW COUNT ANALYSIS
# ============================================================

print("\n2. REVIEW COUNT ANALYSIS")
print("-" * 60)

print(
    df["Review_Count"].describe().round(2)
)

print("\nReview count distribution:")

print(
    df["Review_Count"]
    .value_counts()
    .sort_index()
    .head(20)
)


# ============================================================
# 3. CREATE REVIEW CONFIDENCE
# ============================================================

print("\n3. CREATING REVIEW CONFIDENCE")
print("-" * 60)

max_reviews = df["Review_Count"].max()

df["Review_Confidence"] = (
    np.log1p(df["Review_Count"])
    / np.log1p(max_reviews)
)

print(
    "Review_Confidence is normalized between 0 and 1."
)

print(
    df["Review_Confidence"].describe().round(4)
)


# ============================================================
# 4. CREATE NORMALIZED RATING SCORE
# ============================================================

print("\n4. CREATING RATING SCORE")
print("-" * 60)

df["Rating_Score"] = (
    df["Average_Rating"] / 5
)

print(
    df["Rating_Score"].describe().round(4)
)


# ============================================================
# 5. CREATE SENTIMENT SCORE
# ============================================================

print("\n5. CREATING SENTIMENT SCORE")
print("-" * 60)

# Sentiment polarity ranges approximately from -1 to +1.
# Convert it to a 0-1 score.

df["Sentiment_Score"] = (
    (df["Average_Sentiment"] + 1) / 2
)

print(
    df["Sentiment_Score"].describe().round(4)
)


# ============================================================
# 6. NORMALIZE POSITIVE FEEDBACK
# ============================================================

print("\n6. CREATING FEEDBACK SCORE")
print("-" * 60)

max_feedback = df["Average_Positive_Feedback"].max()

if max_feedback > 0:

    df["Feedback_Score"] = (
        df["Average_Positive_Feedback"]
        / max_feedback
    )

else:

    df["Feedback_Score"] = 0


print(
    df["Feedback_Score"].describe().round(4)
)


# ============================================================
# 7. CREATE PRODUCT WEIGHTED SCORE
# ============================================================

print("\n7. CREATING PRODUCT WEIGHTED SCORE")
print("-" * 60)

df["Weighted_Score"] = (
    0.40 * df["Rating_Score"]
    + 0.30 * (df["Recommendation_Rate"] / 100)
    + 0.20 * df["Sentiment_Score"]
    + 0.10 * df["Feedback_Score"]
)

# Apply review confidence.

df["Weighted_Score"] = (
    df["Weighted_Score"]
    * (
        0.5
        + 0.5 * df["Review_Confidence"]
    )
)


# ============================================================
# 8. ROUND SCORES
# ============================================================

score_columns = [
    "Review_Confidence",
    "Rating_Score",
    "Sentiment_Score",
    "Feedback_Score",
    "Weighted_Score"
]

for column in score_columns:

    df[column] = df[column].round(4)


# ============================================================
# 9. DISPLAY TOP PRODUCTS
# ============================================================

print("\n8. TOP PRODUCTS BY WEIGHTED SCORE")
print("-" * 60)

top_products = (
    df.sort_values(
        "Weighted_Score",
        ascending=False
    )
    .head(20)
)

display_columns = [
    "Clothing ID",
    "Review_Count",
    "Average_Rating",
    "Recommendation_Rate",
    "Average_Sentiment",
    "Review_Confidence",
    "Weighted_Score",
    "Department_Name",
    "Class_Name"
]

print(
    top_products[
        display_columns
    ].to_string(index=False)
)


# ============================================================
# 10. CHECK SCORE RANGES
# ============================================================

print("\n9. SCORE RANGE CHECK")
print("-" * 60)

for column in score_columns:

    print(
        f"{column}: "
        f"{df[column].min():.4f} - "
        f"{df[column].max():.4f}"
    )


# ============================================================
# 11. CHECK MISSING VALUES
# ============================================================

print("\n10. MISSING VALUE CHECK")
print("-" * 60)

missing = df.isna().sum()

print(missing)

print(
    f"\nTotal missing values: "
    f"{missing.sum()}"
)


# ============================================================
# 12. CHECK DUPLICATES
# ============================================================

print("\n11. DUPLICATE CHECK")
print("-" * 60)

print(
    f"Duplicate Clothing IDs: "
    f"{df['Clothing ID'].duplicated().sum()}"
)


# ============================================================
# 13. SAVE MODELING-READY DATASET
# ============================================================

output_file = (
    "data/processed/"
    "clothing_products_modeling_ready.csv"
)

df.to_csv(
    output_file,
    index=False
)


# ============================================================
# FINAL STATUS
# ============================================================

print("\n" + "=" * 60)
print("MODELING-READY DATASET CREATED")
print("=" * 60)

print(f"Output file: {output_file}")
print(f"Products: {len(df)}")
print(f"Columns: {len(df.columns)}")

print("\nSTEP 15.2 STATUS: COMPLETE")
print("=" * 60)