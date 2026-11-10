
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "Data" / "processed" / "telecom_churn_cleaned.csv"

REPORT_DIR = BASE_DIR / "reports"
FIGURE_DIR = REPORT_DIR / "figures"

FIGURE_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

print("=" * 65)
print("TELECOM CUSTOMER CHURN - EXPLORATORY DATA ANALYSIS")
print("=" * 65)

# --------------------------------------------------
# 3. CREATE KEY BUSINESS METRICS
# --------------------------------------------------

total_customers = df["customer_id"].nunique()

churned_customers = (df["churn"] == "Yes").sum()

retained_customers = (df["churn"] == "No").sum()

churn_rate = churned_customers / total_customers * 100

retention_rate = retained_customers / total_customers * 100

total_monthly_revenue = df["monthlycharges"].sum()

avg_monthly_charge = df["monthlycharges"].mean()

avg_tenure = df["tenure"].mean()

print("\n1. OVERALL BUSINESS METRICS")

print("Total Customers:", total_customers)
print("Churned Customers:", churned_customers)
print("Retained Customers:", retained_customers)
print(f"Churn Rate: {churn_rate:.2f}%")
print(f"Retention Rate: {retention_rate:.2f}%")
print(f"Total Monthly Charges: {total_monthly_revenue:,.2f}")
print(f"Average Monthly Charge: {avg_monthly_charge:.2f}")
print(f"Average Customer Tenure: {avg_tenure:.2f} months")

# --------------------------------------------------
# 4. CHURN BY CONTRACT TYPE
# --------------------------------------------------

contract_analysis = (
    df.groupby("contract")
    .agg(
        total_customers=("customer_id", "count"),
        churned_customers=("churn", lambda x: (x == "Yes").sum())
    )
)

contract_analysis["churn_rate"] = (
    contract_analysis["churned_customers"]
    / contract_analysis["total_customers"] * 100
)

print("\n2. CHURN BY CONTRACT TYPE")
print(contract_analysis.round(2))

contract_analysis.to_csv(
    REPORT_DIR / "churn_by_contract.csv"
)

# --------------------------------------------------
# 5. CHURN BY INTERNET SERVICE
# --------------------------------------------------

internet_analysis = (
    df.groupby("internetservice")
    .agg(
        total_customers=("customer_id", "count"),
        churned_customers=("churn", lambda x: (x == "Yes").sum())
    )
)

internet_analysis["churn_rate"] = (
    internet_analysis["churned_customers"]
    / internet_analysis["total_customers"] * 100
)

print("\n3. CHURN BY INTERNET SERVICE")
print(internet_analysis.round(2))

internet_analysis.to_csv(
    REPORT_DIR / "churn_by_internet_service.csv"
)

# --------------------------------------------------
# 6. CHURN BY PAYMENT METHOD
# --------------------------------------------------

payment_analysis = (
    df.groupby("paymentmethod")
    .agg(
        total_customers=("customer_id", "count"),
        churned_customers=("churn", lambda x: (x == "Yes").sum())
    )
)

payment_analysis["churn_rate"] = (
    payment_analysis["churned_customers"]
    / payment_analysis["total_customers"] * 100
)

print("\n4. CHURN BY PAYMENT METHOD")
print(payment_analysis.round(2))

payment_analysis.to_csv(
    REPORT_DIR / "churn_by_payment_method.csv"
)

# --------------------------------------------------
# 7. CHURN BY CUSTOMER TENURE GROUP
# --------------------------------------------------

df["tenure_group"] = pd.cut(
    df["tenure"],
    bins=[-1, 12, 24, 48, 60, 72],
    labels=[
        "0-12 Months",
        "13-24 Months",
        "25-48 Months",
        "49-60 Months",
        "61-72 Months"
    ]
)

tenure_analysis = (
    df.groupby("tenure_group", observed=False)
    .agg(
        total_customers=("customer_id", "count"),
        churned_customers=("churn", lambda x: (x == "Yes").sum())
    )
)

tenure_analysis["churn_rate"] = (
    tenure_analysis["churned_customers"]
    / tenure_analysis["total_customers"] * 100
)

print("\n5. CHURN BY TENURE GROUP")
print(tenure_analysis.round(2))

tenure_analysis.to_csv(
    REPORT_DIR / "churn_by_tenure.csv"
)

# --------------------------------------------------
# 8. CHURN BY MONTHLY CHARGES
# --------------------------------------------------

df["monthly_charge_group"] = pd.cut(
    df["monthlycharges"],
    bins=[0, 35, 70, 100, 120],
    labels=[
        "Low Charges",
        "Medium Charges",
        "High Charges",
        "Very High Charges"
    ],
    include_lowest=True
)

charges_analysis = (
    df.groupby("monthly_charge_group", observed=False)
    .agg(
        total_customers=("customer_id", "count"),
        churned_customers=("churn", lambda x: (x == "Yes").sum())
    )
)

charges_analysis["churn_rate"] = (
    charges_analysis["churned_customers"]
    / charges_analysis["total_customers"] * 100
)

print("\n6. CHURN BY MONTHLY CHARGES")
print(charges_analysis.round(2))

charges_analysis.to_csv(
    REPORT_DIR / "churn_by_monthly_charges.csv"
)

# --------------------------------------------------
# 9. CHURN BY SENIOR CITIZEN STATUS
# --------------------------------------------------

senior_analysis = (
    df.groupby("senior_citizen")
    .agg(
        total_customers=("customer_id", "count"),
        churned_customers=("churn", lambda x: (x == "Yes").sum())
    )
)

senior_analysis["churn_rate"] = (
    senior_analysis["churned_customers"]
    / senior_analysis["total_customers"] * 100
)

print("\n7. CHURN BY SENIOR CITIZEN STATUS")
print(senior_analysis.round(2))

senior_analysis.to_csv(
    REPORT_DIR / "churn_by_senior_citizen.csv"
)

# --------------------------------------------------
# 10. VISUALIZATION SETTINGS
# --------------------------------------------------

sns.set_theme(style="whitegrid")

# --------------------------------------------------
# 11. CHURN DISTRIBUTION
# --------------------------------------------------

plt.figure(figsize=(8, 5))

sns.countplot(
    data=df,
    x="churn",
    hue="churn",
    palette="Set2",
    legend=False
)

plt.title("Customer Churn Distribution")
plt.xlabel("Churn Status")
plt.ylabel("Number of Customers")

plt.tight_layout()
plt.savefig(FIGURE_DIR / "churn_distribution.png", dpi=300)
plt.close()

# --------------------------------------------------
# 12. CHURN BY CONTRACT
# --------------------------------------------------

plt.figure(figsize=(8, 5))

sns.barplot(
    data=df,
    x="contract",
    y=df["churn"].eq("Yes").astype(int),
    hue="contract",
    palette="Set2",
    legend=False
)

plt.title("Average Churn Rate by Contract Type")
plt.xlabel("Contract Type")
plt.ylabel("Churn Rate")

plt.gca().yaxis.set_major_formatter(
    plt.FuncFormatter(lambda y, _: f"{y:.0%}")
)

plt.tight_layout()
plt.savefig(FIGURE_DIR / "churn_by_contract.png", dpi=300)
plt.close()

# --------------------------------------------------
# 13. MONTHLY CHARGES DISTRIBUTION
# --------------------------------------------------

plt.figure(figsize=(8, 5))

sns.boxplot(
    data=df,
    x="churn",
    y="monthlycharges",
    hue="churn",
    palette="Set2",
    legend=False
)

plt.title("Monthly Charges vs Customer Churn")
plt.xlabel("Churn Status")
plt.ylabel("Monthly Charges")

plt.tight_layout()
plt.savefig(FIGURE_DIR / "monthly_charges_vs_churn.png", dpi=300)
plt.close()

# --------------------------------------------------
# 14. TENURE DISTRIBUTION
# --------------------------------------------------

plt.figure(figsize=(8, 5))

sns.histplot(
    data=df,
    x="tenure",
    hue="churn",
    bins=30,
    kde=True,
    multiple="stack"
)

plt.title("Customer Tenure Distribution by Churn")
plt.xlabel("Tenure (Months)")
plt.ylabel("Number of Customers")

plt.tight_layout()
plt.savefig(FIGURE_DIR / "tenure_distribution.png", dpi=300)
plt.close()

# --------------------------------------------------
# 15. CORRELATION ANALYSIS
# --------------------------------------------------

numeric_df = df[
    ["tenure", "monthlycharges", "totalcharges"]
].copy()

numeric_df["churn_numeric"] = df["churn"].map({
    "No": 0,
    "Yes": 1
})

correlation = numeric_df.corr()

print("\n8. NUMERIC CORRELATION MATRIX")
print(correlation.round(3))

plt.figure(figsize=(8, 6))

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Customer Churn Correlation Heatmap")

plt.tight_layout()
plt.savefig(FIGURE_DIR / "correlation_heatmap.png", dpi=300)
plt.close()

# --------------------------------------------------
# 16. SAVE ANALYSIS DATA
# --------------------------------------------------

df.to_csv(
    BASE_DIR / "Data" / "processed" / "telecom_churn_with_segments.csv",
    index=False
)

# --------------------------------------------------
# 17. COMPLETION
# --------------------------------------------------

print("\n" + "=" * 65)
print("EDA COMPLETED SUCCESSFULLY")
print("Reports saved in:", REPORT_DIR)
print("Charts saved in:", FIGURE_DIR)
print("=" * 65)
