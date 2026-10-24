import pandas as pd
import os

from sklearn.preprocessing import StandardScaler


print("=" * 60)
print("STEP 12 - ML PREPROCESSING")
print("=" * 60)


# ------------------------------------------------------------
# 1. LOAD FEATURE-ENGINEERED DATA
# ------------------------------------------------------------

input_file = r"data\processed\clothing_reviews_feature_engineered.csv"

df = pd.read_csv(input_file)

print("\nInput dataset shape:")
print(df.shape)


# ------------------------------------------------------------
# 2. DISPLAY INPUT COLUMNS
# ------------------------------------------------------------

print("\nInput columns:")

for column in df.columns:
    print("-", column)


# ------------------------------------------------------------
# 3. DEFINE TARGET
# ------------------------------------------------------------

target_column = "Recommended IND"

print("\n" + "=" * 60)
print("TARGET VARIABLE")
print("=" * 60)

print("\nTarget:")
print(target_column)

print("\nTarget distribution:")
print(df[target_column].value_counts())


# ------------------------------------------------------------
# 4. DEFINE CATEGORICAL FEATURES
# ------------------------------------------------------------

categorical_columns = [
    "Age Group",
    "Division Name",
    "Department Name",
    "Class Name"
]

print("\n" + "=" * 60)
print("CATEGORICAL FEATURES")
print("=" * 60)

for column in categorical_columns:
    print("-", column)


# ------------------------------------------------------------
# 5. DEFINE NUMERICAL FEATURES
# ------------------------------------------------------------

numerical_columns = [
    "Age",
    "Rating",
    "Positive Feedback Count",
    "Review Text Length",
    "Title Length",
    "Has Review",
    "Has Title",
    "Sentiment Polarity",
    "Positive Feedback Normalized"
]

print("\n" + "=" * 60)
print("NUMERICAL FEATURES")
print("=" * 60)

for column in numerical_columns:
    print("-", column)


# ------------------------------------------------------------
# 6. CHECK REQUIRED COLUMNS
# ------------------------------------------------------------

required_columns = (
    categorical_columns +
    numerical_columns +
    [target_column]
)

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

print("\n" + "=" * 60)
print("REQUIRED COLUMN CHECK")
print("=" * 60)

if len(missing_columns) == 0:
    print("\nAll required preprocessing columns are present.")
else:
    print("\nMissing columns:")
    print(missing_columns)
    raise ValueError("Required columns are missing.")


# ------------------------------------------------------------
# 7. CHECK MISSING VALUES
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("MISSING VALUE CHECK")
print("=" * 60)

missing_values = df[required_columns].isnull().sum()

print(missing_values)

if missing_values.sum() == 0:
    print("\nNo missing values found.")
else:
    print("\nWARNING: Missing values detected.")


# ------------------------------------------------------------
# 8. ONE-HOT ENCODING
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("ONE-HOT ENCODING")
print("=" * 60)

encoded_categorical = pd.get_dummies(
    df[categorical_columns],
    prefix=categorical_columns,
    dtype=int
)

print("\nEncoded categorical shape:")
print(encoded_categorical.shape)

print("\nEncoded categorical columns:")

for column in encoded_categorical.columns:
    print("-", column)


# ------------------------------------------------------------
# 9. NUMERICAL DATA
# ------------------------------------------------------------

numerical_data = df[numerical_columns].copy()


# ------------------------------------------------------------
# 10. SCALING
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("STANDARD SCALING")
print("=" * 60)

scaler = StandardScaler()

scaled_numerical = scaler.fit_transform(
    numerical_data
)

scaled_numerical_df = pd.DataFrame(
    scaled_numerical,
    columns=numerical_columns,
    index=df.index
)

print("\nScaled numerical shape:")
print(scaled_numerical_df.shape)


# ------------------------------------------------------------
# 11. COMBINE PREPROCESSED FEATURES
# ------------------------------------------------------------

X = pd.concat(
    [
        scaled_numerical_df,
        encoded_categorical
    ],
    axis=1
)

y = df[target_column].copy()


# ------------------------------------------------------------
# 12. PREPROCESSING SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("PREPROCESSING SUMMARY")
print("=" * 60)

print("\nFeature matrix shape:")
print(X.shape)

print("\nTarget shape:")
print(y.shape)

print("\nNumber of ML features:")
print(X.shape[1])


# ------------------------------------------------------------
# 13. CHECK SCALED FEATURES
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("SCALED FEATURE CHECK")
print("=" * 60)

print("\nMean of scaled numerical features:")
print(
    scaled_numerical_df.mean().round(4)
)

print("\nStandard deviation of scaled numerical features:")
print(
    scaled_numerical_df.std().round(4)
)


# ------------------------------------------------------------
# 14. CHECK ENCODED DATA
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("ENCODED FEATURE CHECK")
print("=" * 60)

print("\nEncoded categorical values:")
print(
    encoded_categorical.sum().sort_values(ascending=False)
)


# ------------------------------------------------------------
# 15. COMBINE X + TARGET
# ------------------------------------------------------------

ml_ready_data = X.copy()

ml_ready_data[target_column] = y.values


# ------------------------------------------------------------
# 16. CREATE OUTPUT DIRECTORY
# ------------------------------------------------------------

output_dir = r"data\processed"

os.makedirs(
    output_dir,
    exist_ok=True
)


# ------------------------------------------------------------
# 17. SAVE ML-READY DATASET
# ------------------------------------------------------------

output_file = (
    r"data\processed\clothing_reviews_ml_ready.csv"
)

ml_ready_data.to_csv(
    output_file,
    index=False
)

print("\nML-ready dataset saved to:")
print(output_file)


# ------------------------------------------------------------
# 18. FINAL CHECK
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FINAL ML-READY DATASET")
print("=" * 60)

print("\nShape:")
print(ml_ready_data.shape)

print("\nMissing values:")
print(
    ml_ready_data.isnull().sum().sum()
)

print("\nDuplicate rows:")
print(
    ml_ready_data.duplicated().sum()
)


# ------------------------------------------------------------
# 19. FINAL STATUS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("STEP 12 SUMMARY")
print("=" * 60)

print("\nEncoding:")
print("- One-hot encoding applied to categorical features.")

print("\nScaling:")
print("- StandardScaler applied to numerical features.")

print("\nExcluded:")
print("- Clothing ID")
print("- Raw Title")
print("- Raw Review Text")

print("\nTarget:")
print("- Recommended IND")

print("\nOriginal feature-engineered dataset was NOT modified.")

print("\nSTEP 12 STATUS: COMPLETE")