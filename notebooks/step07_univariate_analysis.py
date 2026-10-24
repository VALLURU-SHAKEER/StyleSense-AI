import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("=" * 60)
print("STEP 7 - UNIVARIATE ANALYSIS")
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
# 3. AGE ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("AGE ANALYSIS")
print("=" * 60)

print("\nAge statistics:")
print(df["Age"].describe())

plt.figure(figsize=(8, 5))
sns.histplot(df["Age"], bins=20, kde=True)
plt.title("Distribution of Age")
plt.xlabel("Age")
plt.ylabel("Number of Customers")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "univariate_age_distribution.png"))
plt.close()


# ------------------------------------------------------------
# 4. RATING ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("RATING ANALYSIS")
print("=" * 60)

print("\nRating counts:")
print(df["Rating"].value_counts().sort_index())

plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="Rating")
plt.title("Distribution of Ratings")
plt.xlabel("Rating")
plt.ylabel("Number of Reviews")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "univariate_rating_distribution.png"))
plt.close()


# ------------------------------------------------------------
# 5. RECOMMENDED IND ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("RECOMMENDED IND ANALYSIS")
print("=" * 60)

print("\nRecommended IND counts:")
print(df["Recommended IND"].value_counts().sort_index())

plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="Recommended IND")
plt.title("Distribution of Recommendation Status")
plt.xlabel("Recommended IND")
plt.ylabel("Number of Reviews")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "univariate_recommended_distribution.png"))
plt.close()


# ------------------------------------------------------------
# 6. POSITIVE FEEDBACK COUNT ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("POSITIVE FEEDBACK COUNT ANALYSIS")
print("=" * 60)

print("\nPositive Feedback Count statistics:")
print(df["Positive Feedback Count"].describe())

plt.figure(figsize=(8, 5))
sns.histplot(df["Positive Feedback Count"], bins=30, kde=True)
plt.title("Distribution of Positive Feedback Count")
plt.xlabel("Positive Feedback Count")
plt.ylabel("Number of Reviews")
plt.tight_layout()
plt.savefig(
    os.path.join(output_dir, "univariate_positive_feedback_distribution.png")
)
plt.close()


# ------------------------------------------------------------
# 7. DIVISION NAME ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DIVISION NAME ANALYSIS")
print("=" * 60)

print("\nDivision Name counts:")
print(df["Division Name"].value_counts())

plt.figure(figsize=(8, 5))
sns.countplot(
    data=df,
    y="Division Name",
    order=df["Division Name"].value_counts().index
)
plt.title("Distribution of Division Names")
plt.xlabel("Number of Reviews")
plt.ylabel("Division Name")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "univariate_division_distribution.png"))
plt.close()


# ------------------------------------------------------------
# 8. DEPARTMENT NAME ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DEPARTMENT NAME ANALYSIS")
print("=" * 60)

print("\nDepartment Name counts:")
print(df["Department Name"].value_counts())

plt.figure(figsize=(8, 5))
sns.countplot(
    data=df,
    y="Department Name",
    order=df["Department Name"].value_counts().index
)
plt.title("Distribution of Department Names")
plt.xlabel("Number of Reviews")
plt.ylabel("Department Name")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "univariate_department_distribution.png"))
plt.close()


# ------------------------------------------------------------
# 9. CLASS NAME ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("CLASS NAME ANALYSIS")
print("=" * 60)

print("\nClass Name counts:")
print(df["Class Name"].value_counts())

plt.figure(figsize=(10, 8))
sns.countplot(
    data=df,
    y="Class Name",
    order=df["Class Name"].value_counts().index
)
plt.title("Distribution of Class Names")
plt.xlabel("Number of Reviews")
plt.ylabel("Class Name")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "univariate_class_distribution.png"))
plt.close()


# ------------------------------------------------------------
# 10. FINAL STATUS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("STEP 7 SUMMARY")
print("=" * 60)

print("\nVariables analyzed:")
print("- Age")
print("- Rating")
print("- Recommended IND")
print("- Positive Feedback Count")
print("- Division Name")
print("- Department Name")
print("- Class Name")

print("\nCharts saved in:")
print(output_dir)

print("\nSTEP 7 STATUS: COMPLETE")