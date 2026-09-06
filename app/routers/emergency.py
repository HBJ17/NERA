"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Emergency Management & Priority Green Corridors API Router
"""
from fastapi import APIRouter
from typing import Dict, Any, List
from pydantic import BaseModel
from app.services.emergency_manager import emergency_manager

router = APIRouter(prefix="/emergency", tags=["Emergency Management & Green Corridors"])

class GreenCorridorRequest(BaseModel):
    title: str
    origin: str
    destination: str
    cargo: str
    highway: str
    eta_hours: float = 5.0

@router.get("/protocols")
def get_emergency_protocols() -> Dict[str, Any]:
    """Returns active emergency response protocols, green corridors, and NDRF standby units"""
    return emergency_manager.get_emergency_protocols()

@router.post("/dispatch-green-corridor")
def dispatch_emergency_green_corridor(req: GreenCorridorRequest) -> Dict[str, Any]:
    """Activates prioritized life-saving green corridor for critical medical supplies"""
    return emergency_manager.dispatch_green_corridor(req.model_dump())

@router.get("/inland-waterways")
def get_inland_waterways() -> List[Dict[str, Any]]:
    """Returns National Waterway-2 (NW-2) river ports and daily cargo handling berths"""
    return emergency_manager.get_inland_waterways_terminals()

@router.get("/airbridge-algs")
def get_airbridge_algs() -> List[Dict[str, Any]]:
    """Returns Advanced Landing Grounds (ALGs) and strategic relief helipads"""
    return emergency_manager.get_airbridge_algs()

@router.get("/multimodal-contingency")
def get_multimodal_contingency(origin: str = "Guwahati", destination: str = "Tawang") -> Dict[str, Any]:
    """
    Computes emergency multi-modal fallback corridors (Brahmaputra NW-2 barge,
    IAF/Pawan Hans airbridge sorties, and BRO Bailey bridging) for severed highway routes.
    """
    return emergency_manager.get_multimodal_contingency(origin, destination)

