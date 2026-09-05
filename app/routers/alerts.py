"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Multilingual Alerts API Router: Role-Scoped Emergency Broadcast Bulletins
"""
from fastapi import APIRouter, Query
from typing import List, Dict, Any, Optional
from app.services.fleet_tracker import fleet_manager
from app.services.digital_twin_data import NER_DISTRICT_NODES

router = APIRouter(prefix="/alerts", tags=["Emergency Alerts"])

@router.get("/active")
def get_active_alerts() -> List[Dict[str, Any]]:
    """Returns all active multilingual emergency alerts (English, Assamese, Hindi, Bengali)"""
    return fleet_manager.get_alerts()

@router.get("/scoped")
def get_scoped_alerts(
    role: str = Query("admin", description="Active persona: admin, user, gov_employee"),
    district_id: Optional[str] = Query(None, description="Assigned district ID for govt employee")
) -> List[Dict[str, Any]]:
    """
    Returns role-filtered alerts:
    - Admin: Full regional view across all 8 NER states
    - Citizen / User: Locality / route-relevant hazard alerts
    - Government Employee: Assigned district-specific emergency bulletins
    """
    all_alerts = fleet_manager.get_alerts()
    if role == "admin":
        return all_alerts

    if role == "gov_employee" and district_id:
        node = next((n for n in NER_DISTRICT_NODES if n["id"] == district_id), None)
        d_name = node["name"].split(" (")[0].lower() if node else district_id.lower()
        district_alerts = [
            a for a in all_alerts
            if any(d_name in d.lower() for d in a.get("affected_districts", [])) or d_name in a.get("location_tag", "").lower()
        ]
        return district_alerts if district_alerts else all_alerts[:2]

    # For citizen / user: local / high-priority transit warnings
    user_alerts = [
        a for a in all_alerts
        if a.get("severity") in ("CRITICAL_DANGER", "WARNING")
    ]
    return user_alerts if user_alerts else all_alerts[:3]
