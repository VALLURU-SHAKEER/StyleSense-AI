import pandas as pd
import numpy as np


print("=" * 60)
print("STEP 15.5 - FINAL RECOMMENDATION RANKING")
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
# 2. DEFINE RECOMMENDATION FUNCTION
# ============================================================

def rank_recommendations(
    clothing_id,
    number_of_recommendations=5
):

    matching_rows = df.index[
        df["Clothing ID"] == clothing_id
    ].tolist()

    if not matching_rows:

        raise ValueError(
            f"Clothing ID {clothing_id} "
            "was not found."
        )

    product_index = matching_rows[0]

    # --------------------------------------------------------
    # Get cosine similarity
    # --------------------------------------------------------

    similarity_scores = similarity_matrix[
        product_index
    ]

    # --------------------------------------------------------
    # Create candidate dataframe
    # --------------------------------------------------------

    candidates = df.copy()

    candidates["Similarity_Score"] = (
        similarity_scores
    )

    # Remove selected product.

    candidates = candidates[
        candidates["Clothing ID"] != clothing_id
    ].copy()

    # --------------------------------------------------------
    # Calculate final recommendation score
    # --------------------------------------------------------

    candidates["Final_Recommendation_Score"] = (
        0.40 * candidates["Similarity_Score"]
        + 0.35 * candidates["Weighted_Score"]
        + 0.15 * (
            candidates["Recommendation_Rate"] / 100
        )
        + 0.10 * candidates["Rating_Score"]
    )

    # --------------------------------------------------------
    # Sort recommendations
    # --------------------------------------------------------

    candidates = candidates.sort_values(
        "Final_Recommendation_Score",
        ascending=False
    )

    # --------------------------------------------------------
    # Return top recommendations
    # --------------------------------------------------------

    recommendations = candidates.head(
        number_of_recommendations
    ).copy()

    recommendations[
        "Similarity_Score"
    ] = recommendations[
        "Similarity_Score"
    ].round(4)

    recommendations[
        "Final_Recommendation_Score"
    ] = recommendations[
        "Final_Recommendation_Score"
    ].round(4)

    return recommendations


# ============================================================
# 3. TEST RECOMMENDATION RANKING
# ============================================================

print("\n2. TESTING FINAL RANKING")
print("-" * 60)

test_clothing_id = int(
    df.iloc[0]["Clothing ID"]
)

print(
    f"Selected Clothing ID: "
    f"{test_clothing_id}"
)


selected_product = df[
    df["Clothing ID"] == test_clothing_id
].iloc[0]

print("\nSelected Product:")
print(
    selected_product[
        [
            "Clothing ID",
            "Average_Rating",
            "Recommendation_Rate",
            "Department_Name",
            "Class_Name"
        ]
    ].to_string()
)


# ============================================================
# 4. GENERATE TOP 5
# ============================================================

recommendations = rank_recommendations(
    test_clothing_id,
    5
)

print("\nTop 5 FINAL RECOMMENDATIONS:")
print("-" * 60)

display_columns = [
    "Clothing ID",
    "Final_Recommendation_Score",
    "Similarity_Score",
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
# 5. CHECK SCORE ORDER
# ============================================================

print("\n3. FINAL SCORE ORDER CHECK")
print("-" * 60)

scores = recommendations[
    "Final_Recommendation_Score"
].values

is_descending = np.all(
    scores[:-1] >= scores[1:]
)

print(
    "Final scores:"
)

print(
    np.round(scores, 4)
)

print(
    f"\nScores sorted descending: "
    f"{is_descending}"
)


# ============================================================
# 6. CHECK SELECTED PRODUCT EXCLUSION
# ============================================================

print("\n4. SELECTED PRODUCT EXCLUSION")
print("-" * 60)

selected_product_present = (
    test_clothing_id
    in recommendations["Clothing ID"].values
)

print(
    f"Selected product included: "
    f"{selected_product_present}"
)


# ============================================================
# 7. CHECK RECOMMENDATION QUALITY
# ============================================================

print("\n5. RECOMMENDATION QUALITY")
print("-" * 60)

print(
    f"Average rating of recommendations: "
    f"{recommendations['Average_Rating'].mean():.2f}"
)

print(
    f"Average recommendation rate: "
    f"{recommendations['Recommendation_Rate'].mean():.2f}%"
)

print(
    f"Average similarity: "
    f"{recommendations['Similarity_Score'].mean():.4f}"
)

print(
    f"Average final score: "
    f"{recommendations['Final_Recommendation_Score'].mean():.4f}"
)


# ============================================================
# 8. SAVE TEST RECOMMENDATIONS
# ============================================================

output_file = (
    "data/processed/"
    "sample_recommendations.csv"
)

recommendations.to_csv(
    output_file,
    index=False
)


# ============================================================
# FINAL STATUS
# ============================================================

print("\n" + "=" * 60)
print("FINAL RECOMMENDATION RANKING CREATED")
print("=" * 60)

print(
    f"Selected Clothing ID: "
    f"{test_clothing_id}"
)

print(
    f"Recommendations generated: "
    f"{len(recommendations)}"
)

print(
    f"Output file: "
    f"{output_file}"
)

print("\nSTEP 15.5 STATUS: COMPLETE")
print("=" * 60)