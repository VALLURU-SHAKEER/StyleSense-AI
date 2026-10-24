import pandas as pd
import os

print("=" * 60)
print("STEP 4 - DATA CLEANING")
print("=" * 60)

# --------------------------------------------------
# 1. LOAD RAW DATA
# --------------------------------------------------

input_file = r"data\raw\Womens Clothing E-Commerce Reviews.csv"

df = pd.read_csv(input_file)

print("\nOriginal dataset shape:")
print(df.shape)


# --------------------------------------------------
# 2. REMOVE UNNAMED INDEX COLUMN
# --------------------------------------------------

df = df.drop(columns=["Unnamed: 0"])

print("\nRemoved column:")
print("Unnamed: 0")


# --------------------------------------------------
# 3. HANDLE MISSING TEXT VALUES
# --------------------------------------------------

df["Title"] = df["Title"].fillna("")
df["Review Text"] = df["Review Text"].fillna("")

print("\nMissing text values handled:")
print("Title")
print("Review Text")


# --------------------------------------------------
# 4. HANDLE MISSING CATEGORY VALUES
# --------------------------------------------------

category_columns = [
    "Division Name",
    "Department Name",
    "Class Name"
]

for column in category_columns:
    df[column] = df[column].fillna("Unknown")

print("\nMissing category values replaced with:")
print("Unknown")


# --------------------------------------------------
# 5. FIX INCONSISTENT CATEGORY
# --------------------------------------------------

df["Division Name"] = df["Division Name"].replace(
    "Initmates",
    "Intimates"
)

print("\nCategory correction:")
print("Initmates -> Intimates")


# --------------------------------------------------
# 6. REMOVE DUPLICATES
# --------------------------------------------------

duplicate_count = df.duplicated().sum()

print("\nDuplicate rows found:", duplicate_count)

if duplicate_count > 0:
    df = df.drop_duplicates()
    print("Duplicate rows removed.")
else:
    print("No duplicate rows to remove.")


# --------------------------------------------------
# 7. SAVE CLEANED DATASET
# --------------------------------------------------

output_folder = r"data\processed"

os.makedirs(output_folder, exist_ok=True)

output_file = os.path.join(
    output_folder,
    "clothing_reviews_cleaned.csv"
)

df.to_csv(output_file, index=False)

print("\nCleaned dataset saved to:")
print(output_file)


# --------------------------------------------------
# 8. FINAL CLEANING SUMMARY
# --------------------------------------------------

print("\nFinal dataset shape:")
print(df.shape)

print("\nRemaining missing values:")
print(df.isnull().sum())

print("\nFinal duplicate count:")
print(df.duplicated().sum())

print("\nFinal columns:")
print(df.columns.tolist())

print("\n" + "=" * 60)
print("STEP 4 DATA CLEANING COMPLETE")
print("=" * 60)