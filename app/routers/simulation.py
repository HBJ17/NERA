"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Simulation API Router: 'What-If' Disaster Scenario Execution & Resilience Sandbox
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

@router.post("/run", response_model=DisasterSimulationResponse)
def run_what_if_simulation(req: DisasterSimulationRequest):
    """
    Executes 'What-If' disaster disruption simulation:
    Evaluates isolated districts, delayed life-saving supplies, and generates AI alternate corridors.
    """
    return disaster_sim_engine.run_simulation(req)
