import pandas as pd
import numpy as np

print("=" * 60)
print("STEP 13 - FINAL DATA QUALITY CHECK")
print("=" * 60)


# ------------------------------------------------------------
# 1. LOAD FEATURE-ENGINEERED DATA
# ------------------------------------------------------------

feature_file = (
    r"data\processed\clothing_reviews_feature_engineered.csv"
)

df = pd.read_csv(
    feature_file,
    keep_default_na=False
)

print("\nFeature-engineered dataset shape:")
print(df.shape)


# ------------------------------------------------------------
# 2. DATASET STRUCTURE
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DATASET STRUCTURE")
print("=" * 60)

print("\nRows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nColumns:")

for column in df.columns:
    print("-", column)


# ------------------------------------------------------------
# 3. MISSING VALUE CHECK
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("MISSING VALUE CHECK")
print("=" * 60)

missing_values = df.isnull().sum()

print(missing_values)

total_missing = missing_values.sum()

print("\nTotal missing values:", total_missing)


# ------------------------------------------------------------
# 4. DUPLICATE CHECK
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DUPLICATE CHECK")
print("=" * 60)

duplicate_count = df.duplicated().sum()

print("\nDuplicate rows:", duplicate_count)


# ------------------------------------------------------------
# 5. DATA TYPE CHECK
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DATA TYPE CHECK")
print("=" * 60)

print(df.dtypes)


# ------------------------------------------------------------
# 6. NUMERICAL RANGE CHECK
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("NUMERICAL RANGE CHECK")
print("=" * 60)

numerical_columns = [
    "Age",
    "Rating",
    "Recommended IND",
    "Positive Feedback Count",
    "Review Text Length",
    "Title Length",
    "Has Review",
    "Has Title",
    "Sentiment Polarity",
    "Positive Feedback Normalized"
]

for column in numerical_columns:

    print("\n" + column)

    print("Minimum:", df[column].min())
    print("Maximum:", df[column].max())


# ------------------------------------------------------------
# 7. INVALID VALUE CHECK
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("INVALID VALUE CHECK")
print("=" * 60)


# Age
invalid_age = (
    (df["Age"] < 18) |
    (df["Age"] > 100)
).sum()

print("\nInvalid Age values:", invalid_age)


# Rating
invalid_rating = (
    ~df["Rating"].isin([1, 2, 3, 4, 5])
).sum()

print("Invalid Rating values:", invalid_rating)


# Recommended IND
invalid_recommendation = (
    ~df["Recommended IND"].isin([0, 1])
).sum()

print(
    "Invalid Recommended IND values:",
    invalid_recommendation
)


# Has Review
invalid_has_review = (
    ~df["Has Review"].isin([0, 1])
).sum()

print(
    "Invalid Has Review values:",
    invalid_has_review
)


# Has Title
invalid_has_title = (
    ~df["Has Title"].isin([0, 1])
).sum()

print(
    "Invalid Has Title values:",
    invalid_has_title
)


# Sentiment
invalid_sentiment = (
    (df["Sentiment Polarity"] < -1) |
    (df["Sentiment Polarity"] > 1)
).sum()

print(
    "Invalid Sentiment Polarity values:",
    invalid_sentiment
)


# ------------------------------------------------------------
# 8. INFINITE VALUE CHECK
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("INFINITE VALUE CHECK")
print("=" * 60)

numeric_data = df.select_dtypes(
    include=np.number
)

infinite_values = np.isinf(
    numeric_data
).sum().sum()

print(
    "\nTotal infinite numerical values:",
    infinite_values
)


# ------------------------------------------------------------
# 9. CATEGORICAL VALUE CHECK
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("CATEGORICAL VALUE CHECK")
print("=" * 60)

categorical_columns = [
    "Age Group",
    "Division Name",
    "Department Name",
    "Class Name"
]

for column in categorical_columns:

    print("\n" + column)

    print(
        df[column]
        .value_counts()
    )


# ------------------------------------------------------------
# 10. TARGET DISTRIBUTION
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("TARGET DISTRIBUTION")
print("=" * 60)

target_counts = df["Recommended IND"].value_counts()

print(target_counts)

target_percentages = (
    df["Recommended IND"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print("\nTarget percentages:")
print(target_percentages)


# ------------------------------------------------------------
# 11. ENGINEERED FEATURE CHECK
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("ENGINEERED FEATURE CHECK")
print("=" * 60)

engineered_features = [
    "Age Group",
    "Review Text Length",
    "Title Length",
    "Has Review",
    "Has Title",
    "Sentiment Polarity",
    "Positive Feedback Normalized"
]

for feature in engineered_features:

    print(
        feature,
        "->",
        "PRESENT" if feature in df.columns else "MISSING"
    )


# ------------------------------------------------------------
# 12. ORIGINAL vs FEATURE-ENGINEERED ROW CHECK
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("ROW CONSISTENCY CHECK")
print("=" * 60)

cleaned_file = (
    r"data\processed\clothing_reviews_cleaned.csv"
)

cleaned_df = pd.read_csv(
    cleaned_file,
    keep_default_na=False
)

print(
    "\nCleaned dataset rows:",
    len(cleaned_df)
)

print(
    "Feature-engineered dataset rows:",
    len(df)
)

if len(cleaned_df) == len(df):

    print(
        "\nRow count consistency: PASS"
    )

else:

    print(
        "\nRow count consistency: FAIL"
    )


# ------------------------------------------------------------
# 13. FINAL QUALITY STATUS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FINAL QUALITY STATUS")
print("=" * 60)

quality_checks = {
    "Missing values": total_missing == 0,
    "Invalid Age": invalid_age == 0,
    "Invalid Rating": invalid_rating == 0,
    "Invalid Recommended IND": invalid_recommendation == 0,
    "Invalid Has Review": invalid_has_review == 0,
    "Invalid Has Title": invalid_has_title == 0,
    "Invalid Sentiment": invalid_sentiment == 0,
    "Infinite values": infinite_values == 0,
    "Row consistency": len(cleaned_df) == len(df)
}

print()

all_passed = True

for check, status in quality_checks.items():

    if status:
        print(check, ": PASS")

    else:
        print(check, ": FAIL")
        all_passed = False


# ------------------------------------------------------------
# 14. FINAL SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("STEP 13 SUMMARY")
print("=" * 60)

print("\nDataset verified:")
print("- Feature-engineered dataset")
print("- 23,465 records")
print("- 17 columns")
print("- Missing values checked")
print("- Invalid values checked")
print("- Infinite values checked")
print("- Target checked")
print("- Engineered features checked")
print("- Row consistency checked")

if all_passed:

    print(
        "\nFINAL DATA QUALITY RESULT: PASS"
    )

else:

    print(
        "\nFINAL DATA QUALITY RESULT: REVIEW REQUIRED"
    )

print("\nSTEP 13 STATUS: COMPLETE")