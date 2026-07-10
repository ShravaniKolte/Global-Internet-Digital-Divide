"""
Global Internet Access & Digital Divide Tracker
Week 4: FastAPI serving layer

Run locally with:
    uvicorn app:app --reload

Then open http://127.0.0.1:8000/docs to test interactively.
"""

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(title="Digital Divide Risk Predictor")

# Load the trained model once at startup (not per-request — that would be slow)
model = joblib.load("digital_divide_model.pkl")

FEATURES = ['mobile_subs_per_100', 'gdp_per_capita_usd', 'urban_pop_pct',
            'electricity_access_pct', 'literacy_rate_pct']


class CountryFeatures(BaseModel):
    mobile_subs_per_100: float
    gdp_per_capita_usd: float
    urban_pop_pct: float
    electricity_access_pct: float
    literacy_rate_pct: float


@app.get("/")
def root():
    return {"message": "Digital Divide Risk Predictor is running. Go to /docs to test it."}


@app.post("/predict")
def predict(features: CountryFeatures):
    input_df = pd.DataFrame([features.dict()], columns=FEATURES)

    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]
    classes = model.classes_

    prob_dict = {cls: round(float(prob), 3) for cls, prob in zip(classes, probabilities)}

    return {
        "predicted_risk": prediction,
        "class_probabilities": prob_dict
    }


@app.get("/health")
def health():
    return {"status": "ok"}
