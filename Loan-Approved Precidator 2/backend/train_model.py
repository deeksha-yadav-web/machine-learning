import json
from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "dataset"
MODEL_DIR = Path(__file__).resolve().parent / "models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "loan_model.joblib"


# --------------------------------------------------
# 2. Load dataset
# --------------------------------------------------

csv_files = list(DATASET_DIR.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError(
        "Dataset folder mein CSV file nahi mili. "
        "Apni loan approval CSV file dataset folder mein rakho."
    )

# Agar folder mein ek se zyada CSV files hain,
# toh pehli file select hogi.
DATA_PATH = csv_files[0]

print("\nDataset file:", DATA_PATH.name)

df = pd.read_csv(DATA_PATH)

# Column names ko clean karo
df.columns = (
    df.columns.astype(str)
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
)

print("\nDataset shape:", df.shape)

print("\nFirst five rows:")
print(df.head())

print("\nColumn names:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())


# --------------------------------------------------
# 3. Check target column
# --------------------------------------------------

TARGET_COLUMN = "loan_status"

if TARGET_COLUMN not in df.columns:
    raise ValueError(
        f"'{TARGET_COLUMN}' column dataset mein nahi mili.\n"
        f"Available columns: {df.columns.tolist()}\n"
        "Apne actual target column ke according "
        "TARGET_COLUMN ki value change karo."
    )

# Empty target values wali rows remove karo
df = df.dropna(subset=[TARGET_COLUMN]).copy()

# Target labels ko clean karo
df[TARGET_COLUMN] = (
    df[TARGET_COLUMN]
    .astype(str)
    .str.strip()
    .str.lower()
)

print("\nTarget values:")
print(df[TARGET_COLUMN].value_counts())


# --------------------------------------------------
# 4. Convert target labels into numbers
# --------------------------------------------------

# Is mapping ko apne dataset ke actual labels se match karo.
target_mapping = {
    "approved": 1,
    "rejected": 0,
}

actual_labels = set(df[TARGET_COLUMN].unique())

if not actual_labels.issubset(set(target_mapping.keys())):
    raise ValueError(
        "Dataset ke target labels expected labels se different hain.\n"
        f"Actual labels: {sorted(actual_labels)}\n"
        "Code mein target_mapping ko actual labels ke according update karo."
    )

df[TARGET_COLUMN] = df[TARGET_COLUMN].map(target_mapping)

if df[TARGET_COLUMN].nunique() != 2:
    raise ValueError(
        "Loan approval model ke liye dataset mein "
        "approved aur rejected dono classes honi chahiye."
    )


# --------------------------------------------------
# 5. Separate features and target
# --------------------------------------------------

# Target column ke alawa baaki columns features hain.
# Loan ID ko feature nahi banayenge.
columns_to_drop = [TARGET_COLUMN]

if "loan_id" in df.columns:
    columns_to_drop.append("loan_id")

X = df.drop(columns=columns_to_drop)
y = df[TARGET_COLUMN].astype(int)

if X.shape[1] == 0:
    raise ValueError("Dataset mein koi input feature nahi mila.")

# Completely empty columns ko remove karo
empty_columns = X.columns[X.isnull().all()].tolist()

if empty_columns:
    print("\nRemoving completely empty columns:", empty_columns)
    X = X.drop(columns=empty_columns)

if X.shape[1] == 0:
    raise ValueError("Cleaning ke baad koi usable feature nahi bacha.")

print("\nFeatures used for training:")
print(X.columns.tolist())


# --------------------------------------------------
# 6. Split data into training and testing sets
# --------------------------------------------------

# 80% training aur 20% testing
class_counts = y.value_counts()

if len(class_counts) != 2 or class_counts.min() < 2:
    raise ValueError(
        "Train-test split ke liye har target class mein "
        "kam se kam 2 rows honi chahiye."
    )

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

print("\nTraining rows:", len(X_train))
print("Testing rows:", len(X_test))


# --------------------------------------------------
# 7. Identify numeric and categorical columns
# --------------------------------------------------

numeric_features = X.select_dtypes(
    include=["number"]
).columns.tolist()

categorical_features = X.select_dtypes(
    exclude=["number"]
).columns.tolist()

print("\nNumeric features:", numeric_features)
print("Categorical features:", categorical_features)


# --------------------------------------------------
# 8. Prepare data preprocessing
# --------------------------------------------------

numeric_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]
)

categorical_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        (
            "encoder",
            OneHotEncoder(handle_unknown="ignore"),
        ),
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("numeric", numeric_pipeline, numeric_features),
        ("categorical", categorical_pipeline, categorical_features),
    ],
    remainder="drop",
)


# --------------------------------------------------
# 9. Create machine learning models
# --------------------------------------------------

models = {
    "Logistic Regression": LogisticRegression(
        max_iter=2000,
        random_state=42,
    ),

    "Decision Tree": DecisionTreeClassifier(
        max_depth=8,
        random_state=42,
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1,
    ),
}


# --------------------------------------------------
# 10. Train and compare models
# --------------------------------------------------

results = []
trained_models = {}

for model_name, classifier in models.items():

    print(f"\nTraining {model_name}...")

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier),
        ]
    )

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(
        y_test, predictions, zero_division=0
    )
    recall = recall_score(
        y_test, predictions, zero_division=0
    )
    f1 = f1_score(
        y_test, predictions, zero_division=0
    )

    results.append({
        "model": model_name,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
    })

    trained_models[model_name] = pipeline

    print("Accuracy :", round(accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall   :", round(recall, 4))
    print("F1-score :", round(f1, 4))

    print("\nClassification report:")
    print(
        classification_report(
            y_test,
            predictions,
            labels=[0, 1],
            target_names=["Rejected", "Approved"],
            zero_division=0,
        )
    )


# --------------------------------------------------
# 11. Compare results and select the best model
# --------------------------------------------------

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="f1_score",
    ascending=False,
)

print("\nModel comparison:")
print(results_df.to_string(index=False))

best_model_name = results_df.iloc[0]["model"]
best_model = trained_models[best_model_name]

print("\nBest model:", best_model_name)


# --------------------------------------------------
# 12. Save trained model
# --------------------------------------------------

artifact = {
    "model": best_model,
    "model_name": best_model_name,
    "feature_names": X.columns.tolist(),
    "numeric_features": numeric_features,
    "categorical_features": categorical_features,
    "target_column": TARGET_COLUMN,
    "target_mapping": target_mapping,
    "metrics": results_df.to_dict(orient="records"),
}

joblib.dump(artifact, MODEL_PATH)

print("\nModel successfully saved at:")
print(MODEL_PATH)


# --------------------------------------------------
# 13. Verify saved model
# --------------------------------------------------

saved_artifact = joblib.load(MODEL_PATH)

print("\nSaved model verification:")
print("Model name:", saved_artifact["model_name"])
print("Features:", saved_artifact["feature_names"])
print("\nTraining process completed!")