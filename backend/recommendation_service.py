from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "processed" / "clothing_products_modeling_ready.csv"


def recommend_products(department=None, product_class=None, minimum_rating=4.0,
                      minimum_recommendation_rate=80.0, minimum_reviews=1, top_n=5):
    if not 1 <= int(top_n) <= 50:
        raise ValueError("top_n must be between 1 and 50")
    if not 1 <= float(minimum_rating) <= 5:
        raise ValueError("minimum_rating must be between 1 and 5")
    if not 0 <= float(minimum_recommendation_rate) <= 100:
        raise ValueError("minimum_recommendation_rate must be between 0 and 100")
    if int(minimum_reviews) < 1:
        raise ValueError("minimum_reviews must be at least 1")

    df = pd.read_csv(DATA, keep_default_na=False)
    needed = ["Clothing ID", "Review_Count", "Average_Rating", "Recommendation_Rate",
              "Review_Confidence", "Rating_Score", "Sentiment_Score",
              "Department_Name", "Class_Name"]
    missing = [c for c in needed if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if department:
        df = df[df["Department_Name"].astype(str).str.casefold() == str(department).casefold()]
    if product_class:
        df = df[df["Class_Name"].astype(str).str.casefold() == str(product_class).casefold()]
    df = df[(pd.to_numeric(df["Average_Rating"]) >= float(minimum_rating)) &
            (pd.to_numeric(df["Recommendation_Rate"]) >= float(minimum_recommendation_rate)) &
            (pd.to_numeric(df["Review_Count"]) >= int(minimum_reviews))].copy()
    if df.empty:
        return df
    df["Final_Robust_Score"] = (0.40 * pd.to_numeric(df["Rating_Score"]) +
        0.30 * pd.to_numeric(df["Recommendation_Rate"]) / 100 +
        0.20 * pd.to_numeric(df["Sentiment_Score"]) +
        0.10 * pd.to_numeric(df["Review_Confidence"]))
    cols = ["Clothing ID", "Department_Name", "Class_Name", "Review_Count",
            "Average_Rating", "Recommendation_Rate", "Final_Robust_Score"]
    return df.sort_values(["Final_Robust_Score", "Review_Count"],
                          ascending=[False, False])[cols].head(int(top_n)).reset_index(drop=True)
