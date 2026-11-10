# ============================================================
# TELECOM CUSTOMER CHURN - MACHINE LEARNING
# STEP 1: LOAD DATA AND PREPARE FEATURES
# ============================================================

import pandas as pd
import numpy as np

# Load cleaned dataset
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "Data" / "processed" / "telecom_churn_cleaned.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("TELECOM CUSTOMER CHURN - MACHINE LEARNING")
print("=" * 60)

# Dataset overview
print("\n1. DATASET SHAPE")
print(df.shape)

# Target distribution
print("\n2. CHURN DISTRIBUTION")
print(df["churn"].value_counts())

# Convert target into numeric values
df["churn"] = df["churn"].map({
    "No": 0,
    "Yes": 1
})

# Remove customer ID because it is not useful for prediction
df.drop(columns=["customer_id"], inplace=True)

# Separate features and target
X = df.drop(columns=["churn"])
y = df["churn"]

# Identify categorical and numerical columns
categorical_columns = X.select_dtypes(
    include=["object"]
).columns.tolist()

numerical_columns = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()

print("\n3. CATEGORICAL COLUMNS")
print(categorical_columns)

print("\n4. NUMERICAL COLUMNS")
print(numerical_columns)

print("\n5. TARGET VALUES")
print(y.value_counts())

print("\nDATA PREPARATION COMPLETED")

# ============================================================
# STEP 2: TRAIN-TEST SPLIT
# ============================================================

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\n" + "=" * 60)
print("TRAIN-TEST SPLIT")
print("=" * 60)

print("\nTraining features:", X_train.shape)
print("Testing features:", X_test.shape)

print("\nTraining target distribution:")
print(y_train.value_counts())

print("\nTesting target distribution:")
print(y_test.value_counts())

print("\nTRAIN-TEST SPLIT COMPLETED")

# ============================================================
# STEP 3: LOGISTIC REGRESSION MODEL
# ============================================================

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix
)

# Numerical preprocessing
numerical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

# Categorical preprocessing
categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

# Combine preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numerical_transformer, numerical_columns),
        ("cat", categorical_transformer, categorical_columns)
    ]
)

# Create complete ML pipeline
logistic_model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        random_state=42
    ))
])

# Train model
logistic_model.fit(X_train, y_train)

# Predictions
y_pred = logistic_model.predict(X_test)
y_prob = logistic_model.predict_proba(X_test)[:, 1]

# Evaluation
print("\n" + "=" * 60)
print("LOGISTIC REGRESSION MODEL PERFORMANCE")
print("=" * 60)

print("\nAccuracy:", round(accuracy_score(y_test, y_pred), 4))
print("Precision:", round(precision_score(y_test, y_pred), 4))
print("Recall:", round(recall_score(y_test, y_pred), 4))
print("F1 Score:", round(f1_score(y_test, y_pred), 4))
print("ROC-AUC:", round(roc_auc_score(y_test, y_prob), 4))

print("\nCLASSIFICATION REPORT")
print(classification_report(y_test, y_pred))

print("\nCONFUSION MATRIX")
print(confusion_matrix(y_test, y_pred))

print("\nLOGISTIC REGRESSION MODEL COMPLETED")

# ============================================================
# STEP 4: RANDOM FOREST CLASSIFICATION
# ============================================================

from sklearn.ensemble import RandomForestClassifier

# Create Random Forest pipeline
random_forest_model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        min_samples_split=10,
        min_samples_leaf=4,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ))
])

# Train model
random_forest_model.fit(X_train, y_train)

# Predictions
rf_pred = random_forest_model.predict(X_test)
rf_prob = random_forest_model.predict_proba(X_test)[:, 1]

# Evaluate model
print("\n" + "=" * 60)
print("RANDOM FOREST MODEL PERFORMANCE")
print("=" * 60)

print("\nAccuracy:", round(accuracy_score(y_test, rf_pred), 4))
print("Precision:", round(precision_score(y_test, rf_pred), 4))
print("Recall:", round(recall_score(y_test, rf_pred), 4))
print("F1 Score:", round(f1_score(y_test, rf_pred), 4))
print("ROC-AUC:", round(roc_auc_score(y_test, rf_prob), 4))

print("\nCLASSIFICATION REPORT")
print(classification_report(y_test, rf_pred))

print("\nCONFUSION MATRIX")
print(confusion_matrix(y_test, rf_pred))

print("\nRANDOM FOREST MODEL COMPLETED")

# ============================================================
# STEP 5: EXTRA TREES CLASSIFICATION
# ============================================================

from sklearn.ensemble import ExtraTreesClassifier

extra_trees_model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", ExtraTreesClassifier(
        n_estimators=300,
        max_depth=12,
        min_samples_split=10,
        min_samples_leaf=4,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ))
])

# Train model
extra_trees_model.fit(X_train, y_train)

# Predictions
et_pred = extra_trees_model.predict(X_test)
et_prob = extra_trees_model.predict_proba(X_test)[:, 1]

# Evaluation
print("\n" + "=" * 60)
print("EXTRA TREES MODEL PERFORMANCE")
print("=" * 60)

print("\nAccuracy:", round(accuracy_score(y_test, et_pred), 4))
print("Precision:", round(precision_score(y_test, et_pred), 4))
print("Recall:", round(recall_score(y_test, et_pred), 4))
print("F1 Score:", round(f1_score(y_test, et_pred), 4))
print("ROC-AUC:", round(roc_auc_score(y_test, et_prob), 4))

print("\nCLASSIFICATION REPORT")
print(classification_report(y_test, et_pred))

print("\nCONFUSION MATRIX")
print(confusion_matrix(y_test, et_pred))

print("\nEXTRA TREES MODEL COMPLETED")

# ============================================================
# STEP 6: MODEL COMPARISON REPORT
# ============================================================

models = {
    "Logistic Regression": (y_pred, y_prob),
    "Random Forest": (rf_pred, rf_prob),
    "Extra Trees": (et_pred, et_prob)
}

comparison_results = []

for model_name, (predictions, probabilities) in models.items():

    comparison_results.append({
        "Model": model_name,
        "Accuracy": accuracy_score(y_test, predictions),
        "Precision": precision_score(y_test, predictions),
        "Recall": recall_score(y_test, predictions),
        "F1 Score": f1_score(y_test, predictions),
        "ROC-AUC": roc_auc_score(y_test, probabilities)
    })

comparison_df = pd.DataFrame(comparison_results)

comparison_df = comparison_df.sort_values(
    by="F1 Score",
    ascending=False
)

# Create reports folder if it does not exist
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Save comparison report
comparison_df.to_csv(
    REPORTS_DIR / "model_comparison.csv",
    index=False
)

print("\n" + "=" * 60)
print("FINAL MODEL COMPARISON")
print("=" * 60)

print(comparison_df.round(4).to_string(index=False))

print("\nMODEL COMPARISON SAVED SUCCESSFULLY")

# ============================================================
# STEP 7: SAVE TRAINED MACHINE LEARNING MODELS
# ============================================================

import joblib

MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Save all three trained models
joblib.dump(
    logistic_model,
    MODELS_DIR / "logistic_regression_model.pkl"
)

joblib.dump(
    random_forest_model,
    MODELS_DIR / "random_forest_model.pkl"
)

joblib.dump(
    extra_trees_model,
    MODELS_DIR / "extra_trees_model.pkl"
)

print("\n" + "=" * 60)
print("MACHINE LEARNING MODELS SAVED")
print("=" * 60)

print("Logistic Regression: Saved")
print("Random Forest: Saved")
print("Extra Trees: Saved")
print(f"Model location: {MODELS_DIR}")


# ============================================================
# STEP 8: RANDOM FOREST FEATURE IMPORTANCE
# ============================================================

import matplotlib.pyplot as plt

# Get feature names after preprocessing
feature_names = random_forest_model.named_steps[
    "preprocessor"
].get_feature_names_out()

# Extract feature importance scores
importance_values = random_forest_model.named_steps[
    "classifier"
].feature_importances_

# Create feature importance DataFrame
importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importance_values
})

# Sort by importance
importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

# Save complete feature importance report
importance_df.to_csv(
    REPORTS_DIR / "random_forest_feature_importance.csv",
    index=False
)

# Select top 20 features
top_features = importance_df.head(20).sort_values(
    by="Importance",
    ascending=True
)

# Create visualization
plt.figure(figsize=(10, 8))

plt.barh(
    top_features["Feature"],
    top_features["Importance"]
)

plt.title("Top 20 Factors Influencing Customer Churn")
plt.xlabel("Feature Importance")
plt.ylabel("Customer Features")
plt.tight_layout()

plt.savefig(
    REPORTS_DIR / "random_forest_feature_importance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\n" + "=" * 60)
print("TOP 20 CUSTOMER CHURN FACTORS")
print("=" * 60)

print(importance_df.head(20).to_string(index=False))

print("\nFEATURE IMPORTANCE REPORT SAVED SUCCESSFULLY")


# ============================================================
# STEP 9: CUSTOMER-LEVEL CHURN PREDICTIONS
# ============================================================

# Use the trained Random Forest model
customer_probabilities = random_forest_model.predict_proba(X)

# Extract probability of churn (class 1)
churn_probabilities = customer_probabilities[:, 1]

# Create prediction report
customer_predictions = pd.DataFrame({
    "customer_id": pd.read_csv(DATA_PATH)["customer_id"],
    "actual_churn": y.map({0: "No", 1: "Yes"}).values,
    "churn_probability": churn_probabilities
})

# Classify customer risk
def assign_risk(probability):
    if probability >= 0.70:
        return "High"
    elif probability >= 0.40:
        return "Medium"
    else:
        return "Low"

customer_predictions["risk_category"] = (
    customer_predictions["churn_probability"].apply(assign_risk)
)

customer_predictions["predicted_churn"] = (
    customer_predictions["churn_probability"]
    .apply(lambda x: "Yes" if x >= 0.50 else "No")
)

# Round probabilities
customer_predictions["churn_probability"] = (
    customer_predictions["churn_probability"].round(4)
)

# Save report
PREDICTIONS_PATH = BASE_DIR / "reports" / "customer_churn_predictions.csv"

customer_predictions.to_csv(
    PREDICTIONS_PATH,
    index=False
)

print("\n" + "=" * 60)
print("CUSTOMER-LEVEL CHURN PREDICTIONS")
print("=" * 60)

print("\nRISK CATEGORY DISTRIBUTION:")
print(customer_predictions["risk_category"].value_counts())

print("\nPREDICTED CHURN DISTRIBUTION:")
print(customer_predictions["predicted_churn"].value_counts())

print("\nSAMPLE CUSTOMER PREDICTIONS:")
print(customer_predictions.head(10).to_string(index=False))

print("\nCUSTOMER PREDICTION REPORT SAVED SUCCESSFULLY")
print(PREDICTIONS_PATH)
