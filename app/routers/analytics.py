"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Analytics & Logistics Intelligence API Router
"""
from fastapi import APIRouter
from typing import Dict, Any
from app.services.analytics_engine import analytics_engine

router = APIRouter(prefix="/analytics", tags=["Analytics & Intelligence"])

@router.get("/summary")
def get_executive_analytics_summary() -> Dict[str, Any]:
    """Returns aggregated executive analytics: Logistics efficiency, disaster trends, and report turnaround"""
    return analytics_engine.get_executive_summary()

@router.get("/logistics")
def get_logistics_analytics() -> Dict[str, Any]:
    """Returns freight transit efficiency, delays, and fuel savings estimates"""
    return analytics_engine.get_logistics_analytics()

@router.get("/disasters")
def get_disaster_analytics() -> Dict[str, Any]:
    """Returns hazard frequency breakdown, high-risk district rankings, and response times"""
    return analytics_engine.get_disaster_analytics()

@router.get("/reports")
def get_reports_analytics() -> Dict[str, Any]:
    """Returns verification accuracy, turnaround metrics, and crowdsourced vs official ratio"""
    return analytics_engine.get_field_reporting_analytics()

@router.get("/dvi-matrix")
def get_dvi_matrix() -> Dict[str, Any]:
    """
    Returns District Vulnerability Index (DVI) across all NER districts,
    combining isolation probability, road redundancy, and medical stock runway.
    """
    matrix = analytics_engine.get_dvi_matrix()
    return {
        "status": "success",
        "total_districts": len(matrix),
        "critical_count": sum(1 for d in matrix if d["tier"] == "CRITICAL_ISOLATION_ZONE"),
        "high_hazard_count": sum(1 for d in matrix if d["tier"] == "HIGH_HAZARD_SECTOR"),
        "matrix": matrix
    }

@router.get("/spof-bottlenecks")
def get_spof_bottlenecks() -> Dict[str, Any]:
    """
    Returns Single Points of Failure (SPOF) across the North Eastern transport network,
    highlighting critical highway choke points and downstream isolated populations.
    """
    bottlenecks = analytics_engine.get_spof_bottlenecks()
    return {
        "status": "success",
        "choke_points_count": len(bottlenecks),
        "bottlenecks": bottlenecks
    }

