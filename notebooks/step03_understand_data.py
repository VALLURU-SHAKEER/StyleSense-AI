import pandas as pd

print("=" * 60)
print("STEP 3 - UNDERSTAND THE DATA")
print("=" * 60)

# Load dataset
file_path = r"data\raw\Womens Clothing E-Commerce Reviews.csv"
df = pd.read_csv(file_path)

# 1. Shape
print("\n1. SHAPE")
print(df.shape)

# 2. Columns
print("\n2. COLUMNS")
print(df.columns.tolist())

# 3. Info
print("\n3. DATASET INFO")
df.info()

# 4. Data types
print("\n4. DATA TYPES")
print(df.dtypes)

print("\nSTEP 3 STATUS: COMPLETE")