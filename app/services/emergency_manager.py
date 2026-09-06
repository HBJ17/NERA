"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Module 17: Multi-Agency Emergency Incident & Green Corridor Dispatch Engine
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
from app.services.fleet_tracker import fleet_manager
from app.services.digital_twin_data import NER_DISTRICT_NODES, NER_ROAD_EDGES

class EmergencyManager:
    def __init__(self):
        self.active_green_corridors: List[Dict[str, Any]] = [
            {
                "corridor_id": "gc_guwahati_silchar_o2",
                "title": "Cryogenic Oxygen Express Green Corridor",
                "origin": "Guwahati (Kamrup Metro)",
                "destination": "Silchar Medical College (Cachar)",
                "priority_level": "LIFE_SAVING_CRITICAL",
                "cargo": "16,000 L Liquid Medical Oxygen",
                "highway_corridor": "NH-27 / NH-06 Alternate Bypass",
                "clearance_escort": "Assam Highway Police & NDRF 1st Bn Escort",
                "status": "ACTIVE_TRANSIT",
                "eta_hours": 6.5
            }
        ]

    def get_emergency_protocols(self) -> Dict[str, Any]:
        return {
            "emergency_system_status": "ACTIVE_DISASTER_MONITORING",
            "active_green_corridors_count": len(self.active_green_corridors),
            "green_corridors": self.active_green_corridors,
            "resource_prioritization": [
                {"category": "Medical Oxygen", "priority": 1, "protocol": "Unconditional police escort & green signals at toll checkposts"},
                {"category": "Cold-Chain Vaccines", "priority": 2, "protocol": "Temperature telemetry tracking & auxiliary generator clearance"},
                {"category": "FCI Food Rations", "priority": 3, "protocol": "Bulk convoy movement via cleared arterial bridges"},
                {"category": "Petroleum & Diesel", "priority": 4, "protocol": "Regulated tanker transit through hill passes"}
            ],
            "ndrf_battalions_standby": [
                {"unit": "NDRF 1st Battalion (Patgaon, Guwahati)", "sector": "Lower Assam & Meghalaya", "status": "DEPLOYED"},
                {"unit": "NDRF 12th Battalion (Itanagar)", "sector": "Arunachal & Upper Assam", "status": "STANDBY"},
                {"unit": "SDRF Nagaland (Kohima)", "sector": "Nagaland & Manipur Corridor", "status": "STANDBY"}
            ]
        }

    def get_inland_waterways_terminals(self) -> List[Dict[str, Any]]:
        """Returns Brahmaputra National Waterway-2 (NW-2) riverine cargo terminals"""
        return [
            {"id": "nw2_dhubri", "name": "Dhubri River Port", "chainage_km": 0, "coordinates": [26.0200, 89.9700], "cargo_berths": 4, "draft_depth_m": 2.5, "tonnage_capacity_daily": 2500, "status": "OPERATIONAL"},
            {"id": "nw2_jogighopa", "name": "Jogighopa Multi-Modal Terminal", "chainage_km": 80, "coordinates": [26.1900, 90.5800], "cargo_berths": 6, "draft_depth_m": 2.8, "tonnage_capacity_daily": 4500, "status": "OPERATIONAL"},
            {"id": "nw2_pandu", "name": "Pandu Port (Guwahati Central)", "chainage_km": 260, "coordinates": [26.1600, 91.6800], "cargo_berths": 8, "draft_depth_m": 3.0, "tonnage_capacity_daily": 6000, "status": "OPERATIONAL"},
            {"id": "nw2_tezpur", "name": "Tezpur (Jahajghat) Terminal", "chainage_km": 420, "coordinates": [26.6200, 92.7900], "cargo_berths": 3, "draft_depth_m": 2.2, "tonnage_capacity_daily": 2000, "status": "OPERATIONAL"},
            {"id": "nw2_silghat", "name": "Silghat Terminal (Kaziranga Buffer)", "chainage_km": 450, "coordinates": [26.6000, 92.9300], "cargo_berths": 2, "draft_depth_m": 2.0, "tonnage_capacity_daily": 1500, "status": "OPERATIONAL"},
            {"id": "nw2_neamati", "name": "Neamati Ghat (Jorhat / Majuli)", "chainage_km": 580, "coordinates": [26.8600, 94.2200], "cargo_berths": 3, "draft_depth_m": 2.0, "tonnage_capacity_daily": 1800, "status": "OPERATIONAL"},
            {"id": "nw2_dibrugarh", "name": "Dibrugarh (Bogibeel) Terminal", "chainage_km": 768, "coordinates": [27.4800, 94.9000], "cargo_berths": 4, "draft_depth_m": 2.2, "tonnage_capacity_daily": 3000, "status": "OPERATIONAL"},
            {"id": "nw2_sadiya", "name": "Sadiya Terminal (Eastern Terminus)", "chainage_km": 891, "coordinates": [27.8300, 95.6600], "cargo_berths": 2, "draft_depth_m": 1.8, "tonnage_capacity_daily": 1000, "status": "OPERATIONAL"}
        ]

    def get_airbridge_algs(self) -> List[Dict[str, Any]]:
        """Returns Advanced Landing Grounds (ALGs) and strategic relief helipads across NER"""
        return [
            {"id": "alg_tezpur", "name": "Tezpur AFS (Central Air Base)", "state": "Assam", "coordinates": [26.7090, 92.7840], "runway_length_m": 2743, "suitable_aircraft": ["C-130J Super Hercules", "Il-76", "An-32", "Mi-17V5"], "status": "ACTIVE_24x7"},
            {"id": "alg_chabua", "name": "Chabua AFS (Eastern Lifeline)", "state": "Assam", "coordinates": [27.4640, 95.1170], "runway_length_m": 2743, "suitable_aircraft": ["C-17 Globemaster", "C-130J", "Chinook", "Mi-17"], "status": "ACTIVE_24x7"},
            {"id": "alg_pasighat", "name": "Pasighat ALG", "state": "Arunachal Pradesh", "coordinates": [28.0670, 95.3340], "runway_length_m": 2060, "suitable_aircraft": ["An-32", "C-295", "Chinook", "Pawan Hans"], "status": "ACTIVE_TACTICAL"},
            {"id": "alg_tawang", "name": "Tawang High Altitude Helipad (10,000 ft)", "state": "Arunachal Pradesh", "coordinates": [27.5880, 91.8650], "runway_length_m": 450, "suitable_aircraft": ["Chinook CH-47", "Mi-17V5", "Pawan Hans Bell-412"], "status": "ACTIVE_MOUNTAIN"},
            {"id": "alg_ziro", "name": "Ziro ALG", "state": "Arunachal Pradesh", "coordinates": [27.5920, 93.8290], "runway_length_m": 1200, "suitable_aircraft": ["Dornier-228", "Mi-17", "ALH Dhruv"], "status": "ACTIVE_TACTICAL"},
            {"id": "alg_umroi", "name": "Shillong (Umroi Airport)", "state": "Meghalaya", "coordinates": [25.7030, 91.9790], "runway_length_m": 1829, "suitable_aircraft": ["ATR-72", "C-295", "An-32"], "status": "OPERATIONAL"},
            {"id": "alg_pakyong", "name": "Pakyong High-Altitude Airport", "state": "Sikkim", "coordinates": [27.2340, 88.5870], "runway_length_m": 1700, "suitable_aircraft": ["ATR-72", "Dornier-228", "Mi-17"], "status": "OPERATIONAL_WEATHER_PERMITTING"},
            {"id": "alg_imphal", "name": "Imphal Tulihal Airport", "state": "Manipur", "coordinates": [24.7600, 93.8960], "runway_length_m": 2746, "suitable_aircraft": ["C-17 Globemaster", "C-130J", "Il-76", "Commercial Cargo"], "status": "ACTIVE_24x7"}
        ]

    def get_multimodal_contingency(self, origin: str, destination: str) -> Dict[str, Any]:
        """
        Synthesizes multi-modal contingency relief channels when highway arteries are severed:
        1. NW-2 Riverine Cargo Barges (Brahmaputra)
        2. Airbridge & Pawan Hans / IAF Heavy Helicopter Sorties
        3. Border Roads Organisation (BRO) Bailey Bridge Deployment
        """
        return {
            "origin": origin,
            "destination": destination,
            "contingency_status": "MULTI_MODAL_RELIEF_READY",
            "waterway_nw2": {
                "route_corridor": "NW-2 Pandu (Guwahati) ➔ Tezpur / Dibrugarh Inland Barge",
                "nearest_river_port": "Pandu Multi-Modal Port (Guwahati)",
                "barge_capacity_metric_tons": 800,
                "transit_time_hours": 18.0,
                "suitable_commodities": ["FCI Food Grains (Rice/Wheat)", "Liquid Petroleum Tankers", "Heavy Construction Cement"],
                "fuel_cost_index": "38% Cheaper than Road Freight"
            },
            "airbridge": {
                "corridor": "Guwahati Borjhar / Tezpur AFS ➔ Target Regional Helipad",
                "suitable_aircraft": "IAF Mi-17V5 / Chinook CH-47 / Pawan Hans Bell-412",
                "flight_turnaround_minutes": 45.0,
                "payload_capacity_tons_per_sortie": 3.5,
                "suitable_commodities": ["Liquid Medical Oxygen Cryogenic Cylinders", "Emergency Pediatric Vaccines & Antidotes", "SDRF Life-Saving Rescue Teams"]
            },
            "bro_bailey_bridge": {
                "assigned_taskforce": "BRO Project Vartak / Project Pushpak",
                "bridge_class": "Class 70R Double-Single Pre-Engineered Steel Bailey",
                "estimated_mobilization_time_hours": 14.0,
                "launch_duration_hours": 18.0,
                "temporary_capacity": "Allows 40-Ton Freight Convoys to Resume Transit"
            }
        }

    def dispatch_green_corridor(self, corridor_data: Dict[str, Any]) -> Dict[str, Any]:
        corridor_id = f"gc_{datetime.now().strftime('%H%M%S')}"
        record = {
            "corridor_id": corridor_id,
            "title": corridor_data.get("title", "Emergency Life-Saving Green Corridor"),
            "origin": corridor_data.get("origin", "Guwahati"),
            "destination": corridor_data.get("destination", "Kohima"),
            "priority_level": "LIFE_SAVING_CRITICAL",
            "cargo": corridor_data.get("cargo", "Emergency Medical Supplies"),
            "highway_corridor": corridor_data.get("highway", "NH-27 / NH-29"),
            "clearance_escort": "Priority Police Convoy Escort",
            "status": "DISPATCHED",
            "eta_hours": corridor_data.get("eta_hours", 5.0)
        }
        self.active_green_corridors.insert(0, record)
        return record

emergency_manager = EmergencyManager()
