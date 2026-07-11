"""
Basic tests for the Digital Divide Risk Predictor.
Run with: pytest tests/ -v
"""

import joblib
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

FEATURES = ['mobile_subs_per_100', 'gdp_per_capita_usd', 'urban_pop_pct',
            'electricity_access_pct', 'literacy_rate_pct']


def test_model_file_exists():
    """The trained model file should exist before deployment."""
    assert os.path.exists("digital_divide_model.pkl"), "Model file not found"


def test_model_loads():
    """The saved model should load without errors."""
    model = joblib.load("digital_divide_model.pkl")
    assert model is not None


def test_model_predicts_valid_class():
    """The model should only ever output one of the three known risk tiers."""
    model = joblib.load("digital_divide_model.pkl")

    sample = pd.DataFrame([{
        "mobile_subs_per_100": 82,
        "gdp_per_capita_usd": 2600,
        "urban_pop_pct": 36,
        "electricity_access_pct": 99,
        "literacy_rate_pct": 76,
    }], columns=FEATURES)

    prediction = model.predict(sample)[0]
    assert prediction in ["Low Risk", "Medium Risk", "High Risk"]


def test_high_income_predicts_low_risk():
    """Sanity check: a high-income, highly urban, high-literacy profile
    should never be classified as High Risk."""
    model = joblib.load("digital_divide_model.pkl")

    sample = pd.DataFrame([{
        "mobile_subs_per_100": 120,
        "gdp_per_capita_usd": 60000,
        "urban_pop_pct": 90,
        "electricity_access_pct": 100,
        "literacy_rate_pct": 99,
    }], columns=FEATURES)

    prediction = model.predict(sample)[0]
    assert prediction != "High Risk"
