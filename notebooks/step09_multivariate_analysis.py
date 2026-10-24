import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("=" * 60)
print("STEP 9 - MULTIVARIATE ANALYSIS")
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
# 3. DEPARTMENT + RATING + RECOMMENDED IND
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DEPARTMENT + RATING + RECOMMENDED IND")
print("=" * 60)

department_rating_recommendation = pd.crosstab(
    [df["Department Name"], df["Rating"]],
    df["Recommended IND"]
)

print("\nDepartment + Rating + Recommended IND:")
print(department_rating_recommendation)


# ------------------------------------------------------------
# 4. DIVISION + RATING + RECOMMENDED IND
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DIVISION + RATING + RECOMMENDED IND")
print("=" * 60)

division_rating_recommendation = pd.crosstab(
    [df["Division Name"], df["Rating"]],
    df["Recommended IND"]
)

print("\nDivision + Rating + Recommended IND:")
print(division_rating_recommendation)


# ------------------------------------------------------------
# 5. DEPARTMENT + RATING + POSITIVE FEEDBACK
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DEPARTMENT + RATING + POSITIVE FEEDBACK")
print("=" * 60)

department_rating_feedback = (
    df.groupby(
        ["Department Name", "Rating"]
    )["Positive Feedback Count"]
    .agg(["count", "mean", "median"])
)

print("\nDepartment + Rating + Positive Feedback:")
print(department_rating_feedback)


# ------------------------------------------------------------
# 6. AGE GROUP + RATING + RECOMMENDATION
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("AGE GROUP + RATING + RECOMMENDATION")
print("=" * 60)

# Create age groups only for analysis.
# This does NOT modify the original cleaned dataset.

age_bins = [17, 25, 35, 45, 55, 65, 100]

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

age_rating_recommendation = pd.crosstab(
    [df["Age Group"], df["Rating"]],
    df["Recommended IND"]
)

print("\nAge Group + Rating + Recommended IND:")
print(age_rating_recommendation)


# ------------------------------------------------------------
# 7. VISUALIZATION 1
# DEPARTMENT + RATING + RECOMMENDED IND
# ------------------------------------------------------------

plt.figure(figsize=(12, 6))

sns.countplot(
    data=df,
    x="Department Name",
    hue="Rating"
)

plt.title("Department + Rating Distribution")
plt.xlabel("Department Name")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    os.path.join(
        output_dir,
        "multivariate_department_rating.png"
    )
)

plt.close()


# ------------------------------------------------------------
# 8. VISUALIZATION 2
# DIVISION + RATING
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

sns.countplot(
    data=df,
    x="Division Name",
    hue="Rating"
)

plt.title("Division + Rating Distribution")
plt.xlabel("Division Name")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(
    os.path.join(
        output_dir,
        "multivariate_division_rating.png"
    )
)

plt.close()


# ------------------------------------------------------------
# 9. VISUALIZATION 3
# AGE GROUP + RATING
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

sns.countplot(
    data=df,
    x="Age Group",
    hue="Rating"
)

plt.title("Age Group + Rating Distribution")
plt.xlabel("Age Group")
plt.ylabel("Number of Reviews")
plt.tight_layout()

plt.savefig(
    os.path.join(
        output_dir,
        "multivariate_agegroup_rating.png"
    )
)

plt.close()


# ------------------------------------------------------------
# 10. VISUALIZATION 4
# DEPARTMENT + RECOMMENDED IND + RATING
# ------------------------------------------------------------

department_rating_recommendation_plot = (
    df.groupby(
        ["Department Name", "Rating", "Recommended IND"]
    ).size()
    .reset_index(name="Count")
)

plt.figure(figsize=(12, 7))

sns.barplot(
    data=department_rating_recommendation_plot,
    x="Department Name",
    y="Count",
    hue="Recommended IND"
)

plt.title(
    "Department + Rating + Recommendation Analysis"
)

plt.xlabel("Department Name")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    os.path.join(
        output_dir,
        "multivariate_department_recommendation.png"
    )
)

plt.close()


# ------------------------------------------------------------
# 11. HEATMAP
# DEPARTMENT + RATING
# ------------------------------------------------------------

department_rating_matrix = pd.crosstab(
    df["Department Name"],
    df["Rating"]
)

plt.figure(figsize=(10, 6))

sns.heatmap(
    department_rating_matrix,
    annot=True,
    fmt="d"
)

plt.title("Department vs Rating Heatmap")
plt.xlabel("Rating")
plt.ylabel("Department Name")
plt.tight_layout()

plt.savefig(
    os.path.join(
        output_dir,
        "multivariate_department_rating_heatmap.png"
    )
)

plt.close()


# ------------------------------------------------------------
# 12. FINAL SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("STEP 9 SUMMARY")
print("=" * 60)

print("\nMultivariate relationships analyzed:")

print("- Department + Rating + Recommended IND")
print("- Division + Rating + Recommended IND")
print("- Department + Rating + Positive Feedback")
print("- Age Group + Rating + Recommended IND")

print("\nVisualizations saved in:")
print(output_dir)

print("\nSTEP 9 STATUS: COMPLETE")