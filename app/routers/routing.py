"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Routing API Router: OpenStreetMap Multi-Factor Safe Route & Geocoding Endpoints
"""
from fastapi import APIRouter, Query
from typing import List, Dict, Any, Optional
from app.models.schemas import (
    RouteRequest,
    RouteOptimizationResponse
)
from app.services.routing_engine import smart_route_engine

router = APIRouter(prefix="/routing", tags=["Smart Route Engine"])

@router.get("/search")
def search_places(q: str = Query(..., min_length=1, description="Place search query for North East cities/districts")) -> List[Dict[str, Any]]:
    """
    Geocoding search across NER towns, cities, bridges, and mountain passes.
    """
    return smart_route_engine.search_places(q)

@router.post("/optimize", response_model=RouteOptimizationResponse)
def optimize_logistics_route(req: RouteRequest):
    """
    Computes AI-Optimized Multi-Factor Resilient Route comparing standard highway
    vs risk-mitigated safe bypass with turn-by-turn guidance.
    """
    return smart_route_engine.optimize_route(req)

@router.post("/reroute")
def trigger_dynamic_reroute(req: RouteRequest) -> RouteOptimizationResponse:
    """
    Dynamic Rerouting: Auto-generates a resilient bypass around active hazard disruptions.
    """
    return smart_route_engine.optimize_route(req)
