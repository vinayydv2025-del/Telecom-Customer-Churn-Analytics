
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "Data" / "processed" / "telecom_churn_cleaned.csv"

REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

# Create customer tenure groups

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

print("=" * 65)
print("TELECOM CUSTOMER CHURN - DEEP DIVE ANALYSIS")
print("=" * 65)

# --------------------------------------------------
# 2. CUSTOMER VALUE COMPARISON
# --------------------------------------------------

value_analysis = (
    df.groupby("churn")
    .agg(
        customers=("customer_id", "nunique"),
        average_tenure=("tenure", "mean"),
        average_monthly_charges=("monthlycharges", "mean"),
        average_total_charges=("totalcharges", "mean"),
        total_monthly_charges=("monthlycharges", "sum")
    )
)

print("\n1. CUSTOMER VALUE BY CHURN STATUS")
print(value_analysis.round(2))

value_analysis.to_csv(
    REPORT_DIR / "customer_value_by_churn.csv"
)

# --------------------------------------------------
# 3. CHURN BY ADD-ON SERVICES
# --------------------------------------------------

service_columns = [
    "onlinesecurity",
    "onlinebackup",
    "deviceprotection",
    "techsupport",
    "streamingtv",
    "streamingmovies"
]

service_results = []

for column in service_columns:

    temp = (
        df.groupby(column)
        .agg(
            total_customers=("customer_id", "nunique"),
            churned_customers=(
                "churn",
                lambda x: (x == "Yes").sum()
            )
        )
    )

    temp["churn_rate"] = (
        temp["churned_customers"]
        / temp["total_customers"] * 100
    )

    for category, row in temp.iterrows():
        service_results.append({
            "service": column,
            "service_status": category,
            "total_customers": row["total_customers"],
            "churned_customers": row["churned_customers"],
            "churn_rate": row["churn_rate"]
        })

service_analysis = pd.DataFrame(service_results)

print("\n2. CHURN BY ADD-ON SERVICES")
print(service_analysis.round(2).to_string(index=False))

service_analysis.to_csv(
    REPORT_DIR / "churn_by_addon_services.csv",
    index=False
)

# --------------------------------------------------
# 4. CHURN BY CONTRACT AND TENURE
# --------------------------------------------------

contract_tenure = (
    df.groupby(["contract", "tenure_group"], observed=False)
    .agg(
        total_customers=("customer_id", "nunique"),
        churned_customers=(
            "churn",
            lambda x: (x == "Yes").sum()
        )
    )
)

contract_tenure["churn_rate"] = (
    contract_tenure["churned_customers"]
    / contract_tenure["total_customers"] * 100
)

print("\n3. CHURN BY CONTRACT AND TENURE")
print(contract_tenure.round(2))

contract_tenure.to_csv(
    REPORT_DIR / "churn_by_contract_and_tenure.csv"
)

# --------------------------------------------------
# 5. CHURN BY PARTNER AND DEPENDENTS
# --------------------------------------------------

for column in ["partner", "dependents"]:

    analysis = (
        df.groupby(column)
        .agg(
            total_customers=("customer_id", "nunique"),
            churned_customers=(
                "churn",
                lambda x: (x == "Yes").sum()
            )
        )
    )

    analysis["churn_rate"] = (
        analysis["churned_customers"]
        / analysis["total_customers"] * 100
    )

    print(f"\n4. CHURN BY {column.upper()}")
    print(analysis.round(2))

    analysis.to_csv(
        REPORT_DIR / f"churn_by_{column}.csv"
    )

# --------------------------------------------------
# 6. MONTHLY CHARGES OF CHURNED CUSTOMERS
# --------------------------------------------------

churned_df = df[df["churn"] == "Yes"].copy()

churned_monthly_charges = churned_df["monthlycharges"].sum()

average_churned_monthly_charge = (
    churned_df["monthlycharges"].mean()
)

print("\n5. MONTHLY CHARGES ASSOCIATED WITH CHURNED CUSTOMERS")
print(
    f"Combined monthly charges: "
    f"{churned_monthly_charges:,.2f}"
)

print(
    f"Average monthly charge per churned customer: "
    f"{average_churned_monthly_charge:.2f}"
)

# This is a snapshot-based exposure estimate,
# not verified future revenue loss.

# --------------------------------------------------
# 7. HIGH-PRIORITY CUSTOMER GROUPS
# --------------------------------------------------

priority_groups = (
    df.groupby(["contract", "tenure_group"], observed=False)
    .agg(
        total_customers=("customer_id", "nunique"),
        churned_customers=(
            "churn",
            lambda x: (x == "Yes").sum()
        )
    )
    .reset_index()
)

priority_groups["churn_rate"] = (
    priority_groups["churned_customers"]
    / priority_groups["total_customers"] * 100
)

priority_groups = priority_groups.sort_values(
    by=["churn_rate", "total_customers"],
    ascending=[False, False]
)

print("\n6. HIGHEST CHURN CUSTOMER GROUPS")
print(priority_groups.head(15).round(2).to_string(index=False))

priority_groups.to_csv(
    REPORT_DIR / "high_priority_customer_groups.csv",
    index=False
)

# --------------------------------------------------
# 8. RETENTION OPPORTUNITY SUMMARY
# --------------------------------------------------

retention_summary = pd.DataFrame({
    "metric": [
        "Total Customers",
        "Churned Customers",
        "Overall Churn Rate",
        "Month-to-Month Churn Rate",
        "First-Year Churn Rate",
        "Electronic Check Churn Rate",
        "Churned Customer Monthly Charges"
    ],
    "value": [
        df["customer_id"].nunique(),
        len(churned_df),
        df["churn"].eq("Yes").mean() * 100,
        df.loc[
            df["contract"] == "Month-to-month", "churn"
        ].eq("Yes").mean() * 100,
        df.loc[
            df["tenure"] <= 12, "churn"
        ].eq("Yes").mean() * 100,
        df.loc[
            df["paymentmethod"] == "Electronic check", "churn"
        ].eq("Yes").mean() * 100,
        churned_monthly_charges
    ]
})

print("\n7. RETENTION OPPORTUNITY SUMMARY")
print(retention_summary.round(2).to_string(index=False))

retention_summary.to_csv(
    REPORT_DIR / "retention_opportunity_summary.csv",
    index=False
)

# --------------------------------------------------
# 9. COMPLETION
# --------------------------------------------------

print("\n" + "=" * 65)
print("DEEP DIVE ANALYSIS COMPLETED")
print("Reports saved in:", REPORT_DIR)
print("=" * 65)
