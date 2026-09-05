"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Module 18: Strategic District Management & State-Level Infrastructure Store
"""
from typing import Dict, List, Any, Optional
from app.services.digital_twin_data import NER_DISTRICT_NODES
from app.services.role_manager import role_manager

class DistrictManager:
    def __init__(self):
        self.districts = list(NER_DISTRICT_NODES)

    def get_all_districts(self) -> List[Dict[str, Any]]:
        result = []
        for d in self.districts:
            prof = role_manager.district_profiles.get(d["id"], {})
            result.append({
                **d,
                "assigned_officer": prof.get("officer_name", "District Incident Commander"),
                "department": prof.get("department", f"{d['state']} SDMA"),
                "trust_score": prof.get("trust_score", 90.0)
            })
        return result

    def get_districts_by_state(self, state: str) -> List[Dict[str, Any]]:
        return [d for d in self.get_all_districts() if d["state"].lower() == state.lower()]

    def get_district_statistics(self) -> Dict[str, Any]:
        all_d = self.get_all_districts()
        states = list(set(d["state"] for d in all_d))
        total_pop = sum(d.get("population", 0) for d in all_d)
        total_hospitals = sum(d.get("hospitals", 1) for d in all_d)
        connected_count = len([d for d in all_d if d.get("status") == "connected"])

        return {
            "total_districts": len(all_d),
            "total_states": len(states),
            "states_list": sorted(states),
            "total_population": total_pop,
            "total_hospitals": total_hospitals,
            "connected_districts": connected_count,
            "limited_access_districts": len(all_d) - connected_count,
            "average_oxygen_runway_days": round(sum(d.get("stock_oxygen_days", 10.0) for d in all_d) / max(1, len(all_d)), 1),
            "average_food_runway_days": round(sum(d.get("stock_rations_days", 25.0) for d in all_d) / max(1, len(all_d)), 1)
        }

district_manager = DistrictManager()
