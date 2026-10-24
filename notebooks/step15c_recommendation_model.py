import pandas as pd
import numpy as np

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


print("=" * 60)
print("STEP 15.3 - CONTENT-BASED RECOMMENDATION MODEL")
print("=" * 60)


# ============================================================
# 1. LOAD MODELING-READY DATA
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

print(f"Products: {len(df)}")
print(f"Columns: {len(df.columns)}")


# ============================================================
# 2. DEFINE FEATURES
# ============================================================

print("\n2. DEFINING RECOMMENDATION FEATURES")
print("-" * 60)

categorical_features = [
    "Division_Name",
    "Department_Name",
    "Class_Name"
]

numerical_features = [
    "Average_Rating",
    "Recommendation_Rate",
    "Average_Sentiment",
    "Average_Positive_Feedback",
    "Review_Confidence"
]

print("\nCategorical features:")
for feature in categorical_features:
    print(f"- {feature}")

print("\nNumerical features:")
for feature in numerical_features:
    print(f"- {feature}")


# ============================================================
# 3. ONE-HOT ENCODE CATEGORICAL FEATURES
# ============================================================

print("\n3. ENCODING CATEGORICAL FEATURES")
print("-" * 60)

encoder = OneHotEncoder(
    handle_unknown="ignore",
    sparse_output=False
)

categorical_matrix = encoder.fit_transform(
    df[categorical_features]
)

print(
    f"Categorical feature matrix shape: "
    f"{categorical_matrix.shape}"
)


# ============================================================
# 4. SCALE NUMERICAL FEATURES
# ============================================================

print("\n4. SCALING NUMERICAL FEATURES")
print("-" * 60)

scaler = StandardScaler()

numerical_matrix = scaler.fit_transform(
    df[numerical_features]
)

print(
    f"Numerical feature matrix shape: "
    f"{numerical_matrix.shape}"
)


# ============================================================
# 5. COMBINE FEATURES
# ============================================================

print("\n5. CREATING PRODUCT FEATURE MATRIX")
print("-" * 60)

feature_matrix = np.hstack(
    [
        categorical_matrix,
        numerical_matrix
    ]
)

print(
    f"Final feature matrix shape: "
    f"{feature_matrix.shape}"
)


# ============================================================
# 6. CALCULATE COSINE SIMILARITY
# ============================================================

print("\n6. CALCULATING COSINE SIMILARITY")
print("-" * 60)

similarity_matrix = cosine_similarity(
    feature_matrix
)

print(
    f"Similarity matrix shape: "
    f"{similarity_matrix.shape}"
)

print(
    f"Minimum similarity: "
    f"{similarity_matrix.min():.4f}"
)

print(
    f"Maximum similarity: "
    f"{similarity_matrix.max():.4f}"
)


# ============================================================
# 7. RECOMMENDATION FUNCTION
# ============================================================

def recommend_products(
    clothing_id,
    number_of_recommendations=5
):

    # Find selected product index.

    matching_rows = df.index[
        df["Clothing ID"] == clothing_id
    ].tolist()

    if not matching_rows:

        raise ValueError(
            f"Clothing ID {clothing_id} "
            "was not found."
        )

    product_index = matching_rows[0]

    # Get similarity scores.

    similarity_scores = similarity_matrix[
        product_index
    ]

    # Sort products by similarity.

    similar_indices = np.argsort(
        similarity_scores
    )[::-1]

    # Remove selected product itself.

    similar_indices = [
        index
        for index in similar_indices
        if index != product_index
    ]

    # Select top recommendations.

    selected_indices = similar_indices[
        :number_of_recommendations
    ]

    recommendations = df.loc[
        selected_indices
    ].copy()

    recommendations[
        "Similarity_Score"
    ] = similarity_scores[
        selected_indices
    ]

    recommendations[
        "Similarity_Score"
    ] = recommendations[
        "Similarity_Score"
    ].round(4)

    return recommendations


# ============================================================
# 8. TEST THE RECOMMENDATION ENGINE
# ============================================================

print("\n7. TESTING RECOMMENDATION ENGINE")
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
]

print("\nSelected product:")

print(
    selected_product[
        [
            "Clothing ID",
            "Average_Rating",
            "Recommendation_Rate",
            "Department_Name",
            "Class_Name"
        ]
    ].to_string(index=False)
)


# ============================================================
# 9. GENERATE TOP 5 RECOMMENDATIONS
# ============================================================

recommendations = recommend_products(
    test_clothing_id,
    number_of_recommendations=5
)

print("\nTop 5 Similar Products:")
print("-" * 60)

print(
    recommendations[
        [
            "Clothing ID",
            "Similarity_Score",
            "Average_Rating",
            "Recommendation_Rate",
            "Department_Name",
            "Class_Name"
        ]
    ].to_string(index=False)
)


# ============================================================
# 10. SIMILARITY VALIDATION
# ============================================================

print("\n8. SIMILARITY VALIDATION")
print("-" * 60)

# Diagonal should be 1 because every product
# is identical to itself.

diagonal = np.diag(similarity_matrix)

print(
    f"Minimum self-similarity: "
    f"{diagonal.min():.4f}"
)

print(
    f"Maximum self-similarity: "
    f"{diagonal.max():.4f}"
)

print(
    f"Average self-similarity: "
    f"{diagonal.mean():.4f}"
)


# ============================================================
# 11. CHECK MATRIX FOR INVALID VALUES
# ============================================================

print("\n9. SIMILARITY MATRIX QUALITY CHECK")
print("-" * 60)

print(
    f"NaN values: "
    f"{np.isnan(similarity_matrix).sum()}"
)

print(
    f"Infinite values: "
    f"{np.isinf(similarity_matrix).sum()}"
)

print(
    f"Matrix symmetric: "
    f"{np.allclose(similarity_matrix, similarity_matrix.T)}"
)


# ============================================================
# 12. SAVE SIMILARITY MATRIX
# ============================================================

output_file = (
    "data/processed/"
    "product_similarity_matrix.npy"
)

np.save(
    output_file,
    similarity_matrix
)


# ============================================================
# 13. SAVE PRODUCT INDEX MAPPING
# ============================================================

mapping_file = (
    "data/processed/"
    "product_similarity_index.csv"
)

index_mapping = df[
    [
        "Clothing ID",
        "Department_Name",
        "Class_Name"
    ]
].copy()

index_mapping[
    "Matrix_Index"
] = index_mapping.index

index_mapping.to_csv(
    mapping_file,
    index=False
)


# ============================================================
# FINAL STATUS
# ============================================================

print("\n" + "=" * 60)
print("RECOMMENDATION MODEL CREATED")
print("=" * 60)

print(
    f"Products: {len(df)}"
)

print(
    f"Feature matrix: "
    f"{feature_matrix.shape}"
)

print(
    f"Similarity matrix: "
    f"{similarity_matrix.shape}"
)

print(
    f"Similarity matrix file: "
    f"{output_file}"
)

print(
    f"Index mapping file: "
    f"{mapping_file}"
)

print("\nSTEP 15.3 STATUS: COMPLETE")
print("=" * 60)