
import pandas as pd
from pathlib import Path

# ============================================================
# TELECOM CUSTOMER CHURN - CUSTOMER RISK ANALYSIS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PREDICTIONS_PATH = (
    BASE_DIR / "reports" / "customer_churn_predictions.csv"
)

DATA_PATH = (
    BASE_DIR / "Data" / "processed" / "telecom_churn_cleaned.csv"
)

REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Load data
predictions = pd.read_csv(PREDICTIONS_PATH)
customer_data = pd.read_csv(DATA_PATH)

# ============================================================
# 1. RISK CATEGORY SUMMARY
# ============================================================

risk_summary = predictions.groupby(
    "risk_category"
).agg(
    customer_count=("customer_id", "count"),
    average_churn_probability=("churn_probability", "mean"),
    actual_churned=("actual_churn", lambda x: (x == "Yes").sum()),
    predicted_churn=("predicted_churn", lambda x: (x == "Yes").sum())
).reset_index()

risk_summary["actual_churn_rate"] = (
    risk_summary["actual_churned"] /
    risk_summary["customer_count"] * 100
)

risk_summary["customer_percentage"] = (
    risk_summary["customer_count"] /
    len(predictions) * 100
)

risk_summary.to_csv(
    REPORTS_DIR / "customer_risk_summary.csv",
    index=False
)

# ============================================================
# 2. RISK ANALYSIS BY CONTRACT TYPE
# ============================================================

merged_data = predictions.merge(
    customer_data[["customer_id", "contract"]],
    on="customer_id",
    how="left"
)

contract_risk = merged_data.groupby(
    ["contract", "risk_category"]
).agg(
    customer_count=("customer_id", "count"),
    average_churn_probability=("churn_probability", "mean"),
    actual_churned=("actual_churn", lambda x: (x == "Yes").sum())
).reset_index()

contract_risk["actual_churn_rate"] = (
    contract_risk["actual_churned"] /
    contract_risk["customer_count"] * 100
)

contract_risk.to_csv(
    REPORTS_DIR / "risk_by_contract.csv",
    index=False
)

# ============================================================
# 3. DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 60)
print("CUSTOMER RISK SUMMARY")
print("=" * 60)

print(risk_summary.round(2).to_string(index=False))

print("\n" + "=" * 60)
print("CUSTOMER RISK BY CONTRACT TYPE")
print("=" * 60)

print(contract_risk.round(2).to_string(index=False))

print("\nRISK ANALYSIS REPORTS SAVED SUCCESSFULLY")
