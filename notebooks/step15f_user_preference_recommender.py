import pandas as pd
import numpy as np


print("=" * 60)
print("STEP 15.6 - USER PREFERENCE RECOMMENDER")
print("=" * 60)


# ============================================================
# 1. LOAD DATA
# ============================================================

product_file = (
    "data/processed/"
    "clothing_products_modeling_ready.csv"
)

similarity_file = (
    "data/processed/"
    "product_similarity_matrix.npy"
)

df = pd.read_csv(
    product_file,
    keep_default_na=False
)

similarity_matrix = np.load(
    similarity_file
)

print("\n1. INPUT DATA")
print("-" * 60)

print(f"Products: {len(df)}")
print(
    f"Similarity matrix: "
    f"{similarity_matrix.shape}"
)


# ============================================================
# 2. DISPLAY AVAILABLE USER PREFERENCES
# ============================================================

print("\n2. AVAILABLE USER PREFERENCES")
print("-" * 60)

print("\nDepartments:")
print(
    sorted(
        df["Department_Name"]
        .unique()
        .tolist()
    )
)

print("\nClasses:")
print(
    sorted(
        df["Class_Name"]
        .unique()
        .tolist()
    )
)


# ============================================================
# 3. RECOMMENDATION FUNCTION
# ============================================================

def recommend_for_user(
    department=None,
    product_class=None,
    minimum_rating=4.0,
    minimum_recommendation_rate=80.0,
    number_of_recommendations=5
):

    candidates = df.copy()

    # --------------------------------------------------------
    # Department preference
    # --------------------------------------------------------

    if department is not None:

        candidates = candidates[
            candidates["Department_Name"]
            .str.lower()
            == department.lower()
        ]

    # --------------------------------------------------------
    # Class preference
    # --------------------------------------------------------

    if product_class is not None:

        candidates = candidates[
            candidates["Class_Name"]
            .str.lower()
            == product_class.lower()
        ]

    # --------------------------------------------------------
    # Rating preference
    # --------------------------------------------------------

    candidates = candidates[
        candidates["Average_Rating"]
        >= minimum_rating
    ]

    # --------------------------------------------------------
    # Recommendation preference
    # --------------------------------------------------------

    candidates = candidates[
        candidates["Recommendation_Rate"]
        >= minimum_recommendation_rate
    ]

    # --------------------------------------------------------
    # Calculate user preference score
    # --------------------------------------------------------

    if len(candidates) == 0:
        return candidates

    candidates = candidates.copy()

    candidates["User_Preference_Score"] = (
        0.40
        * candidates["Rating_Score"]

        + 0.30
        * (
            candidates["Recommendation_Rate"]
            / 100
        )

        + 0.20
        * candidates["Sentiment_Score"]

        + 0.10
        * candidates["Review_Confidence"]
    )

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    candidates = candidates.sort_values(
        "User_Preference_Score",
        ascending=False
    )

    return candidates.head(
        number_of_recommendations
    ).copy()


# ============================================================
# 4. DEFINE TEST USER PREFERENCES
# ============================================================

print("\n3. TEST USER PREFERENCES")
print("-" * 60)

user_department = "Tops"
user_class = "Knits"
minimum_rating = 4.0
minimum_recommendation_rate = 80.0
number_of_recommendations = 5

print(
    f"Department: {user_department}"
)

print(
    f"Class: {user_class}"
)

print(
    f"Minimum rating: {minimum_rating}"
)

print(
    f"Minimum recommendation rate: "
    f"{minimum_recommendation_rate}%"
)

print(
    f"Number of recommendations: "
    f"{number_of_recommendations}"
)


# ============================================================
# 5. GENERATE RECOMMENDATIONS
# ============================================================

recommendations = recommend_for_user(
    department=user_department,
    product_class=user_class,
    minimum_rating=minimum_rating,
    minimum_recommendation_rate=(
        minimum_recommendation_rate
    ),
    number_of_recommendations=(
        number_of_recommendations
    )
)


# ============================================================
# 6. DISPLAY RESULTS
# ============================================================

print("\n4. USER PREFERENCE RECOMMENDATIONS")
print("-" * 60)

if len(recommendations) == 0:

    print(
        "No products matched the selected "
        "user preferences."
    )

else:

    display_columns = [
        "Clothing ID",
        "User_Preference_Score",
        "Average_Rating",
        "Recommendation_Rate",
        "Average_Sentiment",
        "Review_Count",
        "Department_Name",
        "Class_Name"
    ]

    recommendations[
        "User_Preference_Score"
    ] = recommendations[
        "User_Preference_Score"
    ].round(4)

    print(
        recommendations[
            display_columns
        ].to_string(index=False)
    )


# ============================================================
# 7. VERIFY USER PREFERENCES
# ============================================================

print("\n5. PREFERENCE VALIDATION")
print("-" * 60)

if len(recommendations) > 0:

    department_valid = (
        recommendations["Department_Name"]
        .str.lower()
        == user_department.lower()
    ).all()

    class_valid = (
        recommendations["Class_Name"]
        .str.lower()
        == user_class.lower()
    ).all()

    rating_valid = (
        recommendations["Average_Rating"]
        >= minimum_rating
    ).all()

    recommendation_rate_valid = (
        recommendations["Recommendation_Rate"]
        >= minimum_recommendation_rate
    ).all()

    print(
        f"Department preference satisfied: "
        f"{department_valid}"
    )

    print(
        f"Class preference satisfied: "
        f"{class_valid}"
    )

    print(
        f"Minimum rating satisfied: "
        f"{rating_valid}"
    )

    print(
        f"Minimum recommendation rate satisfied: "
        f"{recommendation_rate_valid}"
    )

else:

    print(
        "Validation skipped because no "
        "products matched."
    )


# ============================================================
# 8. SAVE RECOMMENDATIONS
# ============================================================

output_file = (
    "data/processed/"
    "user_preference_recommendations.csv"
)

recommendations.to_csv(
    output_file,
    index=False
)


# ============================================================
# 9. FINAL STATUS
# ============================================================

print("\n" + "=" * 60)
print("USER PREFERENCE RECOMMENDER COMPLETE")
print("=" * 60)

print(
    f"Recommendations generated: "
    f"{len(recommendations)}"
)

print(
    f"Output file: "
    f"{output_file}"
)

print("\nSTEP 15.6 STATUS: COMPLETE")
print("=" * 60)