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

    user_alerts = [
        a for a in all_alerts
        if a.get("severity") in ("CRITICAL_DANGER", "WARNING")
    ]
    return user_alerts if user_alerts else all_alerts[:3]

@router.get("/hotlines")
def get_emergency_hotlines() -> Dict[str, Any]:
    """
    Returns official 8-state Disaster Management Authority (SDMA), NDRF, BRO,
    and Highway Police emergency control room hotlines for 1-click dispatch.
    """
    return {
        "status": "success",
        "national_emergency_number": "112",
        "highway_toll_free": "1033 (NHIDCL Emergency Road Assistance)",
        "ndrf_headquarters": {
            "unit": "NDRF 1st Battalion (Patgaon, Guwahati)",
            "phone": "+91-361-2840284",
            "mobile": "+91-94350-11234",
            "coverage": "Assam, Meghalaya, Mizoram, Tripura"
        },
        "bro_projects": [
            {"name": "BRO Project Vartak", "base": "Tezpur (Assam)", "phone": "+91-3712-259123", "sector": "Western Arunachal & NH-13 Sela Pass"},
            {"name": "BRO Project Pushpak", "base": "Aizawl (Mizoram)", "phone": "+91-389-2351240", "sector": "Mizoram & Barak Valley NH-06"},
            {"name": "BRO Project Sewak", "base": "Dimapur (Nagaland)", "phone": "+91-3862-248102", "sector": "Nagaland & Manipur NH-29"},
            {"name": "BRO Project Swastik", "base": "Gangtok (Sikkim)", "phone": "+91-3592-202244", "sector": "Sikkim NH-10 Teesta Lifeline"}
        ],
        "state_eoc": [
            {"state": "Assam", "agency": "ASDMA State Control Room", "helpline": "1070 / 1079", "phone": "+91-361-2237221"},
            {"state": "Arunachal Pradesh", "agency": "APSDMA Emergency Cell", "helpline": "1070", "phone": "+91-360-2212200"},
            {"state": "Meghalaya", "agency": "SDMA Shillong", "helpline": "1070", "phone": "+91-364-2502188"},
            {"state": "Nagaland", "agency": "NSDMA Kohima", "helpline": "1070", "phone": "+91-370-2291122"},
            {"state": "Manipur", "agency": "Manipur Relief & Disaster Cell", "helpline": "1070", "phone": "+91-385-2443441"},
            {"state": "Mizoram", "agency": "DM&R Aizawl", "helpline": "1070", "phone": "+91-389-2335842"},
            {"state": "Tripura", "agency": "TSDMA Agartala", "helpline": "1070", "phone": "+91-381-2416045"},
            {"state": "Sikkim", "agency": "SSDMA Gangtok", "helpline": "1070 / 1077", "phone": "+91-3592-201145"}
        ]
    }

