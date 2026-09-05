"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Government Employee District Command API Router
Module 5 & 6: District-Scoped Monitoring, Incident Verification & High-Trust Reporting
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from app.services.fleet_tracker import fleet_manager
from app.services.role_manager import role_manager
from app.services.digital_twin_data import NER_DISTRICT_NODES, NER_ROAD_EDGES
from app.models.schemas import FieldReportCreate, FieldReportRecord, FieldReportVerifyRequest

router = APIRouter(prefix="/district", tags=["Government Employee District Command"])

class DistrictVerifyAction(BaseModel):
    report_id: str
    action: str # "CONFIRM" or "REJECT"
    officer_name: str
    department: str
    notes: Optional[str] = None

@router.get("/dashboard/{district_id}")
def get_district_employee_dashboard(district_id: str) -> Dict[str, Any]:
    """
    Returns district-specific metrics, pending reports queue, active incidents,
    and road blockage data for the assigned Government Employee.
    """
    node = next((n for n in NER_DISTRICT_NODES if n["id"] == district_id), None)
    if not node:
        node = NER_DISTRICT_NODES[0]

    d_name = node["name"].split(" (")[0].lower()
    
    all_reports = fleet_manager.get_field_reports()
    district_reports = [
        r for r in all_reports
        if d_name in r.get("location_name", "").lower() or district_id in r.get("location_name", "").lower() or d_name in r.get("nearest_highway", "").lower()
    ]
    if not district_reports:
        district_reports = all_reports[:4] # Fallback display

    pending_queue = [r for r in district_reports if r.get("verification_status") == "PENDING_VERIFICATION"]
    verified_incidents = [r for r in district_reports if r.get("verification_status") in ("ACTIVE_INCIDENT", "PWD_CONFIRMED", "VERIFIED_AI")]

    blocked_roads = [
        e for e in fleet_manager.edges_state
        if (e["source"] == district_id or e["target"] == district_id) and e.get("status") in ("blocked", "warning")
    ]

    all_alerts = fleet_manager.get_alerts()
    district_alerts = [
        a for a in all_alerts
        if any(d_name in d.lower() for d in a.get("affected_districts", [])) or d_name in a.get("location_tag", "").lower()
    ]

    officer_profile = role_manager.district_profiles.get(district_id, {
        "officer_name": f"Officer {node['name'].split(' (')[0]}",
        "department": f"{node['state']} SDMA District Cell",
        "trust_score": 92.0
    })

    return {
        "district_id": node["id"],
        "district_name": node["name"],
        "state": node["state"],
        "assigned_officer": officer_profile.get("officer_name", "District Disaster Officer"),
        "department": officer_profile.get("department", "PWD / SDMA"),
        "trust_score": officer_profile.get("trust_score", 92.0),
        "status": node.get("status", "connected"),
        "population": node.get("population", 0),
        "hospital_stock_runway": {
            "oxygen_days": node.get("stock_oxygen_days", 8.0),
            "rations_days": node.get("stock_rations_days", 25.0),
            "medicines_days": node.get("stock_medicines_days", 16.0)
        },
        "metrics": {
            "active_incidents": len(verified_incidents) + (2 if node.get("status") != "connected" else 1),
            "pending_reports": len(pending_queue),
            "critical_hazards": len([r for r in district_reports if r.get("severity") in ("HIGH", "BLOCKING")]),
            "road_blockages": len(blocked_roads),
            "floods": len([r for r in district_reports if "flood" in r.get("incident_type", "").lower()]),
            "landslides": len([r for r in district_reports if "landslide" in r.get("incident_type", "").lower()])
        },
        "pending_verification_queue": pending_queue,
        "verified_incidents": verified_incidents,
        "district_alerts": district_alerts
    }

@router.post("/verify")
def verify_district_report(req: DistrictVerifyAction) -> Dict[str, Any]:
    """
    Government Employee verification action: Confirm or Reject a field report.
    Instantly triggers closed loop into Digital Twin road state and Alert System.
    """
    verify_req = FieldReportVerifyRequest(
        action=req.action,
        verifier_name=req.officer_name,
        verifier_department=req.department,
        notes=req.notes
    )
    result = fleet_manager.verify_field_report(req.report_id, verify_req)
    if not result:
        raise HTTPException(status_code=404, detail="Field report not found")
    return {
        "status": "success",
        "action": req.action,
        "report": result
    }

@router.post("/official-report", response_model=FieldReportRecord)
def submit_official_employee_report(report: FieldReportCreate):
    """
    Submits a high-confidence official report from a Government Employee (90-95% trust level).
    """
    report.reporter_role = "gov_employee"
    report.confidence_score = 92.0
    return fleet_manager.add_field_report(report)
