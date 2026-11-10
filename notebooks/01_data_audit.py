
import pandas as pd
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset path
DATA_PATH = BASE_DIR / "Data" / "raw" / "Telco-Customer-Churn.csv"

# Load dataset
df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("TELECOM CUSTOMER CHURN - DATA AUDIT")
print("=" * 60)

print("\n1. DATASET SHAPE")
print(df.shape)

print("\n2. FIRST FIVE ROWS")
print(df.head())

print("\n3. COLUMN NAMES")
print(df.columns.tolist())

print("\n4. DATA TYPES")
print(df.dtypes)

print("\n5. MISSING VALUES")
print(df.isnull().sum())

print("\n6. DUPLICATE ROWS")
print(df.duplicated().sum())

print("\n7. CHURN DISTRIBUTION")
print(df["Churn"].value_counts())

print("\n8. BASIC STATISTICS")
print(df.describe(include="all").T)

print("\n" + "=" * 60)
print("DATA AUDIT COMPLETED")
print("=" * 60)
