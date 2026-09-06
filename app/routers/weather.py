"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Weather & 4-Stream Data Fusion API Router
"""
from fastapi import APIRouter
from typing import Dict, Any, List, Optional
from app.services.weather_engine import weather_engine
from app.services.data_fusion import data_fusion_engine

router = APIRouter(prefix="/weather", tags=["Meteorological & Data Fusion Engine"])

@router.get("/stations")
def get_weather_stations() -> List[Dict[str, Any]]:
    """Returns real-time meteorological observations for all NER regional stations"""
    return weather_engine.get_all_stations()

@router.get("/district/{district_id}")
def get_district_weather(district_id: str) -> Dict[str, Any]:
    """Returns weather telemetry and radar precipitation for a specific district"""
    return weather_engine.get_district_weather(district_id)

@router.get("/radar-overlays")
def get_radar_overlays() -> List[Dict[str, Any]]:
    """Returns Doppler radar precipitation coordinates for Leaflet GIS layer"""
    return weather_engine.get_radar_overlays()

@router.get("/live-status")
def get_live_weather_status() -> Dict[str, Any]:
    """Returns Open-Meteo live synchronization status, timestamps and warning stats"""
    return weather_engine.get_sync_status()

@router.post("/sync-live")
def trigger_live_weather_sync(districts: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Triggers on-demand live meteorological synchronization from Open-Meteo
    for all NER districts. Fallback is gracefully maintained if offline.
    """
    return weather_engine.sync_live_weather(districts)

@router.get("/fusion/composite-risk")
def get_fused_composite_risk() -> Dict[str, Any]:
    """
    Returns 4-Stream Data Fusion composite risk matrix across all North East corridors
    (Merging Weather + Infrastructure + GPS Delays + Crowdsourced Field Reports)
    """
    return data_fusion_engine.compute_composite_risk_matrix()


