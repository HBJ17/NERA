"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Field Incident Reporting API Router: Crowdsourced & Official Hazard Ingestion
"""
from fastapi import APIRouter
from typing import List, Dict, Any
from app.models.schemas import FieldReportCreate, FieldReportRecord
from app.services.fleet_tracker import fleet_manager

router = APIRouter(prefix="/reports", tags=["Field Reporting"])

@router.get("/all")
def get_all_reports() -> List[Dict[str, Any]]:
    """Returns submitted PWD / NDRF and driver hazard reports"""
    return fleet_manager.get_field_reports()

@router.post("/submit", response_model=FieldReportRecord)
def submit_field_report(report: FieldReportCreate):
    """
    Submits an on-ground disaster/blockage report with GPS and photo,
    and dynamically propagates hazard into the Digital Twin network.
    """
    return fleet_manager.add_field_report(report)
