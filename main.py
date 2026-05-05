from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model & scaler
model = joblib.load("model.joblib")
scaler = joblib.load("scaler.joblib")

# Input schema
class InputData(BaseModel):
    SPX: float
    USO: float
    SLV: float
    EUR_USD: float

@app.get("/")
def home():
    return {"message": "Gold Price Prediction API"}

@app.post("/predict")
def predict(data: InputData):
    features = np.array([[data.SPX, data.USO, data.SLV, data.EUR_USD]])
    scaled = scaler.transform(features)
    prediction = model.predict(scaled)

    return {"predicted_gold_price": float(prediction[0])}