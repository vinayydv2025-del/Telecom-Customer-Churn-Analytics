
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. SET PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_PATH = BASE_DIR / "Data" / "raw" / "Telco-Customer-Churn.csv"

PROCESSED_DIR = BASE_DIR / "Data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = PROCESSED_DIR / "telecom_churn_cleaned.csv"

# --------------------------------------------------
# 2. LOAD RAW DATA
# --------------------------------------------------

df = pd.read_csv(RAW_PATH)

print("=" * 60)
print("TELECOM CUSTOMER CHURN - DATA CLEANING")
print("=" * 60)

print("\nOriginal dataset shape:", df.shape)

# --------------------------------------------------
# 3. CLEAN COLUMN NAMES
# --------------------------------------------------

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# --------------------------------------------------
# 4. CLEAN TEXT COLUMNS
# --------------------------------------------------

text_columns = df.select_dtypes(include=["object", "str"]).columns

for col in text_columns:
    df[col] = df[col].astype("string").str.strip()

# --------------------------------------------------
# 5. CONVERT TOTAL CHARGES TO NUMERIC
# --------------------------------------------------

df["totalcharges"] = pd.to_numeric(
    df["totalcharges"],
    errors="coerce"
)

# --------------------------------------------------
# 6. HANDLE MISSING TOTAL CHARGES
# --------------------------------------------------

# The 11 missing values belong to customers
# whose tenure is zero.
zero_tenure_mask = df["tenure"] == 0

df.loc[
    zero_tenure_mask & df["totalcharges"].isna(),
    "totalcharges"
] = 0

# --------------------------------------------------
# 7. CONVERT SENIOR CITIZEN TO READABLE FORMAT
# --------------------------------------------------

df["seniorcitizen"] = df["seniorcitizen"].map({
    0: "No",
    1: "Yes"
})

# --------------------------------------------------
# 8. STANDARDIZE COLUMN NAMES
# --------------------------------------------------

df = df.rename(columns={
    "customerid": "customer_id",
    "seniorcitizen": "senior_citizen"
})

# --------------------------------------------------
# 9. REMOVE DUPLICATE RECORDS
# --------------------------------------------------

duplicates_before = df.duplicated().sum()

df = df.drop_duplicates()

# --------------------------------------------------
# 10. VALIDATE CLEANED DATA
# --------------------------------------------------

print("\nCLEANING VALIDATION")

print("Final dataset shape:", df.shape)

print("\nMissing values:")
print(df.isnull().sum()[df.isnull().sum() > 0])

print("\nDuplicate rows:", df.duplicated().sum())

print("\nDuplicate customer IDs:", df["customer_id"].duplicated().sum())

print("\nTotalCharges data type:", df["totalcharges"].dtype)

print("\nZero tenure customers:")
print((df["tenure"] == 0).sum())

print("\nTotalCharges for zero tenure customers:")
print(df.loc[df["tenure"] == 0, "totalcharges"].unique())

# --------------------------------------------------
# 11. SAVE CLEANED DATASET
# --------------------------------------------------

df.to_csv(OUTPUT_PATH, index=False)

print("\nCleaned dataset saved successfully:")
print(OUTPUT_PATH)

print("\nOriginal duplicate rows removed:", duplicates_before)

print("\n" + "=" * 60)
print("DATA CLEANING COMPLETED")
print("=" * 60)
