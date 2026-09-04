"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Fleet Telemetry API Router: Live GPS Tracking & Cargo Manifest Endpoints
"""
from fastapi import APIRouter
from typing import List, Dict, Any
from app.services.fleet_tracker import fleet_manager

router = APIRouter(prefix="/fleet", tags=["Fleet Tracking"])

@router.get("/live")
def get_live_fleet() -> List[Dict[str, Any]]:
    """Returns real-time GPS locations, speed, cargo manifest and status of all freight vehicles"""
    fleet_manager.tick_telemetry()
    return fleet_manager.get_fleet()
