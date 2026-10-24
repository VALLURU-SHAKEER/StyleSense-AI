import pandas as pd
import numpy as np
import os

print("=" * 60)
print("STEP 11 - FEATURE ENGINEERING")
print("=" * 60)


# ------------------------------------------------------------
# 1. LOAD CLEANED DATA
# ------------------------------------------------------------

input_file = r"data\processed\clothing_reviews_cleaned.csv"

df = pd.read_csv(input_file)

print("\nOriginal dataset shape:")
print(df.shape)


# ------------------------------------------------------------
# 2. CREATE FEATURE ENGINEERING OUTPUT DIRECTORY
# ------------------------------------------------------------

output_dir = r"data\processed"
os.makedirs(output_dir, exist_ok=True)


# ------------------------------------------------------------
# 3. AGE GROUP
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FEATURE 1 - AGE GROUP")
print("=" * 60)

age_bins = [17, 25, 35, 45, 55, 65, np.inf]

age_labels = [
    "18-25",
    "26-35",
    "36-45",
    "46-55",
    "56-65",
    "66+"
]

df["Age Group"] = pd.cut(
    df["Age"],
    bins=age_bins,
    labels=age_labels
)

print("\nAge Group distribution:")
print(df["Age Group"].value_counts().sort_index())


# ------------------------------------------------------------
# 4. REVIEW TEXT LENGTH
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FEATURE 2 - REVIEW TEXT LENGTH")
print("=" * 60)

df["Review Text Length"] = (
    df["Review Text"]
    .fillna("")
    .astype(str)
    .str.len()
)

print("\nReview Text Length statistics:")
print(df["Review Text Length"].describe())


# ------------------------------------------------------------
# 5. TITLE LENGTH
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FEATURE 3 - TITLE LENGTH")
print("=" * 60)

df["Title Length"] = (
    df["Title"]
    .fillna("")
    .astype(str)
    .str.len()
)

print("\nTitle Length statistics:")
print(df["Title Length"].describe())


# ------------------------------------------------------------
# 6. HAS REVIEW
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FEATURE 4 - HAS REVIEW")
print("=" * 60)

df["Has Review"] = (
    df["Review Text"].fillna("").astype(str).str.strip() != ""
).astype(int)

print("\nHas Review distribution:")
print(df["Has Review"].value_counts())


# ------------------------------------------------------------
# 7. HAS TITLE
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FEATURE 5 - HAS TITLE")
print("=" * 60)

df["Has Title"] = (
    df["Title"].fillna("").astype(str).str.strip() != ""
).astype(int)

print("\nHas Title distribution:")
print(df["Has Title"].value_counts())


# ------------------------------------------------------------
# 8. SENTIMENT POLARITY
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FEATURE 6 - SENTIMENT POLARITY")
print("=" * 60)

try:
    from textblob import TextBlob

    df["Sentiment Polarity"] = (
        df["Review Text"]
        .fillna("")
        .astype(str)
        .apply(
            lambda text: TextBlob(text).sentiment.polarity
            if text.strip() != ""
            else 0.0
        )
    )

    print("\nSentiment Polarity statistics:")
    print(df["Sentiment Polarity"].describe())

    print("\nSentiment feature created successfully.")

except ImportError:

    print("\nTextBlob is not installed.")
    print("Sentiment Polarity feature was not created.")


# ------------------------------------------------------------
# 9. POSITIVE FEEDBACK NORMALIZED
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FEATURE 7 - POSITIVE FEEDBACK NORMALIZED")
print("=" * 60)

df["Positive Feedback Normalized"] = (
    df["Positive Feedback Count"] /
    (df["Positive Feedback Count"].max() + 1)
)

print("\nPositive Feedback Normalized statistics:")
print(df["Positive Feedback Normalized"].describe())

# ------------------------------------------------------------
# 10. CHECK NEW FEATURES
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("NEW FEATURES CREATED")
print("=" * 60)

original_columns = [
    "Clothing ID",
    "Age",
    "Title",
    "Review Text",
    "Rating",
    "Recommended IND",
    "Positive Feedback Count",
    "Division Name",
    "Department Name",
    "Class Name"
]

new_features = [
    column
    for column in df.columns
    if column not in original_columns
]

print("\nNew feature columns:")

for feature in new_features:
    print("-", feature)


# ------------------------------------------------------------
# 11. CHECK MISSING VALUES
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("MISSING VALUE CHECK")
print("=" * 60)

print(df[new_features].isnull().sum())


# ------------------------------------------------------------
# 12. SAVE FEATURE-ENGINEERED DATASET
# ------------------------------------------------------------

output_file = (
    r"data\processed\clothing_reviews_feature_engineered.csv"
)

df.to_csv(
    output_file,
    index=False
)

print("\nFeature-engineered dataset saved to:")
print(output_file)


# ------------------------------------------------------------
# 13. FINAL SHAPE
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FINAL FEATURE-ENGINEERED DATASET")
print("=" * 60)

print("\nFinal shape:")
print(df.shape)

print("\nFinal columns:")

for column in df.columns:
    print("-", column)


# ------------------------------------------------------------
# 14. FINAL STATUS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("STEP 11 SUMMARY")
print("=" * 60)

print("\nFeatures created:")
for feature in new_features:
    print("-", feature)

print("\nOriginal cleaned dataset was NOT modified.")

print("\nSTEP 11 STATUS: COMPLETE")
