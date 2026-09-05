"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Role & Persona Management Service: 1-Click Multi-Stakeholder Switcher
"""
from typing import Dict, List, Any, Optional
from app.services.digital_twin_data import NER_DISTRICT_NODES

DEFAULT_DISTRICT_PROFILES = {
    "node_kohima": {
        "officer_name": "Er. T. Jamir",
        "department": "PWD & Nagaland SDMA",
        "designation": "Executive Disaster Response Engineer",
        "district_id": "node_kohima",
        "district_name": "Kohima",
        "state": "Nagaland",
        "trust_score": 92.0
    },
    "node_imphal": {
        "officer_name": "Dr. L. Singh",
        "department": "Manipur Emergency Operations Centre",
        "designation": "District Relief Commissioner",
        "district_id": "node_imphal",
        "district_name": "Imphal (Manipur Central)",
        "state": "Manipur",
        "trust_score": 94.0
    },
    "node_aizawl": {
        "officer_name": "Z. Ralte",
        "department": "Mizoram Disaster Management Authority",
        "designation": "District Highway Safety Officer",
        "district_id": "node_aizawl",
        "district_name": "Aizawl",
        "state": "Mizoram",
        "trust_score": 90.0
    },
    "node_pasighat": {
        "officer_name": "K. Lego",
        "department": "PWD Highway Division (East Siang)",
        "designation": "Senior Infrastructure Inspector",
        "district_id": "node_pasighat",
        "district_name": "Pasighat (East Siang)",
        "state": "Arunachal Pradesh",
        "trust_score": 91.0
    },
    "node_guwahati": {
        "officer_name": "S. Barua",
        "department": "Assam SDMA Central Operations",
        "designation": "State Logistics & Relief Controller",
        "district_id": "node_guwahati",
        "district_name": "Guwahati (Kamrup Metro)",
        "state": "Assam",
        "trust_score": 96.0
    },
    "node_shillong": {
        "officer_name": "P. Kharkongor",
        "department": "Meghalaya Disaster Relief Cell",
        "designation": "District Emergency Operations Manager",
        "district_id": "node_shillong",
        "district_name": "Shillong (East Khasi Hills)",
        "state": "Meghalaya",
        "trust_score": 93.0
    },
    "node_gangtok": {
        "officer_name": "T. Bhutia",
        "department": "Sikkim SDRF & Highway Protection",
        "designation": "Mountain Corridor Incident Commander",
        "district_id": "node_gangtok",
        "district_name": "Gangtok",
        "state": "Sikkim",
        "trust_score": 95.0
    },
    "node_agartala": {
        "officer_name": "D. Debbarma",
        "department": "Tripura Emergency Management Office",
        "designation": "Divisional Relief Officer",
        "district_id": "node_agartala",
        "district_name": "Agartala",
        "state": "Tripura",
        "trust_score": 89.0
    },
    "node_haflong": {
        "officer_name": "B. Thaosen",
        "department": "Dima Hasao Hill Highway Inspectorate",
        "designation": "Hill Slopes Geological Monitor",
        "district_id": "node_haflong",
        "district_name": "Haflong (Dima Hasao)",
        "state": "Assam",
        "trust_score": 90.0
    }
}

class RoleManager:
    def __init__(self):
        self.current_role: str = "admin" # "admin", "user", "gov_employee"
        self.current_district_id: str = "node_kohima"
        self.district_profiles: Dict[str, Dict[str, Any]] = dict(DEFAULT_DISTRICT_PROFILES)
        
        # Populate any missing districts dynamically from NER_DISTRICT_NODES
        for node in NER_DISTRICT_NODES:
            n_id = node["id"]
            if n_id not in self.district_profiles:
                self.district_profiles[n_id] = {
                    "officer_name": f"Officer {node['name'].split(' (')[0]}",
                    "department": f"{node['state']} SDMA District Cell",
                    "designation": "District Emergency Operations Officer",
                    "district_id": n_id,
                    "district_name": node["name"],
                    "state": node["state"],
                    "trust_score": 88.0
                }

    def get_available_roles(self) -> Dict[str, Any]:
        return {
            "roles": [
                {
                    "id": "admin",
                    "name": "Admin",
                    "badge": "AI-GIS Commander",
                    "description": "Full regional AI-GIS control, digital twin stress-testing, analytics, fleet logistics.",
                    "icon": "👑"
                },
                {
                    "id": "user",
                    "name": "Citizen / Traveller",
                    "badge": "Smart Route Navigator",
                    "description": "Google Maps-like smart navigation with AI disaster risk layers and hazard bypass.",
                    "icon": "🚗"
                },
                {
                    "id": "gov_employee",
                    "name": "Government Employee",
                    "badge": "District Incident Officer",
                    "description": "District-scoped monitoring, pending report verification queue, and official reporting.",
                    "icon": "🏛️"
                }
            ],
            "districts": [
                {
                    "id": node["id"],
                    "name": node["name"],
                    "state": node["state"],
                    "coordinates": node["coordinates"],
                    "officer": self.district_profiles.get(node["id"], {}).get("officer_name", "Officer"),
                    "department": self.district_profiles.get(node["id"], {}).get("department", "SDMA")
                }
                for node in NER_DISTRICT_NODES
            ],
            "current_role": self.current_role,
            "current_district": self.get_current_profile()
        }

    def get_current_profile(self) -> Dict[str, Any]:
        profile = self.district_profiles.get(self.current_district_id, self.district_profiles["node_kohima"])
        district_node = next((n for n in NER_DISTRICT_NODES if n["id"] == self.current_district_id), NER_DISTRICT_NODES[0])
        return {
            "role": self.current_role,
            "district_id": self.current_district_id,
            "profile": profile,
            "district_metadata": district_node
        }

    def switch_role(self, role: str, district_id: Optional[str] = None) -> Dict[str, Any]:
        if role in ("admin", "user", "gov_employee"):
            self.current_role = role
        if district_id and (district_id in self.district_profiles or any(n["id"] == district_id for n in NER_DISTRICT_NODES)):
            self.current_district_id = district_id
        return self.get_current_profile()

role_manager = RoleManager()
