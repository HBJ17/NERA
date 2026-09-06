"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Module 10, 11 & 12: 'What-If' Disaster Simulation & Cross-Role Propagation Engine

Features:
- Preset & Custom Disaster Stress-Testing Scenarios (Sela Pass, Saraighat, Haflong, Teesta, Kohima)
- Graph Partitioning & Reachability Analysis across Regional Subgraphs
- Isolation Impact Quantification (Affected Population, Trapped Oxygen, Vaccines & Food Rations)
- Cross-Role Real-Time Propagation: Mutates Digital Twin road states, updates Alert tickers, and triggers user rerouting
- Complete Reset & State Recovery Lifecycle
"""
import copy
import uuid
import networkx as nx
from typing import Dict, Any, List, Optional
from datetime import datetime
from app.services.digital_twin_data import (
    NER_DISTRICT_NODES,
    NER_BRIDGES,
    NER_ROAD_EDGES,
    INITIAL_FLEET_DATA
)
from app.services.routing_engine import smart_route_engine
from app.models.schemas import (
    DisasterSimulationRequest,
    DisasterSimulationResponse,
    IsolatedDistrictReport,
    AffectedVehicleReport,
    RoutePlan,
    RouteRequest,
    EmergencyAlert
)

class DisasterSimulationEngine:
    """
    Digital Twin 'What-If' Disaster Simulation & Network Resilience Engine.
    Simulates infrastructural disruptions (bridge collapses, major landslides, river flooding),
    evaluates network partitioning, calculates essential supply risks, and computes AI alternate corridors.
    """

    PRESET_SCENARIOS = {
        "scenario_sela_landslide": {
            "title": "Severe Landslide Blockade at Sela Pass Corridor (NH-13)",
            "location": "Sela Pass Viaduct / Baisakhi - Tawang Sector",
            "target_edge": "edge_dirang_tawang",
            "target_node": "node_tawang",
            "affected_districts": ["Tawang", "West Kameng"],
            "description": "Massive 2,000 cu.m debris fall has completely blocked NH-13 at 13,700 ft elevation. Sub-zero temperatures hindering heavy earthmover clearance."
        },
        "scenario_saraighat_flood": {
            "title": "Catastrophic Flood Surge on Saraighat Bridge Corridor",
            "location": "Brahmaputra River - Guwahati North Bank Link",
            "target_edge": "edge_barpeta_guwahati",
            "target_node": "node_guwahati",
            "affected_districts": ["Guwahati", "Kamrup"],
            "description": "Brahmaputra river level surged 1.4m above extreme danger level. PWD closed bridge deck to heavy cargo convoys due to hydrodynamic turbulence."
        },
        "scenario_haflong_breach": {
            "title": "NH-27 Jatinga Valley Hill Cutting Collapse (Dima Hasao)",
            "location": "NH-27 Lumding-Haflong-Silchar Mountain Highway",
            "target_edge": "edge_nagaon_haflong",
            "target_node": "node_haflong",
            "affected_districts": ["Haflong", "Silchar", "Cachar"],
            "description": "Continuous 72h monsoon downpour (190mm) caused progressive embankment failure. Barak Valley lifeline severed."
        },
        "scenario_teesta_gorge_cut": {
            "title": "NH-10 Teesta River Gorge Submergence & Rockfall",
            "location": "NH-10 29th Mile - Sikkim Lifeline",
            "target_edge": "edge_kalimpong_gangtok",
            "target_node": "node_gangtok",
            "affected_districts": ["Gangtok", "Mangan"],
            "description": "Teesta river overflowed retaining walls with simultaneous rock slides. Land connection to Gangtok severed for 72 hours."
        },
        "scenario_kohima_mudslide": {
            "title": "NH-29 Phesama - Kohima Mountain Sinking & Mudflow",
            "location": "NH-29 Dimapur - Kohima Mountain Lifeline",
            "target_edge": "edge_dimapur_kohima",
            "target_node": "node_kohima",
            "affected_districts": ["Kohima", "Dimapur"],
            "description": "High slope saturation triggered road sinking at NH-29 Phesama bypass. Highway impassable for heavy transport."
        }
    }

    def __init__(self):
        self.active_simulation: Optional[Dict[str, Any]] = None

    def get_active_simulation(self) -> Optional[Dict[str, Any]]:
        return self.active_simulation

    def reset_simulation(self) -> Dict[str, Any]:
        """Restores Digital Twin road edges and node states back to normal operational status"""
        from app.services.fleet_tracker import fleet_manager
        fleet_manager.edges_state = copy.deepcopy(NER_ROAD_EDGES)
        fleet_manager.nodes_state = copy.deepcopy(NER_DISTRICT_NODES)
        self.active_simulation = None
        smart_route_engine.build_graph()
        return {"status": "reset", "message": "Digital Twin simulation reset to normal baseline."}

    def trigger_hazard_at_point(self, lat: float, lng: float, disaster_type: str = "landslide", severity: str = "HIGH", edge_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Dynamically simulates a disaster blockage at the closest highway corridor to (lat, lng) or matching edge_id.
        Mutates fleet_manager edges_state, rebuilds graph, and identifies affected vehicles and reroutes.
        """
        from app.services.fleet_tracker import fleet_manager

        best_edge = None
        best_dist = float("inf")
        nodes_dict = {n["id"]: n for n in NER_DISTRICT_NODES}

        if edge_id:
            for edge in fleet_manager.edges_state:
                if edge["id"] == edge_id:
                    best_edge = edge
                    break

        if not best_edge:
            for edge in fleet_manager.edges_state:
                poly = edge.get("coordinates_polyline", [])
                if not poly:
                    u_coord = nodes_dict.get(edge["source"], {}).get("coordinates", [26.0, 92.0])
                    v_coord = nodes_dict.get(edge["target"], {}).get("coordinates", [26.0, 92.0])
                    poly = [u_coord, v_coord]

                for pt in poly:
                    d = ((pt[0] - lat)**2 + (pt[1] - lng)**2)**0.5
                    if d < best_dist:
                        best_dist = d
                        best_edge = edge

        if not best_edge:
            best_edge = fleet_manager.edges_state[0]

        target_edge_id = best_edge["id"]
        highway_name = best_edge.get("name", best_edge["id"])
        highway_code = best_edge.get("highway_code", "Corridor")

        disaster_title = "Massive Rockfall & Hill Cutting Failure" if disaster_type == "landslide" else "River Flood Inundation & Embankment Breach"
        for e in fleet_manager.edges_state:
            if e["id"] == target_edge_id:
                e["status"] = "blocked"
                e["closure_reason"] = f"CRITICAL: {disaster_title} ({severity} Severity)"
                e["landslide_risk"] = 98.0 if disaster_type == "landslide" else e.get("landslide_risk", 70.0)
                e["flood_risk"] = 95.0 if disaster_type == "flood" else e.get("flood_risk", 50.0)

        # Rebuild graph with new blockage
        smart_route_engine.build_graph()

        # Check affected vehicles
        affected_vehicles = []
        for v in fleet_manager.get_fleet():
            if v.get("assigned_route_id") == target_edge_id:
                v["status"] = "delayed"
                v["delay_minutes"] = v.get("delay_minutes", 0) + 90
                affected_vehicles.append({
                    "vehicle_id": v["id"],
                    "vehicle_number": v["vehicle_number"],
                    "driver_name": v.get("driver_name", "Driver"),
                    "cargo_type": v.get("cargo_type", "Supplies"),
                    "category": v.get("category", "logistics"),
                    "status": "REROUTING"
                })

        # Store active simulation
        self.active_simulation = {
            "type": "point_hazard",
            "disaster_type": disaster_type,
            "severity": severity,
            "coordinates": [lat, lng],
            "target_edge_id": target_edge_id,
            "highway_code": highway_code,
            "highway_name": highway_name,
            "source_node": best_edge["source"],
            "target_node": best_edge["target"],
            "description": f"{disaster_title} on {highway_code} ({highway_name}) near coordinates [{lat:.4f}, {lng:.4f}]. Real-time AI bypass active.",
            "timestamp": datetime.now().strftime("%I:%M %p")
        }

        # Add emergency alert
        fleet_manager.alerts.insert(0, {
            "id": f"alert_sim_{uuid.uuid4().hex[:4]}",
            "timestamp": "Just now",
            "severity": "CRITICAL_DANGER",
            "category": disaster_type.upper(),
            "location_tag": f"{highway_code} ({highway_name})",
            "message_en": f"RED ALERT: {disaster_title} at coordinates [{lat:.3f}, {lng:.3f}]. Highway impassable. Autonomous AI safe bypass engaged for all vehicles.",
            "message_as": f"ৰঙা সতৰ্কবাৰ্তা: {highway_code} পথত দুৰ্যোগৰ বাবে যাতায়ত বন্ধ।",
            "message_hi": f"रेड अलर्ट: {highway_code} पर आपदा के कारण मार्ग अवरुद्ध। वैकल्पिक सुरक्षित मार्ग सक्रिय।",
            "message_bn": f"লাল সতর্কতা: {highway_code} পথে বিপর্যয়ের জন্য যান চলাচল বন্ধ।",
            "affected_routes": [highway_code],
            "affected_districts": [best_edge["source"], best_edge["target"]]
        })

        # Generate dynamic alternate bypass for this severed corridor
        ai_reroutes = []
        try:
            reroute_res = smart_route_engine.optimize_route(RouteRequest(
                source_id=best_edge["source"],
                destination_id=best_edge["target"],
                avoid_high_risk=True
            ))
            if reroute_res.recommended_route:
                ai_reroutes.append(reroute_res.recommended_route)
        except Exception:
            pass

        # Connectivity Matrix & Isolated Districts Analysis
        hub_node = "node_guwahati"
        connectivity_matrix = {}
        isolated_districts = []
        total_pop_affected = 0
        G_sim = smart_route_engine.G_distance.copy()
        for u, v, data in list(G_sim.edges(data=True)):
            if data.get("edge_id") == target_edge_id:
                G_sim.remove_edge(u, v)

        for n_id, n_data in nodes_dict.items():
            if n_id == hub_node:
                connectivity_matrix[n_id] = "connected"
                continue
            try:
                has_p = nx.has_path(G_sim, source=hub_node, target=n_id)
                if has_p:
                    orig_len = nx.shortest_path_length(smart_route_engine.G_distance, source=hub_node, target=n_id, weight="weight")
                    sim_len = nx.shortest_path_length(G_sim, source=hub_node, target=n_id, weight="weight")
                    status = "limited" if sim_len > orig_len * 1.4 else "connected"
                else:
                    status = "disconnected"
            except Exception:
                status = "disconnected"

            connectivity_matrix[n_id] = status
            if status in ("disconnected", "limited"):
                tier = "FULLY_CUT_OFF" if status == "disconnected" else "RESTRICTED_ACCESS"
                pop = n_data["population"]
                total_pop_affected += pop
                isolated_districts.append({
                    "district_id": n_id,
                    "district_name": n_data["name"],
                    "state": n_data["state"],
                    "population_impacted": pop,
                    "days_oxygen_left": n_data["stock_oxygen_days"],
                    "days_food_left": n_data["stock_rations_days"],
                    "isolation_tier": tier
                })

        supplies_at_risk = {
            "liquid_oxygen_liters": 16000 if len(affected_vehicles) > 0 else 0,
            "vaccines_and_insulin_tons": 3.5 if len(affected_vehicles) > 0 else 0.0,
            "fci_food_rations_tons": 18.0 if len(affected_vehicles) > 0 else 0.0,
            "petroleum_fuel_kl": 24.0 if len(affected_vehicles) > 0 else 0.0,
            "high_priority_shipments_count": len(affected_vehicles)
        }

        # Structure delayed_vehicles to match what the UI expects
        formatted_delayed_vehicles = []
        for v in affected_vehicles:
            formatted_delayed_vehicles.append({
                "vehicle_id": v["vehicle_id"],
                "vehicle_number": v["vehicle_number"],
                "cargo_type": v.get("cargo_type", "Emergency Supplies"),
                "cargo_priority": "CRITICAL",
                "destination": v.get("target_node", best_edge["target"]),
                "current_status": "REROUTING_DISPATCHED",
                "estimated_delay_hrs": 3.5,
                "suggested_reroute_id": "Diverted along AI Resilient Safe Corridor"
            })

        emergency_protocols = [
            f"🚨 POINT HAZARD INJECTION ACTIVE: Simulated {disaster_type.capitalize()} on {highway_code}.",
            f"1. AI Safe Corridor Bypass engaged between {best_edge['source']} and {best_edge['target']}.",
            f"2. {len(affected_vehicles)} vehicles rerouted around severed sector.",
            f"3. {len(isolated_districts)} district hubs monitored for critical survival supply runway.",
            "4. Real-time digital twin state synchronized across all stakeholder consoles."
        ]

        return {
            "status": "hazard_triggered",
            "scenario_title": f"Simulated {disaster_type.capitalize()} Blockade at {highway_code}",
            "incident_location": f"{highway_code} (Lat {lat:.4f}, Lng {lng:.4f})",
            "target_edge_id": target_edge_id,
            "nearest_edge_id": target_edge_id,
            "highway_code": highway_code,
            "highway_name": highway_name,
            "severed_highway": highway_code,
            "coordinates": [lat, lng],
            "disaster_type": disaster_type,
            "severity": severity,
            "message": f"Blockade established on {highway_code} ({highway_name}). Dynamic AI Reroute engaged.",
            "affected_vehicles": affected_vehicles,
            "delayed_vehicles": formatted_delayed_vehicles,
            "ai_generated_reroutes": ai_reroutes,
            "isolated_districts": isolated_districts,
            "total_population_affected": total_pop_affected,
            "critical_supplies_at_risk": supplies_at_risk,
            "emergency_action_recommendations": emergency_protocols,
            "connectivity_matrix": connectivity_matrix,
            "source_node": best_edge["source"],
            "target_node": best_edge["target"]
        }

    def run_simulation(self, req: DisasterSimulationRequest) -> DisasterSimulationResponse:
        scenario_id = req.scenario_id
        preset = self.PRESET_SCENARIOS.get(scenario_id, None)

        if preset:
            scenario_title = preset["title"]
            incident_loc = preset["location"]
            target_edge = preset["target_edge"]
            target_node = preset["target_node"]
            aff_districts = preset.get("affected_districts", ["Target District"])
            desc = preset["description"]
        else:
            scenario_title = f"Custom Stress Simulation: {req.target_edge_id or req.target_node_id or 'Regional Hazard'}"
            incident_loc = "Custom Target Sector"
            target_edge = req.target_edge_id or "edge_bomdila_tawang"
            target_node = req.target_node_id or "node_tawang"
            aff_districts = ["Regional Sector"]
            desc = f"Simulated disaster with severity {req.disaster_severity} on critical corridor."

        # Build simulated network graph
        G_sim = nx.Graph()
        nodes_dict = {n["id"]: n for n in NER_DISTRICT_NODES}
        for n_id, n_data in nodes_dict.items():
            G_sim.add_node(n_id, **n_data)

        # Add edges, excluding severed edge
        severed_edges = []
        for e in NER_ROAD_EDGES:
            if e["id"] == target_edge:
                severed_edges.append(e)
                continue # Omit severed link
            G_sim.add_edge(e["source"], e["target"], **e)

        # 1. Connectivity Matrix & Isolated Districts Analysis
        hub_node = "node_guwahati"
        connectivity_matrix = {}
        isolated_districts: List[IsolatedDistrictReport] = []
        total_pop_affected = 0

        for n_id, n_data in nodes_dict.items():
            if n_id == hub_node:
                connectivity_matrix[n_id] = "connected"
                continue

            try:
                has_path = nx.has_path(G_sim, source=hub_node, target=n_id)
                if has_path:
                    orig_len = nx.shortest_path_length(smart_route_engine.G_distance, source=hub_node, target=n_id, weight="weight")
                    sim_len = nx.shortest_path_length(G_sim, source=hub_node, target=n_id, weight="weight")
                    if sim_len > orig_len * 1.5:
                        status = "limited"
                    else:
                        status = "connected"
                else:
                    status = "disconnected"
            except Exception:
                status = "disconnected"

            connectivity_matrix[n_id] = status

            if status in ("disconnected", "limited"):
                tier = "FULLY_CUT_OFF" if status == "disconnected" else "RESTRICTED_ACCESS"
                pop = n_data["population"]
                total_pop_affected += pop
                isolated_districts.append(IsolatedDistrictReport(
                    district_id=n_id,
                    district_name=n_data["name"],
                    state=n_data["state"],
                    population_impacted=pop,
                    days_oxygen_left=n_data["stock_oxygen_days"],
                    days_food_left=n_data["stock_rations_days"],
                    isolation_tier=tier
                ))

        # 2. Affected Active Vehicles
        delayed_vehicles: List[AffectedVehicleReport] = []
        supplies_at_risk = {
            "liquid_oxygen_liters": 0,
            "vaccines_and_insulin_tons": 0.0,
            "fci_food_rations_tons": 0.0,
            "petroleum_fuel_kl": 0.0,
            "high_priority_shipments_count": 0
        }

        for v in INITIAL_FLEET_DATA:
            is_affected = False
            delay_h = 0.0
            reroute_desc = None

            if v.get("assigned_route_id") == target_edge:
                is_affected = True
                delay_h = 5.5
                reroute_desc = "Diverted to Emergency Staging Depot / Alternate Hill Pass"
            else:
                dest_node = next((n["id"] for n in NER_DISTRICT_NODES if n["name"].split(" (")[0].lower() in v["destination"].lower()), None)
                if dest_node and connectivity_matrix.get(dest_node) == "disconnected":
                    is_affected = True
                    delay_h = 12.0
                    reroute_desc = "Awaiting Helicopter Air-Drop Transition / PWD Bailey Bridge"
                elif dest_node and connectivity_matrix.get(dest_node) == "limited":
                    is_affected = True
                    delay_h = 3.5
                    reroute_desc = "Rerouted via Long-Distance Secondary Arterial Highway"

            if is_affected:
                delayed_vehicles.append(AffectedVehicleReport(
                    vehicle_id=v["id"],
                    vehicle_number=v["vehicle_number"],
                    cargo_type=v["cargo_type"],
                    cargo_priority=v["cargo_priority"],
                    destination=v["destination"],
                    current_status="REROUTING_DISPATCHED",
                    estimated_delay_hrs=delay_h,
                    suggested_reroute_id=reroute_desc
                ))

                cargo_text = v["cargo_type"].lower()
                if "oxygen" in cargo_text:
                    supplies_at_risk["liquid_oxygen_liters"] += 16000
                    supplies_at_risk["high_priority_shipments_count"] += 1
                elif "vaccine" in cargo_text or "insulin" in cargo_text:
                    supplies_at_risk["vaccines_and_insulin_tons"] += v["cargo_weight_tons"]
                    supplies_at_risk["high_priority_shipments_count"] += 1
                elif "rice" in cargo_text or "ration" in cargo_text:
                    supplies_at_risk["fci_food_rations_tons"] += v["cargo_weight_tons"]
                elif "diesel" in cargo_text or "fuel" in cargo_text:
                    supplies_at_risk["petroleum_fuel_kl"] += 24.0

        # 3. AI Generated Alternate Strategic Corridors
        ai_reroutes: List[RoutePlan] = []
        if severed_edges:
            e = severed_edges[0]
            src_pt, dst_pt = e["source"], e["target"]
            try:
                alt_resp = smart_route_engine.optimize_route(
                    RouteRequest(
                        source_id=src_pt,
                        destination_id=dst_pt,
                        custom_avoid_edges=[target_edge]
                    )
                )
                if alt_resp.recommended_route:
                    ai_reroutes.append(alt_resp.recommended_route)
                if alt_resp.alternative_route:
                    ai_reroutes.append(alt_resp.alternative_route)
            except Exception:
                pass

        # 4. Emergency Action Protocols
        emergency_protocols = [
            f"🚨 DIGITAL TWIN SIMULATION DISPATCH: {scenario_title}",
            f"1. Priority Detour: Reroute {len(delayed_vehicles)} essential cargo convoys away from {incident_loc}.",
            f"2. Health Resource Alert: {len(isolated_districts)} districts impacted. Hospital liquid oxygen reserves tracked.",
            f"3. PWD Infrastructure Mobilization: Deploy heavy excavators and emergency Bailey Bridge units to {incident_loc}.",
            "4. Multi-Agency Coordination: Notify SDMA, NDRF 1st Battalion, and Regional Emergency Operation Centres."
        ]

        # 5. CROSS-ROLE PROPAGATION: Mutate Digital Twin In-Memory State!
        from app.services.fleet_tracker import fleet_manager
        for edge in fleet_manager.edges_state:
            if edge["id"] == target_edge:
                edge["status"] = "blocked"
                edge["landslide_risk"] = 98.0
                edge["closure_reason"] = f"SIMULATED DISASTER: {scenario_title}"

        for node in fleet_manager.nodes_state:
            if node["id"] in connectivity_matrix:
                node["status"] = connectivity_matrix[node["id"]]

        # Insert Emergency Alert into Alert Ticker
        sim_alert = {
            "id": f"sim_alt_{uuid.uuid4().hex[:4]}",
            "timestamp": "SIMULATION ACTIVE",
            "severity": "CRITICAL_DANGER",
            "category": "LANDSLIDE" if "landslide" in scenario_title.lower() else ("FLOOD" if "flood" in scenario_title.lower() else "ROAD_CLOSURE"),
            "location_tag": f"{incident_loc}",
            "message_en": f"🚨 SIMULATION ALERT: {scenario_title}. Corridor impassable at {incident_loc}. Safe bypass reroutes engaged.",
            "message_as": f"🚨 অনুৰূপ সতৰ্কবাণী: {incident_loc} ত দুৰ্যোগৰ ঘটনা। বিকল্প সুৰক্ষিত পথ ব্যৱহাৰ কৰক।",
            "message_hi": f"🚨 सिमुलेशन अलर्ट: {incident_loc} पर भीषण आपदा सिमुलेट की गई। सुरक्षित वैकल्पिक मार्ग तैयार।",
            "message_bn": f"🚨 সিমুলেশন সতর্কতা: {incident_loc} এ দুর্যোগ। নিরাপদ বাইপাস রুট সক্রিয়।",
            "affected_routes": [target_edge],
            "affected_districts": aff_districts
        }
        fleet_manager.alerts.insert(0, sim_alert)

        # Store active simulation state
        self.active_simulation = {
            "scenario_title": scenario_title,
            "incident_location": incident_loc,
            "target_edge": target_edge,
            "target_node": target_node,
            "affected_districts": aff_districts,
            "isolated_districts_count": len(isolated_districts),
            "delayed_vehicles_count": len(delayed_vehicles),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
        }

        # Rebuild routing graph
        smart_route_engine.build_graph()

        return DisasterSimulationResponse(
            scenario_title=scenario_title,
            incident_location=incident_loc,
            impact_timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S IST"),
            isolated_districts=isolated_districts,
            total_population_affected=total_pop_affected,
            delayed_vehicles=delayed_vehicles,
            critical_supplies_at_risk=supplies_at_risk,
            ai_generated_reroutes=ai_reroutes,
            emergency_action_recommendations=emergency_protocols,
            connectivity_matrix=connectivity_matrix
        )

disaster_sim_engine = DisasterSimulationEngine()
