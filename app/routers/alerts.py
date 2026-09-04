"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Multilingual Alerts API Router: Regional Emergency Broadcast Bulletins
"""
from fastapi import APIRouter
from typing import List, Dict, Any
from app.services.fleet_tracker import fleet_manager

router = APIRouter(prefix="/alerts", tags=["Emergency Alerts"])

@router.get("/active")
def get_active_alerts() -> List[Dict[str, Any]]:
    """Returns multilingual emergency alerts (English, Assamese, Hindi, Bengali)"""
    return fleet_manager.get_alerts()
