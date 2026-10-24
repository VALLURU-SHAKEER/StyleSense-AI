import pandas as pd


print("=" * 60)
print("STEP 14 - INSIGHTS AND CONCLUSIONS")
print("=" * 60)


# ============================================================
# 1. LOAD FEATURE-ENGINEERED DATA
# ============================================================

file = "data/processed/clothing_reviews_feature_engineered.csv"

df = pd.read_csv(file, keep_default_na=False)


# ============================================================
# 2. DATASET OVERVIEW
# ============================================================

print("\n1. DATASET OVERVIEW")
print("-" * 60)

print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Missing values: {df.isna().sum().sum()}")
print(f"Duplicate rows: {df.duplicated().sum()}")


# ============================================================
# 3. CUSTOMER AGE INSIGHTS
# ============================================================

print("\n2. CUSTOMER AGE INSIGHTS")
print("-" * 60)

print(f"Average age: {df['Age'].mean():.2f}")
print(f"Minimum age: {df['Age'].min()}")
print(f"Maximum age: {df['Age'].max()}")

print("\nAge group distribution:")
print(df["Age Group"].value_counts())


# ============================================================
# 4. RATING INSIGHTS
# ============================================================

print("\n3. RATING INSIGHTS")
print("-" * 60)

print("Rating distribution:")
print(df["Rating"].value_counts().sort_index())

print(f"\nAverage rating: {df['Rating'].mean():.2f}")


# ============================================================
# 5. RECOMMENDATION INSIGHTS
# ============================================================

print("\n4. RECOMMENDATION INSIGHTS")
print("-" * 60)

recommended = (df["Recommended IND"] == 1).sum()
not_recommended = (df["Recommended IND"] == 0).sum()

recommendation_rate = df["Recommended IND"].mean() * 100

print(f"Recommended: {recommended}")
print(f"Not recommended: {not_recommended}")
print(f"Recommendation rate: {recommendation_rate:.2f}%")

print("\nRecommendation rate by rating:")

recommendation_by_rating = (
    df.groupby("Rating")["Recommended IND"]
    .mean()
    .mul(100)
    .round(2)
)

print(recommendation_by_rating)


# ============================================================
# 6. CATEGORY INSIGHTS
# ============================================================

print("\n5. CATEGORY INSIGHTS")
print("-" * 60)

print("Top departments:")
print(df["Department Name"].value_counts().head(10))

print("\nTop product classes:")
print(df["Class Name"].value_counts().head(10))

print("\nDivision distribution:")
print(df["Division Name"].value_counts())


# ============================================================
# 7. REVIEW INSIGHTS
# ============================================================

print("\n6. REVIEW INSIGHTS")
print("-" * 60)

reviews_with_text = df["Has Review"].sum()
reviews_without_text = (df["Has Review"] == 0).sum()

titles_with_text = df["Has Title"].sum()
titles_without_text = (df["Has Title"] == 0).sum()

print(f"Reviews with text: {reviews_with_text}")
print(f"Reviews without text: {reviews_without_text}")

print(f"Reviews with title: {titles_with_text}")
print(f"Reviews without title: {titles_without_text}")

print(f"Average review length: {df['Review Text Length'].mean():.2f}")
print(f"Average title length: {df['Title Length'].mean():.2f}")


# ============================================================
# 8. SENTIMENT INSIGHTS
# ============================================================

print("\n7. SENTIMENT INSIGHTS")
print("-" * 60)

print(
    f"Average sentiment polarity: "
    f"{df['Sentiment Polarity'].mean():.4f}"
)

print(
    f"Minimum sentiment: "
    f"{df['Sentiment Polarity'].min():.4f}"
)

print(
    f"Maximum sentiment: "
    f"{df['Sentiment Polarity'].max():.4f}"
)


# ============================================================
# 9. CORRELATION INSIGHTS
# ============================================================

print("\n8. CORRELATION INSIGHTS")
print("-" * 60)

correlation_columns = [
    "Age",
    "Rating",
    "Recommended IND",
    "Positive Feedback Count"
]

correlation_matrix = df[correlation_columns].corr()

print(correlation_matrix.round(4))

rating_recommendation_corr = correlation_matrix.loc[
    "Rating",
    "Recommended IND"
]

print(
    f"\nRating vs Recommendation correlation: "
    f"{rating_recommendation_corr:.4f}"
)


# ============================================================
# 10. OUTLIER CONCLUSION
# ============================================================

print("\n9. OUTLIER CONCLUSION")
print("-" * 60)

print(
    "No valid records were removed solely because of "
    "statistical outlier detection."
)

print(
    "Age outliers were retained because the values can "
    "represent real customer ages."
)

print(
    "Rating and Recommended IND are bounded variables, "
    "so IQR flags were not treated as errors."
)

print(
    "Positive feedback outliers may represent genuine "
    "highly-engaged reviews."
)


# ============================================================
# 11. FEATURE ENGINEERING CONCLUSION
# ============================================================

print("\n10. FEATURE ENGINEERING CONCLUSION")
print("-" * 60)

engineered_features = [
    "Age Group",
    "Review Text Length",
    "Title Length",
    "Has Review",
    "Has Title",
    "Sentiment Polarity",
    "Positive Feedback Normalized"
]

for feature in engineered_features:
    if feature in df.columns:
        print(f"OK - {feature}")
    else:
        print(f"MISSING - {feature}")


# ============================================================
# 12. IMPORTANT PROJECT FINDINGS
# ============================================================

print("\n11. IMPORTANT PROJECT FINDINGS")
print("-" * 60)

print(
    "1. The dataset contains 23,465 cleaned customer reviews."
)

print(
    "2. Most customers gave positive ratings."
)

print(
    "3. Around 82% of reviews indicate that the customer "
    "recommends the product."
)

print(
    "4. Rating has a strong positive relationship with "
    "recommendation."
)

print(
    "5. Age has a very weak relationship with rating "
    "and recommendation."
)

print(
    "6. Positive feedback count has only a weak relationship "
    "with rating."
)

print(
    "7. Review sentiment provides useful textual information "
    "for future modeling."
)

print(
    "8. Clothing ID is an identifier and should not be treated "
    "as a meaningful numeric feature."
)

print(
    "9. The dataset is suitable for building a review-based "
    "fashion recommendation/ranking system."
)


# ============================================================
# 13. DATASET LIMITATIONS
# ============================================================

print("\n12. DATASET LIMITATIONS")
print("-" * 60)

print(
    "1. The dataset does not contain explicit user IDs."
)

print(
    "2. It does not contain product price, color, size, "
    "season, or occasion information."
)

print(
    "3. Therefore, highly personalized recommendations "
    "based on those attributes cannot be directly learned."
)

print(
    "4. Recommendation modeling should use only information "
    "actually available in this dataset."
)


# ============================================================
# 14. FINAL CONCLUSION
# ============================================================

print("\n13. FINAL CONCLUSION")
print("-" * 60)

print(
    "The EDA process successfully identified the structure, "
    "quality, patterns, relationships, and useful features "
    "in the fashion review data."
)

print(
    "The data is clean, complete, and ready for the "
    "modeling stage."
)

print(
    "The next stage is MODELING, where recommendation/"
    "ranking logic will be developed using the available "
    "fashion review information."
)


# ============================================================
# FINAL STATUS
# ============================================================

print("\n" + "=" * 60)
print("STEP 14 STATUS: COMPLETE")
print("=" * 60)