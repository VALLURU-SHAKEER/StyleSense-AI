import pandas as pd

print("=" * 60)
print("STEP 6 - OUTLIER DETECTION")
print("=" * 60)

# --------------------------------------------------
# LOAD CLEANED DATASET
# --------------------------------------------------

file_path = r"data\processed\clothing_reviews_cleaned.csv"
df = pd.read_csv(file_path)

print("\nDataset shape:")
print(df.shape)


# --------------------------------------------------
# IQR OUTLIER DETECTION FUNCTION
# --------------------------------------------------

def detect_outliers(column):

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[
        (df[column] < lower_bound) |
        (df[column] > upper_bound)
    ]

    print(f"\n{column}")
    print("-" * 40)
    print("Q1:", Q1)
    print("Q3:", Q3)
    print("IQR:", IQR)
    print("Lower Bound:", lower_bound)
    print("Upper Bound:", upper_bound)
    print("Number of Outliers:", len(outliers))
    print("Percentage of Outliers:",
          round((len(outliers) / len(df)) * 100, 2), "%")


# --------------------------------------------------
# CHECK NUMERICAL VARIABLES
# --------------------------------------------------

print("\n" + "=" * 60)
print("IQR OUTLIER ANALYSIS")
print("=" * 60)

numerical_columns = [
    "Age",
    "Clothing ID",
    "Rating",
    "Recommended IND",
    "Positive Feedback Count"
]

for column in numerical_columns:
    detect_outliers(column)


# --------------------------------------------------
# COMPLETE
# --------------------------------------------------

print("\n" + "=" * 60)
print("STEP 6 OUTLIER DETECTION COMPLETE")
print("=" * 60)