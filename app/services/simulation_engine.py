"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Module 10: 'What-If' Disaster Simulation & Network Resilience Sandbox

Features:
- Preset & Custom Disaster Stress-Testing Scenarios (Sela Pass, Saraighat, Haflong, Teesta)
- Graph Partitioning & Reachability Analysis across Regional Subgraphs
- Isolation Impact Quantification (Affected Population, Trapped Oxygen, Vaccines & Food Rations)
- Autonomous Multi-Agency Standard Operating Procedures (SOP) Directives
"""
import copy
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
    RoutePlan
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
            "target_edge": "edge_bomdila_tawang",
            "target_node": "node_tawang",
            "description": "Massive 2,000 cu.m debris fall has completely blocked NH-13 at 13,700 ft elevation. Sub-zero temperatures hindering heavy earthmover clearance."
        },
        "scenario_saraighat_flood": {
            "title": "Catastrophic Flood Surge on Saraighat Bridge Corridor",
            "location": "Brahmaputra River - Guwahati North Bank Link",
            "target_edge": "edge_siliguri_guwahati",
            "target_node": "bridge_saraighat",
            "description": "Brahmaputra river level surged 1.4m above extreme danger level. PWD closed bridge deck to heavy cargo convoys due to hydrodynamic turbulence."
        },
        "scenario_haflong_breach": {
            "title": "NH-27 Jatinga Valley Hill Cutting Collapse (Dima Hasao)",
            "location": "NH-27 Lumding-Haflong-Silchar Mountain Highway",
            "target_edge": "edge_nagaon_haflong",
            "target_node": "node_haflong",
            "description": "Continuous 72h monsoon downpour (190mm) caused progressive embankment failure. Barak Valley lifeline severed."
        },
        "scenario_teesta_gorge_cut": {
            "title": "NH-10 Teesta River Gorge Submergence & Rockfall",
            "location": "NH-10 29th Mile - Sikkim Lifeline",
            "target_edge": "edge_siliguri_gangtok",
            "target_node": "node_gangtok",
            "description": "Teesta river overflowed retaining walls with simultaneous rock slides. Land connection to Gangtok severed for 72 hours."
        }
    }

    def run_simulation(self, req: DisasterSimulationRequest) -> DisasterSimulationResponse:
        scenario_id = req.scenario_id
        preset = self.PRESET_SCENARIOS.get(scenario_id, None)

        if preset:
            scenario_title = preset["title"]
            incident_loc = preset["location"]
            target_edge = preset["target_edge"]
            target_node = preset["target_node"]
        else:
            scenario_title = f"Custom Stress Simulation: {req.target_edge_id or req.target_node_id or 'Regional Hazard'}"
            incident_loc = "Custom Target Sector"
            target_edge = req.target_edge_id or "edge_bomdila_tawang"
            target_node = req.target_node_id or "node_tawang"

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
        hub_node = "node_guwahati" # Central logistics gateway
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
                    # Check if path length significantly increased
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
            # Check if vehicle is traversing severed edge or heading to isolated node
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

                # Aggregate supplies
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
            # Try computing alternate route between severed edge endpoints
            src_pt, dst_pt = e["source"], e["target"]
            try:
                alt_resp = smart_route_engine.optimize_route(
                    smart_route_engine.RouteRequest(
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
            f"🚨 DIGITAL TWIN ACTION PLAN: Disruption in {incident_loc}",
            f"1. Priority Dispatch: Reroute {len(delayed_vehicles)} commercial freight vehicles to green corridors immediately.",
            f"2. Health Department Alert: {len(isolated_districts)} districts flagged. Monitor hospital liquid oxygen reserves (< 5 days stock).",
            f"3. PWD Infrastructure Mobilization: Deploy heavy excavators and emergency Bailey Bridge construction units to {incident_loc}.",
            "4. Multi-Agency Coordination: Notify SDMA, NDRF 1st Battalion (Guwahati/Patgaon), and Food Corporation of India regional depots."
        ]

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
