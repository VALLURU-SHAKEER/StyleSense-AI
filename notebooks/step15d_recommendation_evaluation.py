import pandas as pd
import numpy as np


print("=" * 60)
print("STEP 15.4 - RECOMMENDATION MODEL EVALUATION")
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
# 2. DEFINE EVALUATION FUNCTION
# ============================================================

def get_recommendations(
    clothing_id,
    number_of_recommendations=5
):

    matching_rows = df.index[
        df["Clothing ID"] == clothing_id
    ].tolist()

    if not matching_rows:
        return None

    product_index = matching_rows[0]

    scores = similarity_matrix[
        product_index
    ]

    sorted_indices = np.argsort(
        scores
    )[::-1]

    sorted_indices = [
        index
        for index in sorted_indices
        if index != product_index
    ]

    selected_indices = sorted_indices[
        :number_of_recommendations
    ]

    result = df.loc[
        selected_indices
    ].copy()

    result["Similarity_Score"] = (
        scores[selected_indices]
    )

    return result


# ============================================================
# 3. BASIC RECOMMENDATION TEST
# ============================================================

print("\n2. BASIC RECOMMENDATION TEST")
print("-" * 60)

test_id = int(
    df.iloc[0]["Clothing ID"]
)

recommendations = get_recommendations(
    test_id,
    5
)

print(
    f"Test Clothing ID: {test_id}"
)

print(
    f"Recommendations returned: "
    f"{len(recommendations)}"
)

print(
    f"Selected product included: "
    f"{test_id in recommendations['Clothing ID'].values}"
)


# ============================================================
# 4. SIMILARITY ORDER CHECK
# ============================================================

print("\n3. SIMILARITY ORDER CHECK")
print("-" * 60)

scores = recommendations[
    "Similarity_Score"
].values

is_descending = np.all(
    scores[:-1] >= scores[1:]
)

print(
    "Similarity scores:"
)

print(
    np.round(scores, 4)
)

print(
    f"\nScores sorted descending: "
    f"{is_descending}"
)


# ============================================================
# 5. CATEGORY MATCH TEST
# ============================================================

print("\n4. CATEGORY MATCH TEST")
print("-" * 60)

selected_product = df[
    df["Clothing ID"] == test_id
].iloc[0]

same_department = (
    recommendations["Department_Name"]
    == selected_product["Department_Name"]
)

same_class = (
    recommendations["Class_Name"]
    == selected_product["Class_Name"]
)

department_match_rate = (
    same_department.mean() * 100
)

class_match_rate = (
    same_class.mean() * 100
)

print(
    f"Selected department: "
    f"{selected_product['Department_Name']}"
)

print(
    f"Selected class: "
    f"{selected_product['Class_Name']}"
)

print(
    f"Same department: "
    f"{same_department.sum()}/"
    f"{len(recommendations)}"
)

print(
    f"Department match rate: "
    f"{department_match_rate:.2f}%"
)

print(
    f"Same class: "
    f"{same_class.sum()}/"
    f"{len(recommendations)}"
)

print(
    f"Class match rate: "
    f"{class_match_rate:.2f}%"
)


# ============================================================
# 6. TOP-5 AVERAGE SIMILARITY
# ============================================================

print("\n5. TOP-5 SIMILARITY")
print("-" * 60)

average_similarity = (
    recommendations["Similarity_Score"]
    .mean()
)

print(
    f"Average Top-5 similarity: "
    f"{average_similarity:.4f}"
)

print(
    f"Minimum Top-5 similarity: "
    f"{recommendations['Similarity_Score'].min():.4f}"
)

print(
    f"Maximum Top-5 similarity: "
    f"{recommendations['Similarity_Score'].max():.4f}"
)


# ============================================================
# 7. MULTIPLE PRODUCT EVALUATION
# ============================================================

print("\n6. MULTIPLE PRODUCT EVALUATION")
print("-" * 60)

sample_products = (
    df["Clothing ID"]
    .sample(
        n=min(100, len(df)),
        random_state=42
    )
    .tolist()
)

evaluation_results = []

for clothing_id in sample_products:

    recommendations = get_recommendations(
        clothing_id,
        5
    )

    if recommendations is None:
        continue

    selected = df[
        df["Clothing ID"] == clothing_id
    ].iloc[0]

    same_department_rate = (
        recommendations["Department_Name"]
        == selected["Department_Name"]
    ).mean()

    same_class_rate = (
        recommendations["Class_Name"]
        == selected["Class_Name"]
    ).mean()

    evaluation_results.append(
        {
            "Clothing_ID": clothing_id,
            "Average_Similarity":
                recommendations[
                    "Similarity_Score"
                ].mean(),
            "Department_Match_Rate":
                same_department_rate,
            "Class_Match_Rate":
                same_class_rate
        }
    )


evaluation_df = pd.DataFrame(
    evaluation_results
)


# ============================================================
# 8. OVERALL EVALUATION
# ============================================================

print("\n7. OVERALL EVALUATION")
print("-" * 60)

print(
    f"Products evaluated: "
    f"{len(evaluation_df)}"
)

print(
    f"Average Top-5 similarity: "
    f"{evaluation_df['Average_Similarity'].mean():.4f}"
)

print(
    f"Average department match rate: "
    f"{evaluation_df['Department_Match_Rate'].mean() * 100:.2f}%"
)

print(
    f"Average class match rate: "
    f"{evaluation_df['Class_Match_Rate'].mean() * 100:.2f}%"
)


# ============================================================
# 9. SAVE EVALUATION RESULTS
# ============================================================

output_file = (
    "data/processed/"
    "recommendation_evaluation.csv"
)

evaluation_df.to_csv(
    output_file,
    index=False
)


# ============================================================
# 10. FINAL STATUS
# ============================================================

print("\n" + "=" * 60)
print("RECOMMENDATION MODEL EVALUATION COMPLETE")
print("=" * 60)

print(
    f"Evaluation file: {output_file}"
)

print("\nSTEP 15.4 STATUS: COMPLETE")
print("=" * 60)