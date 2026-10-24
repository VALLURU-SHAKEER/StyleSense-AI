import pandas as pd

print("=" * 60)
print("STEP 4B - CLEANING INVESTIGATION")
print("=" * 60)

# Load original dataset
file_path = r"data\raw\Womens Clothing E-Commerce Reviews.csv"
df = pd.read_csv(file_path)

# --------------------------------------------------
# 1. INVESTIGATE Unnamed: 0
# --------------------------------------------------
print("\n1. Unnamed: 0 INVESTIGATION")

print("First 10 values:")
print(df["Unnamed: 0"].head(10).tolist())

print("\nLast 10 values:")
print(df["Unnamed: 0"].tail(10).tolist())

print("\nNumber of unique values:")
print(df["Unnamed: 0"].nunique())

print("\nNumber of rows:")
print(len(df))

print("\nDoes Unnamed: 0 match row index?")
print(df["Unnamed: 0"].equals(pd.Series(range(len(df)))))

# --------------------------------------------------
# 2. INVESTIGATE Division Name
# --------------------------------------------------
print("\n2. DIVISION NAME VALUES")

print(df["Division Name"].value_counts(dropna=False))

# --------------------------------------------------
# 3. SHOW ROWS WITH MISSING CATEGORY VALUES
# --------------------------------------------------
print("\n3. ROWS WITH MISSING CATEGORY VALUES")

missing_category_rows = df[
    df["Division Name"].isna()
    | df["Department Name"].isna()
    | df["Class Name"].isna()
]

print(missing_category_rows[
    [
        "Clothing ID",
        "Age",
        "Rating",
        "Recommended IND",
        "Division Name",
        "Department Name",
        "Class Name"
    ]
])

# --------------------------------------------------
# 4. CHECK RELATED CATEGORIES
# --------------------------------------------------
print("\n4. CATEGORY COMBINATIONS")

print(
    df[
        ["Division Name", "Department Name", "Class Name"]
    ].drop_duplicates().sort_values(
        ["Division Name", "Department Name", "Class Name"],
        na_position="last"
    ).to_string(index=False)
)

print("\n" + "=" * 60)
print("STEP 4B INVESTIGATION COMPLETE")
print("=" * 60)