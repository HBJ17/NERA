"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Simulation API Router: 'What-If' Disaster Scenario Execution & Cross-Role Propagation
"""
from fastapi import APIRouter
from typing import Dict, Any
from app.models.schemas import (
    DisasterSimulationRequest,
    DisasterSimulationResponse
)
from app.services.simulation_engine import disaster_sim_engine

router = APIRouter(prefix="/simulation", tags=["What-If Simulation Sandbox"])

@router.get("/scenarios")
def get_preset_scenarios() -> Dict[str, Any]:
    """Returns available pre-configured disaster simulation scenarios for the North East"""
    return {
        "scenarios": [
            {
                "id": k,
                **v
            }
            for k, v in disaster_sim_engine.PRESET_SCENARIOS.items()
        ]
    }

@router.get("/active")
def get_active_simulation_state() -> Dict[str, Any]:
    """Returns current active disaster simulation if running"""
    active = disaster_sim_engine.get_active_simulation()
    return {"active": active is not None, "simulation": active}

@router.post("/run", response_model=DisasterSimulationResponse)
def run_what_if_simulation(req: DisasterSimulationRequest):
    """
    Executes 'What-If' disaster disruption simulation:
    Evaluates isolated districts, delayed life-saving supplies, propagates to digital twin maps across all roles.
    """
    return disaster_sim_engine.run_simulation(req)

@router.post("/reset")
def reset_simulation():
    """
    Resets Digital Twin road network back to normal operational state.
    """
    return disaster_sim_engine.reset_simulation()

from pydantic import BaseModel

class PointHazardRequest(BaseModel):
    lat: float
    lng: float
    disaster_type: str = "landslide"
    severity: str = "HIGH"

@router.post("/trigger-point")
def trigger_hazard_at_point(req: PointHazardRequest):
    """
    Triggers an instant disaster blockage at the closest road corridor to (lat, lng).
    Mutates digital twin network and prompts real-time vehicle & commuter rerouting.
    """
    return disaster_sim_engine.trigger_hazard_at_point(
        lat=req.lat,
        lng=req.lng,
        disaster_type=req.disaster_type,
        severity=req.severity
    )

