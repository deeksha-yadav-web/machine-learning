import random
from pathlib import Path

import pandas as pd

random.seed(42)

# Dataset folder ka path
BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "dataset"
DATASET_DIR.mkdir(parents=True, exist_ok=True)

DATA_PATH = DATASET_DIR / "loan_approval_dataset.csv"

rows = []

# Sample dataset generate karna
for i in range(1000):

    dependents = random.randint(0, 5)
    education = random.choice(["Graduate", "Not Graduate"])
    self_employed = random.choice(["Yes", "No"])

    income = random.randint(200000, 2000000)
    loan_amount = random.randint(100000, 1500000)
    loan_term = random.choice([5, 10, 15, 20])

    credit_score = random.randint(300, 900)

    residential_assets = random.randint(0, 2000000)
    commercial_assets = random.randint(0, 1500000)
    luxury_assets = random.randint(0, 1000000)
    bank_assets = random.randint(0, 1000000)

    # Demonstration ke liye synthetic approval rule
    approved = (
        credit_score >= 650
        and income >= loan_amount * 0.35
    )

    loan_status = "Approved" if approved else "Rejected"

    rows.append({
        "loan_id": i + 1,
        "no_of_dependents": dependents,
        "education": education,
        "self_employed": self_employed,
        "income_annum": income,
        "loan_amount": loan_amount,
        "loan_term": loan_term,
        "cibil_score": credit_score,
        "residential_assets_value": residential_assets,
        "commercial_assets_value": commercial_assets,
        "luxury_assets_value": luxury_assets,
        "bank_asset_value": bank_assets,
        "loan_status": loan_status
    })

df = pd.DataFrame(rows)

df.to_csv(DATA_PATH, index=False)

print("Sample dataset successfully created!")
print("File location:", DATA_PATH)
print("Total records:", len(df))
print("\nFirst five rows:")
print(df.head())

print("\nLoan status distribution:")
print(df["loan_status"].value_counts())