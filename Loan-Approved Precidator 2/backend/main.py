# from pathlib import Path

# import joblib
# import pandas as pd

# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel


# # --------------------------------------------------
# # 1. Initialize FastAPI
# # --------------------------------------------------

# app = FastAPI(
#     title="Loan Approval Predictor API",
#     description="Machine Learning based loan approval prediction",
#     version="1.0.0",
# )


# # --------------------------------------------------
# # 2. Allow React frontend to connect
# # --------------------------------------------------

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:5173",
#         "http://127.0.0.1:5173",
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # --------------------------------------------------
# # 3. Model file path
# # --------------------------------------------------

# BASE_DIR = Path(__file__).resolve().parent
# MODEL_PATH = BASE_DIR / "models" / "loan_model.joblib"


# # --------------------------------------------------
# # 4. Define applicant input
# # --------------------------------------------------

# class Applicant(BaseModel):
#     no_of_dependents: int
#     education: str
#     self_employed: str
#     income_annum: float
#     loan_amount: float
#     loan_term: int
#     cibil_score: float
#     residential_assets_value: float
#     commercial_assets_value: float
#     luxury_assets_value: float
#     bank_asset_value: float


# # --------------------------------------------------
# # 5. Home route
# # --------------------------------------------------

# @app.get("/")
# def home():
#     return {
#         "message": "Loan Approval Predictor API is running"
#     }


# # --------------------------------------------------
# # 6. Health check route
# # --------------------------------------------------

# @app.get("/health")
# def health_check():
#     return {
#         "status": "healthy",
#         "model_exists": MODEL_PATH.exists(),
#     }


# # --------------------------------------------------
# # 7. Predict loan approval
# # --------------------------------------------------

# @app.post("/predict")
# def predict_loan(applicant: Applicant):

#     # Check whether model training has been completed
#     if not MODEL_PATH.exists():
#         raise HTTPException(
#             status_code=503,
#             detail=(
#                 "Trained model not found. "
#                 "Please run train_model.py first."
#             ),
#         )

#     try:
#         # Load trained model
#         artifact = joblib.load(MODEL_PATH)

#         model = artifact["model"]
#         feature_names = artifact["feature_names"]

#         # Convert applicant details into a DataFrame
#         applicant_data = applicant.model_dump()

#         input_df = pd.DataFrame([applicant_data])

#         # Ensure input columns match training columns
#         missing_features = [
#             feature
#             for feature in feature_names
#             if feature not in input_df.columns
#         ]

#         extra_features = [
#             feature
#             for feature in input_df.columns
#             if feature not in feature_names
#         ]

#         if missing_features or extra_features:
#             raise HTTPException(
#                 status_code=422,
#                 detail={
#                     "message": (
#                         "Input features do not match "
#                         "the trained model."
#                     ),
#                     "missing_features": missing_features,
#                     "extra_features": extra_features,
#                 },
#             )

#         input_df = input_df[feature_names]

#         # Predict loan status
#         prediction = int(model.predict(input_df)[0])

#         # Get probability if supported
#         approval_probability = None

#         if hasattr(model, "predict_proba"):
#             probabilities = model.predict_proba(input_df)[0]

#             classes = list(model.named_steps["classifier"].classes_)

#             if 1 in classes:
#                 approval_probability = float(
#                     probabilities[classes.index(1)] * 100
#                 )

#         # Convert prediction into readable text
#         status = "Approved" if prediction == 1 else "Rejected"

#         return {
#             "success": True,
#             "prediction": prediction,
#             "loan_status": status,
#             "approval_probability": (
#                 round(approval_probability, 2)
#                 if approval_probability is not None
#                 else None
#             ),
#             "model_used": artifact["model_name"],
#             "message": (
#                 "The model predicts loan approval."
#                 if prediction == 1
#                 else "The model predicts loan rejection."
#             ),
#             "note": (
#                 "This is a machine learning prediction, "
#                 "not an official bank decision."
#             ),
#         }

#     except HTTPException:
#         raise

#     except Exception as error:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Prediction failed: {str(error)}",
#         )



















































from pathlib import Path

import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# ==========================================
# 1. CREATE FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="Loan Approval Predictor",
    description="Loan approval prediction using Machine Learning",
    version="1.0.0"
)


# ==========================================
# 2. CORS CONFIGURATION
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# 3. MODEL FILE PATH
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "loan_model.joblib"


# ==========================================
# 4. APPLICANT INPUT FIELDS
# ==========================================

class Applicant(BaseModel):

    no_of_dependents: int = Field(ge=0, le=20)

    education: str = Field(
        pattern=r"^(Graduate|Not Graduate)$"
    )

    self_employed: str = Field(
        pattern=r"^(Yes|No)$"
    )

    income_annum: float = Field(ge=0)

    loan_amount: float = Field(gt=0)

    loan_term: int = Field(gt=0, le=50)

    cibil_score: float = Field(ge=0, le=1000)

    residential_assets_value: float = Field(ge=0)

    commercial_assets_value: float = Field(ge=0)

    luxury_assets_value: float = Field(ge=0)

    bank_asset_value: float = Field(ge=0)


# ==========================================
# 5. HOME ROUTE
# ==========================================

@app.get("/")
def home():

    return {
        "success": True,
        "message": "Loan Approval Predictor API is running!"
    }


# ==========================================
# 6. HEALTH CHECK ROUTE
# ==========================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "model_exists": MODEL_PATH.exists()
    }


# ==========================================
# 7. LOAN PREDICTION ROUTE
# ==========================================

@app.post("/predict")
def predict_loan(applicant: Applicant):

    # Check whether the model exists
    if not MODEL_PATH.exists():

        raise HTTPException(
            status_code=503,
            detail=(
                "Trained model not found. "
                "Please run train_model.py first."
            )
        )

    try:

        # Load the trained model
        artifact = joblib.load(MODEL_PATH)

        model = artifact["model"]

        feature_names = artifact["feature_names"]

        # Convert applicant details into a DataFrame
        applicant_data = applicant.model_dump()

        input_df = pd.DataFrame([applicant_data])

        # Check whether required features are available
        missing_features = [
            feature
            for feature in feature_names
            if feature not in input_df.columns
        ]

        if missing_features:

            raise HTTPException(
                status_code=422,
                detail={
                    "message": "Input fields do not match the model.",
                    "missing_features": missing_features
                }
            )

        # Keep the same feature order used during training
        input_df = input_df[feature_names]

        # Predict loan status
        prediction = int(model.predict(input_df)[0])

        # Calculate approval probability if supported
        approval_probability = None

        if hasattr(model, "predict_proba"):

            probabilities = model.predict_proba(input_df)[0]

            classifier = model.named_steps["classifier"]

            classes = list(classifier.classes_)

            if 1 in classes:

                approval_probability = float(
                    probabilities[classes.index(1)] * 100
                )

        # Convert numeric prediction into readable status
        target_mapping = artifact.get("target_mapping", {})

        reverse_mapping = {
            value: key
            for key, value in target_mapping.items()
        }

        loan_status = reverse_mapping.get(prediction)

        if loan_status is None:

            loan_status = (
                "Approved"
                if prediction == 1
                else "Rejected"
            )

        loan_status = str(loan_status).strip().title()

        # Return the prediction to the frontend
        return {
            "success": True,
            "prediction": prediction,
            "loan_status": loan_status,
            "approval_probability": (
                round(approval_probability, 2)
                if approval_probability is not None
                else None
            ),
            "model_used": artifact.get(
                "model_name",
                "Machine Learning Model"
            ),
            "message": f"Model prediction: {loan_status}",
            "note": (
                "This is a machine learning prediction, "
                "not an official bank decision."
            )
        }

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}"
        )
