import pandas as pd

print("=" * 60)
print("STEP 5 - STATISTICAL UNDERSTANDING")
print("=" * 60)

# --------------------------------------------------
# LOAD CLEANED DATASET
# --------------------------------------------------

file_path = r"data\processed\clothing_reviews_cleaned.csv"
df = pd.read_csv(file_path)

print("\nDataset shape:")
print(df.shape)


# --------------------------------------------------
# 1. DESCRIPTIVE STATISTICS
# --------------------------------------------------

print("\n" + "=" * 60)
print("1. DESCRIPTIVE STATISTICS - describe()")
print("=" * 60)

print(df.describe())


# --------------------------------------------------
# 2. UNIQUE VALUES
# --------------------------------------------------

print("\n" + "=" * 60)
print("2. UNIQUE VALUES - unique()")
print("=" * 60)

columns_to_check = [
    "Rating",
    "Recommended IND",
    "Division Name",
    "Department Name",
    "Class Name"
]

for column in columns_to_check:
    print(f"\n{column}:")
    print(df[column].unique())


# --------------------------------------------------
# 3. VALUE COUNTS
# --------------------------------------------------

print("\n" + "=" * 60)
print("3. VALUE COUNTS - value_counts()")
print("=" * 60)

for column in columns_to_check:
    print(f"\n{column}:")
    print(df[column].value_counts())


# --------------------------------------------------
# COMPLETE
# --------------------------------------------------

print("\n" + "=" * 60)
print("STEP 5 STATISTICAL UNDERSTANDING COMPLETE")
print("=" * 60)