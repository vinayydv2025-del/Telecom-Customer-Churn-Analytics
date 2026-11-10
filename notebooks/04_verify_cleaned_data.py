
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR / "Data" / "processed" / "telecom_churn_cleaned.csv"
)

# Load cleaned dataset
df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("CLEANED DATASET VERIFICATION")
print("=" * 60)

print("\n1. DATASET SHAPE")
print(df.shape)

print("\n2. COLUMN NAMES")
print(df.columns.tolist())

print("\n3. DATA TYPES")
print(df.dtypes)

print("\n4. MISSING VALUES")
print(df.isnull().sum().sum())

print("\n5. DUPLICATE ROWS")
print(df.duplicated().sum())

print("\n6. DUPLICATE CUSTOMER IDs")
print(df["customer_id"].duplicated().sum())

print("\n7. CHURN DISTRIBUTION")
print(df["churn"].value_counts())

print("\n8. NUMERIC SUMMARY")
print(df[[
    "tenure",
    "monthlycharges",
    "totalcharges"
]].describe())

print("\n9. FIRST FIVE CLEANED RECORDS")
print(df.head())

print("\n" + "=" * 60)
print("VERIFICATION COMPLETED")
print("=" * 60)
