import os
import joblib
import json
import numpy as np
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import io

app = FastAPI(title="House Price Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CURRENT_DIR = os.path.dirname(__file__) if "__file__" in locals() else "."
LOCATIONS_PATH = os.path.join(CURRENT_DIR, "locations.json")

# Combine the three parts programmatically and read them
model_parts = [
    os.path.join(CURRENT_DIR, "house_price_part1.pkl"),
    os.path.join(CURRENT_DIR, "house_price_part2.pkl"),
    os.path.join(CURRENT_DIR, "house_price_part3.pkl")
]
model_bytearray = bytearray()
for part in model_parts:
    with open(part, 'rb') as f:
        model_bytearray.extend(f.read())

# Load the model directly using joblib
model = joblib.load(io.BytesIO(model_bytearray))

try:
    with open(LOCATIONS_PATH, "r") as f:
        allowed_locations = json.load(f)
except Exception:
    allowed_locations = []

class PredictionInput(BaseModel):
    carpet_area_sqft: float
    floor_num: int
    bathroom: int
    balcony: int
    location_grouped: str
    Furnishing: str
    Transaction: str
    Ownership: str
    facing: str

@app.get("/")
def read_root():
    return {"message": "House Price Prediction API is running"}

@app.get("/locations")
def get_locations():
    return {"locations": allowed_locations}

@app.post("/predict")
def predict_price(payload: PredictionInput):
    input_data = pd.DataFrame([{
        "carpet_area_sqft": payload.carpet_area_sqft,
        "floor_num": payload.floor_num,
        "bathroom": payload.bathroom,
        "balcony": payload.balcony,
        "location_grouped": payload.location_grouped,
        "Furnishing": payload.Furnishing,
        "Transaction": payload.Transaction,
        "Ownership": payload.Ownership,
        "facing": payload.facing
    }])

    log_pred = model.predict(input_data)[0]
    final_price = float(np.expm1(log_pred))

    return {"predicted_price": round(final_price, 2)}
