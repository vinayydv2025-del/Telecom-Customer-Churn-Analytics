
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load feature importance report
REPORT_PATH = BASE_DIR / "reports" / "random_forest_feature_importance.csv"

df = pd.read_csv(REPORT_PATH)

# Select top 20 features
df = df.sort_values(
    by="Importance",
    ascending=True
).tail(20)

# Create figure
plt.figure(figsize=(12, 9))

plt.barh(
    df["Feature"],
    df["Importance"]
)

plt.title(
    "Top 20 Factors Influencing Customer Churn",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Feature Importance")
plt.ylabel("Features")

plt.tight_layout()

# Save chart
FIGURE_DIR = BASE_DIR / "reports" / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

plt.savefig(
    FIGURE_DIR / "top_20_churn_factors.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("FEATURE IMPORTANCE VISUALIZATION SAVED SUCCESSFULLY")
