"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Roles API Router: 1-Click Multi-Stakeholder Role & District Management Endpoints
"""
from fastapi import APIRouter
from typing import Dict, Any, Optional
from pydantic import BaseModel
from app.services.role_manager import role_manager
from app.services.fleet_tracker import fleet_manager
from app.services.digital_twin_data import NER_DISTRICT_NODES, NER_ROAD_EDGES

router = APIRouter(prefix="/roles", tags=["Role & Persona Management"])

class RoleSwitchRequest(BaseModel):
    role: str
    district_id: Optional[str] = None

@router.get("/list")
def get_roles_list() -> Dict[str, Any]:
    """Returns available roles, district profiles, and current active role state"""
    return role_manager.get_available_roles()

@router.get("/current")
def get_current_role() -> Dict[str, Any]:
    """Returns current active role, district ID, and officer profile"""
    return role_manager.get_current_profile()

@router.post("/switch")
def switch_active_role(req: RoleSwitchRequest) -> Dict[str, Any]:
    """Switches active role and district profile instantaneously without auth friction"""
    return role_manager.switch_role(role=req.role, district_id=req.district_id)

@router.get("/district-summary/{district_id}")
def get_district_summary(district_id: str) -> Dict[str, Any]:
    """Returns real-time district status, incident counts, and infrastructure runway"""
    node = next((n for n in NER_DISTRICT_NODES if n["id"] == district_id), None)
    if not node:
        node = NER_DISTRICT_NODES[0]

    # Calculate live reports in this district
    all_reports = fleet_manager.get_field_reports()
    d_name = node["name"].split(" (")[0].lower()
    
    district_reports = [
        r for r in all_reports 
        if d_name in r.get("location_name", "").lower() or district_id in r.get("location_name", "").lower()
    ]
    
    pending_reports = [r for r in district_reports if r.get("verification_status") == "PENDING_VERIFICATION"]
    verified_reports = [r for r in district_reports if r.get("verification_status") != "PENDING_VERIFICATION"]
    
    # Calculate road blockages touching this district
    blocked_highways = [
        e for e in fleet_manager.edges_state
        if (e["source"] == district_id or e["target"] == district_id) and e.get("status") in ("blocked", "warning")
    ]

    # Calculate active alerts for this district
    all_alerts = fleet_manager.get_alerts()
    district_alerts = [
        a for a in all_alerts
        if any(d_name in d.lower() for d in a.get("affected_districts", [])) or d_name in a.get("location_tag", "").lower()
    ]

    profile = role_manager.district_profiles.get(district_id, {})

    return {
        "district_id": node["id"],
        "district_name": node["name"],
        "state": node["state"],
        "status": node.get("status", "connected"),
        "population": node.get("population", 0),
        "hospitals": node.get("hospitals", 1),
        "stock_oxygen_days": node.get("stock_oxygen_days", 10.0),
        "stock_rations_days": node.get("stock_rations_days", 20.0),
        "stock_medicines_days": node.get("stock_medicines_days", 15.0),
        "officer": profile.get("officer_name", "District Incident Commander"),
        "department": profile.get("department", "District Disaster Management Authority"),
        "trust_score": profile.get("trust_score", 90.0),
        "metrics": {
            "active_incidents": len(verified_reports) + (1 if node.get("status") != "connected" else 0),
            "pending_reports": len(pending_reports),
            "critical_hazards": len([r for r in district_reports if r.get("severity") in ("HIGH", "BLOCKING")]),
            "road_blockages": len(blocked_highways),
            "floods": len([r for r in district_reports if "flood" in r.get("incident_type", "").lower()]),
            "landslides": len([r for r in district_reports if "landslide" in r.get("incident_type", "").lower()]),
            "active_alerts_count": len(district_alerts)
        },
        "recent_reports": district_reports[:5],
        "active_alerts": district_alerts[:3]
    }
