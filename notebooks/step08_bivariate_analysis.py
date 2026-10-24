import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("=" * 60)
print("STEP 8 - BIVARIATE ANALYSIS")
print("=" * 60)


# ------------------------------------------------------------
# 1. LOAD CLEANED DATA
# ------------------------------------------------------------

file_path = r"data\processed\clothing_reviews_cleaned.csv"

df = pd.read_csv(file_path)

print("\nDataset shape:")
print(df.shape)


# ------------------------------------------------------------
# 2. CREATE OUTPUT DIRECTORY
# ------------------------------------------------------------

output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)


# ------------------------------------------------------------
# 3. AGE vs RATING
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("AGE vs RATING")
print("=" * 60)

age_rating = df.groupby("Rating")["Age"].agg(
    ["count", "mean", "median", "min", "max"]
)

print("\nAge statistics by Rating:")
print(age_rating)

plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="Rating", y="Age")
plt.title("Age vs Rating")
plt.xlabel("Rating")
plt.ylabel("Age")
plt.tight_layout()

plt.savefig(
    os.path.join(output_dir, "bivariate_age_vs_rating.png")
)

plt.close()


# ------------------------------------------------------------
# 4. RATING vs RECOMMENDED IND
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("RATING vs RECOMMENDED IND")
print("=" * 60)

rating_recommended = pd.crosstab(
    df["Rating"],
    df["Recommended IND"]
)

print("\nRating vs Recommended IND:")
print(rating_recommended)

plt.figure(figsize=(8, 5))
sns.countplot(
    data=df,
    x="Rating",
    hue="Recommended IND"
)

plt.title("Rating vs Recommended IND")
plt.xlabel("Rating")
plt.ylabel("Number of Reviews")
plt.tight_layout()

plt.savefig(
    os.path.join(output_dir, "bivariate_rating_vs_recommended.png")
)

plt.close()


# ------------------------------------------------------------
# 5. DEPARTMENT vs RATING
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DEPARTMENT vs RATING")
print("=" * 60)

department_rating = pd.crosstab(
    df["Department Name"],
    df["Rating"]
)

print("\nDepartment vs Rating:")
print(department_rating)

plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df,
    x="Department Name",
    y="Rating"
)

plt.title("Department vs Rating")
plt.xlabel("Department Name")
plt.ylabel("Rating")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    os.path.join(output_dir, "bivariate_department_vs_rating.png")
)

plt.close()


# ------------------------------------------------------------
# 6. DIVISION vs RATING
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DIVISION vs RATING")
print("=" * 60)

division_rating = pd.crosstab(
    df["Division Name"],
    df["Rating"]
)

print("\nDivision vs Rating:")
print(division_rating)

plt.figure(figsize=(9, 5))
sns.boxplot(
    data=df,
    x="Division Name",
    y="Rating"
)

plt.title("Division vs Rating")
plt.xlabel("Division Name")
plt.ylabel("Rating")
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(
    os.path.join(output_dir, "bivariate_division_vs_rating.png")
)

plt.close()


# ------------------------------------------------------------
# 7. POSITIVE FEEDBACK vs RATING
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("POSITIVE FEEDBACK COUNT vs RATING")
print("=" * 60)

feedback_rating = df.groupby("Rating")["Positive Feedback Count"].agg(
    ["count", "mean", "median", "min", "max"]
)

print("\nPositive Feedback statistics by Rating:")
print(feedback_rating)

plt.figure(figsize=(8, 5))
sns.boxplot(
    data=df,
    x="Rating",
    y="Positive Feedback Count"
)

plt.title("Positive Feedback Count vs Rating")
plt.xlabel("Rating")
plt.ylabel("Positive Feedback Count")
plt.tight_layout()

plt.savefig(
    os.path.join(output_dir, "bivariate_feedback_vs_rating.png")
)

plt.close()


# ------------------------------------------------------------
# 8. DEPARTMENT vs RECOMMENDED IND
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DEPARTMENT vs RECOMMENDED IND")
print("=" * 60)

department_recommended = pd.crosstab(
    df["Department Name"],
    df["Recommended IND"]
)

print("\nDepartment vs Recommended IND:")
print(department_recommended)

plt.figure(figsize=(10, 6))
sns.countplot(
    data=df,
    x="Department Name",
    hue="Recommended IND"
)

plt.title("Department vs Recommended IND")
plt.xlabel("Department Name")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    os.path.join(output_dir, "bivariate_department_vs_recommended.png")
)

plt.close()


# ------------------------------------------------------------
# 9. FINAL SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("STEP 8 SUMMARY")
print("=" * 60)

print("\nBivariate relationships analyzed:")

print("- Age vs Rating")
print("- Rating vs Recommended IND")
print("- Department vs Rating")
print("- Division vs Rating")
print("- Positive Feedback Count vs Rating")
print("- Department vs Recommended IND")

print("\nCharts saved in:")
print(output_dir)

print("\nSTEP 8 STATUS: COMPLETE")