
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. SET PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "Data" / "raw" / "Telco-Customer-Churn.csv"

# --------------------------------------------------
# 2. LOAD DATASET
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

# --------------------------------------------------
# 3. CHECK BLANK STRINGS
# --------------------------------------------------

text_columns = df.select_dtypes(include=["object", "str"])

blank_counts = text_columns.apply(
    lambda col: col.astype("string").str.strip().eq("").sum()
)

# --------------------------------------------------
# 4. CHECK TOTAL CHARGES CONVERSION
# --------------------------------------------------

total_charges = pd.to_numeric(
    df["TotalCharges"].astype("string").str.strip(),
    errors="coerce"
)

# --------------------------------------------------
# 5. DATA QUALITY REPORT
# --------------------------------------------------

print("=" * 60)
print("TELECOM CUSTOMER CHURN - DATA QUALITY REPORT")
print("=" * 60)

print("\n1. DATASET DIMENSIONS")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\n2. BLANK STRINGS IN TEXT COLUMNS")
print(blank_counts[blank_counts > 0])

print("\n3. TOTAL CHARGES VALIDATION")
print("Invalid or blank values:", total_charges.isna().sum())

print("\n4. MISSING VALUES AFTER NUMERIC CONVERSION")
print(total_charges.isna().sum())

print("\n5. INVALID NUMERIC VALUES")
print("Negative tenure:", (df["tenure"] < 0).sum())
print("Negative monthly charges:", (df["MonthlyCharges"] < 0).sum())
print("Negative total charges:", (total_charges < 0).sum())

print("\n6. CUSTOMER ID VALIDATION")
print("Unique customer IDs:", df["customerID"].nunique())
print("Total records:", len(df))
print("Duplicate customer IDs:", df["customerID"].duplicated().sum())

print("\n7. CHURN DISTRIBUTION")
print(df["Churn"].value_counts())

print("\n8. OVERALL CHURN RATE")
churn_rate = df["Churn"].eq("Yes").mean() * 100
print(f"{churn_rate:.2f}%")

print("\n9. ZERO TENURE CUSTOMERS")
print("Customers with zero tenure:", (df["tenure"] == 0).sum())

print("\n" + "=" * 60)
print("DATA QUALITY CHECK COMPLETED")
print("=" * 60)


