"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Prediction API Router: Exposes Landslide Probability & Flood Inundation Models
"""
from fastapi import APIRouter
from app.models.schemas import (
    LandslidePredictionRequest,
    LandslidePredictionResponse,
    FloodPredictionRequest,
    FloodPredictionResponse
)
from app.services.ai_predictor import AIPredictionEngine

router = APIRouter(prefix="/predict", tags=["AI Prediction Engine"])

@router.post("/landslide", response_model=LandslidePredictionResponse)
def predict_landslide_risk(req: LandslidePredictionRequest):
    """
    AI model predicting landslide vulnerability % and factor importance
    based on 24h rainfall, hill slope gradient, soil moisture, and seismic history.
    """
    return AIPredictionEngine.predict_landslide(req)

@router.post("/flood", response_model=FloodPredictionResponse)
def predict_flood_inundation(req: FloodPredictionRequest):
    """
    AI model predicting river basin flood risk and estimated time to submergence.
    """
    return AIPredictionEngine.predict_flood(req)
