from fastapi import APIRouter
from typing import Dict, Any
from app.services.digital_twin_data import (
    NER_DISTRICT_NODES,
    NER_BRIDGES,
    NER_ROAD_EDGES
)
from app.services.fleet_tracker import fleet_manager

router = APIRouter(prefix="/twin", tags=["Digital Twin"])

@router.get("/state")
def get_digital_twin_state() -> Dict[str, Any]:
    """
    Returns the complete live state of the North Eastern Region Digital Twin:
    Districts, Bridges, Highways, Active Vehicles, Weather Sensors, and Hazards.
    """
    fleet_manager.tick_telemetry()
    return {
        "region": "North Eastern Region (NER) of India",
        "states_covered": ["Assam", "Arunachal Pradesh", "Meghalaya", "Manipur", "Mizoram", "Nagaland", "Tripura", "Sikkim"],
        "districts": fleet_manager.nodes_state,
        "bridges": NER_BRIDGES,
        "highways": fleet_manager.edges_state,
        "fleet": fleet_manager.get_fleet(),
        "threat_level": "ORANGE_MONSOON_WARNING",
        "active_disruptions_count": len([e for e in fleet_manager.edges_state if e["status"] != "open"]),
        "operational_bridges_ratio": f"{len([b for b in NER_BRIDGES if b['status'] == 'operational'])}/{len(NER_BRIDGES)}"
    }
