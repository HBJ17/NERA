"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Routing API Router: Multi-Factor Safe Route Optimization Endpoints
"""
from fastapi import APIRouter
from app.models.schemas import (
    RouteRequest,
    RouteOptimizationResponse
)
from app.services.routing_engine import smart_route_engine

router = APIRouter(prefix="/routing", tags=["Smart Route Engine"])

@router.post("/optimize", response_model=RouteOptimizationResponse)
def optimize_logistics_route(req: RouteRequest):
    """
    Computes AI-Optimized Multi-Factor Resilient Route comparing standard highway
    vs risk-mitigated safe bypass with turn-by-turn guidance.
    """
    return smart_route_engine.optimize_route(req)
