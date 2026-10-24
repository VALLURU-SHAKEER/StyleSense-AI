import pandas as pd

print("=" * 60)
print("STEP 2 - LOAD DATA")
print("=" * 60)

# Dataset path
file_path = r"data\raw\Womens Clothing E-Commerce Reviews.csv"

# Load dataset
df = pd.read_csv(file_path)

print("\nDataset loaded successfully!")

print("\nNumber of rows:", len(df))
print("Number of columns:", len(df.columns))

print("\nSTEP 2 STATUS: COMPLETE")