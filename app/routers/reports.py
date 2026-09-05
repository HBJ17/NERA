"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Field Incident Reporting API Router: Crowdsourced, Official Verification & Offline Sync
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.models.schemas import (
    FieldReportCreate,
    FieldReportRecord,
    FieldReportVerifyRequest
)
from app.services.fleet_tracker import fleet_manager

router = APIRouter(prefix="/reports", tags=["Field Reporting"])

@router.get("/all")
def get_all_reports() -> List[Dict[str, Any]]:
    """Returns all submitted and verified hazard reports"""
    return fleet_manager.get_field_reports()

@router.get("/pending")
def get_pending_verification_reports() -> List[Dict[str, Any]]:
    """Returns crowdsourced hazard reports awaiting government employee review"""
    return fleet_manager.get_pending_reports()

@router.post("/submit", response_model=FieldReportRecord)
def submit_field_report(report: FieldReportCreate):
    """
    Submits an on-ground disaster/blockage report with GPS and photo evidence.
    """
    return fleet_manager.add_field_report(report)

@router.post("/verify/{report_id}")
def verify_report(report_id: str, req: FieldReportVerifyRequest) -> Dict[str, Any]:
    """
    Government Employee or Admin action: Confirm or Reject a pending report.
    Confirmed reports are immediately promoted to active incidents and propagated to Digital Twin.
    """
    result = fleet_manager.verify_field_report(report_id, req)
    if not result:
        raise HTTPException(status_code=404, detail="Field report not found")
    return {
        "status": "success",
        "action": req.action,
        "report": result
    }

@router.post("/sync-batch")
def sync_offline_reports_batch(reports: List[FieldReportCreate]) -> Dict[str, Any]:
    """
    Batch synchronization endpoint for reports captured offline without internet in remote hill terrains.
    """
    synced = fleet_manager.sync_batch_offline_reports(reports)
    return {
        "status": "synced",
        "synced_count": len(synced),
        "reports": synced
    }
