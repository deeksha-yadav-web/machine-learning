# Loan Approval Predictor

## 1. Project Architecture

React Frontend
      |
      | Applicant details (JSON)
      v
FastAPI Backend
      |
      v
Saved ML Pipeline (Joblib)
      |
      v
Prediction + Estimated Probability
      |
      v
React par Result Display

## 2. Important Files

- dataset/loan_approval_dataset.csv: Original dataset.
- backend/train_model.py: Dataset inspect, preprocess,
  train, evaluate aur save karta hai.
- backend/main.py: FastAPI endpoints aur predictions.
- backend/models/loan_model.joblib: Trained pipeline.
- frontend/src/App.jsx: Applicant form aur result.
- frontend/src/App.css: Frontend styling.
- frontend/src/main.jsx: React application entry point.
- CONNECT.md: Setup aur execution instructions.

## 3. Dataset Setup

Kaggle se dataset download karke CSV file dataset folder mein rakho.
Training code mein DATA_PATH ko actual filename ke according update karo.

## 4. Training

Backend terminal mein virtual environment activate karo:

Windows PowerShell:
.\venv\Scripts\Activate.ps1

Dependencies install karo:

python -m pip install -r requirements.txt

Model train karo:

python train_model.py

Training ke baad backend/models/loan_model.joblib generate hogi.

## 5. Start FastAPI Backend

Backend folder ke andar:

python -m uvicorn main:app --reload

API:
http://127.0.0.1:8000

Health check:
http://127.0.0.1:8000/health

Interactive API documentation:
http://127.0.0.1:8000/docs

## 6. Start React Frontend

VS Code mein doosra terminal kholo.

Project root se:

cd frontend
npm install
npm run dev

Vite terminal mein jo local URL show ho, use browser mein kholo.
Usually URL http://localhost:5173 hota hai.

## 7. Request Flow

React /predict endpoint par applicant details JSON mein bhejta hai.
FastAPI input validate karta hai aur saved ML pipeline se prediction leta hai.
API result JSON mein return karti hai.
React prediction aur estimated probability display karta hai.

## 8. Common Errors

Dataset not found:
CSV ko dataset folder mein rakho aur DATA_PATH check karo.

Model not found:
Pehle backend folder mein python train_model.py run karo.

Module not found:
Virtual environment activate karke
python -m pip install -r requirements.txt run karo.

Connection refused:
Check karo ki FastAPI server port 8000 par running hai.

CORS error:
Frontend ka origin main.py ke allow_origins mein check karo.

422 Validation Error:
Check karo ki frontend ke field names aur types
training dataset ke actual features se match karte hain.

Port already in use:
Terminal mein running server stop karo ya doosra available port use karo.

## 9. Stop Servers

Server wale terminal mein Ctrl+C press karo.

## 10. Retrain Model

Dataset change karne ke baad backend folder mein
python train_model.py run karo.

Purani model file successful retraining par replace ho jayegi.

## 11. Limitations

Ye student demonstration project hai, real bank decision system nahi.
Dataset mein historical bias ho sakta hai.
Model ki probability actual loan approval ki guarantee nahi hai.