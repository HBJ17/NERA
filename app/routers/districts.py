"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
District Management API Router
"""
from fastapi import APIRouter
from typing import Dict, Any, List
from app.services.district_manager import district_manager

router = APIRouter(prefix="/districts", tags=["District Management"])

@router.get("/all")
def get_all_districts() -> List[Dict[str, Any]]:
    """Returns all 32 strategic district nodes across all 8 North Eastern states"""
    return district_manager.get_all_districts()

@router.get("/state/{state_name}")
def get_districts_in_state(state_name: str) -> List[Dict[str, Any]]:
    """Returns districts filtered by North East state (Assam, Meghalaya, Nagaland, Manipur, etc.)"""
    return district_manager.get_districts_by_state(state_name)

@router.get("/summary-stats")
def get_districts_summary() -> Dict[str, Any]:
    """Returns aggregated population, hospital capacity, and stock runway across all NER states"""
    return district_manager.get_district_statistics()
