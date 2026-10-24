import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("=" * 60)
print("STEP 10 - CORRELATION ANALYSIS")
print("=" * 60)


# ------------------------------------------------------------
# 1. LOAD CLEANED DATA
# ------------------------------------------------------------

file_path = r"data\processed\clothing_reviews_cleaned.csv"

df = pd.read_csv(file_path)

print("\nDataset shape:")
print(df.shape)


# ------------------------------------------------------------
# 2. SELECT NUMERICAL VARIABLES
# ------------------------------------------------------------

numerical_columns = [
    "Age",
    "Rating",
    "Recommended IND",
    "Positive Feedback Count",
    "Clothing ID"
]

numerical_df = df[numerical_columns]

print("\nNumerical variables selected:")
for column in numerical_columns:
    print("-", column)


# ------------------------------------------------------------
# 3. CALCULATE CORRELATION MATRIX
# ------------------------------------------------------------

correlation_matrix = numerical_df.corr()

print("\n" + "=" * 60)
print("CORRELATION MATRIX")
print("=" * 60)

print(correlation_matrix.round(4))


# ------------------------------------------------------------
# 4. SAVE CORRELATION MATRIX
# ------------------------------------------------------------

output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)

correlation_matrix.to_csv(
    os.path.join(
        output_dir,
        "correlation_matrix.csv"
    )
)

print("\nCorrelation matrix saved to:")
print("outputs/correlation_matrix.csv")


# ------------------------------------------------------------
# 5. CORRELATION HEATMAP
# ------------------------------------------------------------

plt.figure(figsize=(10, 7))

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0
)

plt.title("Correlation Heatmap")
plt.tight_layout()

plt.savefig(
    os.path.join(
        output_dir,
        "correlation_heatmap.png"
    )
)

plt.close()

print("\nCorrelation heatmap saved to:")
print("outputs/correlation_heatmap.png")


# ------------------------------------------------------------
# 6. IDENTIFY STRONGEST CORRELATIONS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("CORRELATION INTERPRETATION")
print("=" * 60)

print("\nImportant correlation pairs:")

pairs = [
    ("Age", "Rating"),
    ("Age", "Recommended IND"),
    ("Age", "Positive Feedback Count"),
    ("Rating", "Recommended IND"),
    ("Rating", "Positive Feedback Count"),
    ("Recommended IND", "Positive Feedback Count")
]

for column1, column2 in pairs:

    value = correlation_matrix.loc[column1, column2]

    print(
        f"{column1} vs {column2}: "
        f"{value:.4f}"
    )


# ------------------------------------------------------------
# 7. IDENTIFY STRONGEST ABSOLUTE CORRELATION
# ------------------------------------------------------------

correlation_pairs = []

for i in range(len(correlation_matrix.columns)):

    for j in range(i + 1, len(correlation_matrix.columns)):

        column1 = correlation_matrix.columns[i]
        column2 = correlation_matrix.columns[j]

        value = correlation_matrix.iloc[i, j]

        correlation_pairs.append(
            (
                column1,
                column2,
                value,
                abs(value)
            )
        )


correlation_pairs.sort(
    key=lambda x: x[3],
    reverse=True
)

print("\nCorrelation pairs ranked by absolute strength:")

for column1, column2, value, absolute_value in correlation_pairs:

    print(
        f"{column1} <-> {column2}: "
        f"{value:.4f}"
    )


# ------------------------------------------------------------
# 8. ID COLUMN WARNING
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("IMPORTANT NOTE")
print("=" * 60)

print(
    "\nClothing ID is an identifier, not a meaningful "
    "predictive numerical feature."
)

print(
    "Therefore, Clothing ID correlation should not be "
    "used to make recommendation decisions."
)


# ------------------------------------------------------------
# 9. FINAL SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("STEP 10 SUMMARY")
print("=" * 60)

print("\nCorrelation analysis completed for:")
for column in numerical_columns:
    print("-", column)

print("\nOutput files:")
print("- outputs/correlation_matrix.csv")
print("- outputs/correlation_heatmap.png")

print("\nSTEP 10 STATUS: COMPLETE")