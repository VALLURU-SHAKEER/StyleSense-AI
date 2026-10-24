import pandas as pd
import numpy as np


print("=" * 60)
print("STEP 15.7 - END-TO-END RECOMMENDATION SYSTEM")
print("=" * 60)


# ============================================================
# 1. LOAD MODELING DATA
# ============================================================

input_file = (
    "data/processed/"
    "clothing_products_modeling_ready.csv"
)

df = pd.read_csv(
    input_file,
    keep_default_na=False
)

print("\n1. INPUT DATA")
print("-" * 60)

print(f"Products available: {len(df)}")


# ============================================================
# 2. CREATE RECOMMENDATION FUNCTION
# ============================================================

def recommend_fashion(
    department=None,
    product_class=None,
    minimum_rating=4.0,
    minimum_recommendation_rate=80.0,
    number_of_recommendations=5
):

    candidates = df.copy()

    fallback_used = False

    # --------------------------------------------------------
    # STEP A: Department filter
    # --------------------------------------------------------

    if department is not None:

        department_candidates = candidates[
            candidates["Department_Name"]
            .str.lower()
            == department.lower()
        ]

        if len(department_candidates) > 0:
            candidates = department_candidates

    # --------------------------------------------------------
    # STEP B: Class filter
    # --------------------------------------------------------

    if product_class is not None:

        class_candidates = candidates[
            candidates["Class_Name"]
            .str.lower()
            == product_class.lower()
        ]

        # Only use class filter if enough products exist.

        if len(class_candidates) >= number_of_recommendations:
            candidates = class_candidates

        else:
            fallback_used = True

    # --------------------------------------------------------
    # STEP C: Minimum rating
    # --------------------------------------------------------

    candidates = candidates[
        candidates["Average_Rating"]
        >= minimum_rating
    ]

    # --------------------------------------------------------
    # STEP D: Minimum recommendation rate
    # --------------------------------------------------------

    candidates = candidates[
        candidates["Recommendation_Rate"]
        >= minimum_recommendation_rate
    ]

    # --------------------------------------------------------
    # STEP E: If too few products remain,
    # use fallback
    # --------------------------------------------------------

    if len(candidates) < number_of_recommendations:

        fallback_used = True

        candidates = df.copy()

        if department is not None:

            department_candidates = candidates[
                candidates["Department_Name"]
                .str.lower()
                == department.lower()
            ]

            if len(department_candidates) > 0:
                candidates = department_candidates

        candidates = candidates[
            candidates["Average_Rating"]
            >= minimum_rating
        ]

        candidates = candidates[
            candidates["Recommendation_Rate"]
            >= minimum_recommendation_rate
        ]

    # --------------------------------------------------------
    # STEP F: Calculate final preference score
    # --------------------------------------------------------

    candidates = candidates.copy()

    candidates["Final_User_Score"] = (
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
    # STEP G: Sort
    # --------------------------------------------------------

    candidates = candidates.sort_values(
        [
            "Final_User_Score",
            "Review_Count"
        ],
        ascending=[False, False]
    )

    # --------------------------------------------------------
    # STEP H: Return Top-N
    # --------------------------------------------------------

    recommendations = candidates.head(
        number_of_recommendations
    ).copy()

    recommendations[
        "Final_User_Score"
    ] = recommendations[
        "Final_User_Score"
    ].round(4)

    return recommendations, fallback_used


# ============================================================
# 3. TEST USER PROFILE
# ============================================================

print("\n2. USER PROFILE")
print("-" * 60)

user_department = "Tops"
user_class = "Knits"
minimum_rating = 4.0
minimum_recommendation_rate = 80.0
number_of_recommendations = 5

print(f"Department: {user_department}")
print(f"Class: {user_class}")
print(f"Minimum Rating: {minimum_rating}")
print(
    f"Minimum Recommendation Rate: "
    f"{minimum_recommendation_rate}%"
)
print(f"Top-N: {number_of_recommendations}")


# ============================================================
# 4. GENERATE FINAL RECOMMENDATIONS
# ============================================================

print("\n3. GENERATING RECOMMENDATIONS")
print("-" * 60)

recommendations, fallback_used = recommend_fashion(
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

print(
    f"Fallback used: {fallback_used}"
)


# ============================================================
# 5. DISPLAY RECOMMENDATIONS
# ============================================================

print("\n4. FINAL RECOMMENDATIONS")
print("-" * 60)

if len(recommendations) == 0:

    print(
        "No products matched the selected "
        "preferences."
    )

else:

    display_columns = [
        "Clothing ID",
        "Final_User_Score",
        "Average_Rating",
        "Recommendation_Rate",
        "Average_Sentiment",
        "Review_Count",
        "Department_Name",
        "Class_Name"
    ]

    print(
        recommendations[
            display_columns
        ].to_string(index=False)
    )


# ============================================================
# 6. VALIDATE RECOMMENDATIONS
# ============================================================

print("\n5. RECOMMENDATION VALIDATION")
print("-" * 60)

if len(recommendations) > 0:

    rating_valid = (
        recommendations["Average_Rating"]
        >= minimum_rating
    ).all()

    recommendation_valid = (
        recommendations["Recommendation_Rate"]
        >= minimum_recommendation_rate
    ).all()

    score_sorted = (
        recommendations["Final_User_Score"]
        .is_monotonic_decreasing
    )

    print(
        f"Minimum rating satisfied: "
        f"{rating_valid}"
    )

    print(
        f"Minimum recommendation rate satisfied: "
        f"{recommendation_valid}"
    )

    print(
        f"Final score sorted correctly: "
        f"{score_sorted}"
    )

    print(
        f"Number of recommendations: "
        f"{len(recommendations)}"
    )


# ============================================================
# 7. RECOMMENDATION SUMMARY
# ============================================================

print("\n6. RECOMMENDATION SUMMARY")
print("-" * 60)

if len(recommendations) > 0:

    print(
        f"Average recommendation rating: "
        f"{recommendations['Average_Rating'].mean():.2f}"
    )

    print(
        f"Average recommendation rate: "
        f"{recommendations['Recommendation_Rate'].mean():.2f}%"
    )

    print(
        f"Average review count: "
        f"{recommendations['Review_Count'].mean():.2f}"
    )

    print(
        f"Average final user score: "
        f"{recommendations['Final_User_Score'].mean():.4f}"
    )


# ============================================================
# 8. SAVE FINAL RECOMMENDATIONS
# ============================================================

output_file = (
    "data/processed/"
    "final_user_recommendations.csv"
)

recommendations.to_csv(
    output_file,
    index=False
)


# ============================================================
# 9. FINAL STATUS
# ============================================================

print("\n" + "=" * 60)
print("END-TO-END RECOMMENDATION SYSTEM COMPLETE")
print("=" * 60)

print(
    f"Recommendations generated: "
    f"{len(recommendations)}"
)

print(
    f"Output file: "
    f"{output_file}"
)

print("\nSTEP 15.7 STATUS: COMPLETE")
print("=" * 60)