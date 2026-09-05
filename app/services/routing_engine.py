"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Module 2, 3 & 9: OpenStreetMap Multi-Factor Resilient Routing & Safe-Corridor Engine

Features:
- Dual Graph Network Architecture: Physical Distance Graph vs Hazard Cost Graph
- Dynamic Dijkstra & Yen's K-Shortest Simple Paths Algorithm
- Place search & geocoding across North Eastern region cities, districts, highways, and passes
- Real-time synchronization with Digital Twin road blockage states & simulated disasters
- Dynamic Rerouting Engine generating Safe-Corridor Bypasses around severed sectors
"""
import math
import networkx as nx
from typing import Dict, Any, List, Optional, Tuple
from app.services.digital_twin_data import NER_DISTRICT_NODES, NER_ROAD_EDGES, NER_BRIDGES
from app.models.schemas import (
    RouteRequest,
    RouteOptimizationResponse,
    RoutePlan,
    RouteSegment
)

# Places database for instant autocomplete / geocoding
NER_PLACES_INDEX = [
    {"name": "Guwahati (Kamrup Metro)", "district_id": "node_guwahati", "state": "Assam", "coordinates": [26.1445, 91.7362], "type": "City / Gateway Hub"},
    {"name": "Kohima", "district_id": "node_kohima", "state": "Nagaland", "coordinates": [25.6751, 94.1086], "type": "Capital City"},
    {"name": "Imphal East / West", "district_id": "node_imphal", "state": "Manipur", "coordinates": [24.8170, 93.9368], "type": "Capital City"},
    {"name": "Shillong (East Khasi Hills)", "district_id": "node_shillong", "state": "Meghalaya", "coordinates": [25.5788, 91.8933], "type": "Capital City"},
    {"name": "Aizawl", "district_id": "node_aizawl", "state": "Mizoram", "coordinates": [23.7271, 92.7176], "type": "Capital City"},
    {"name": "Itanagar (Papum Pare)", "district_id": "node_itanagar", "state": "Arunachal Pradesh", "coordinates": [27.0844, 93.6053], "type": "Capital City"},
    {"name": "Gangtok", "district_id": "node_gangtok", "state": "Sikkim", "coordinates": [27.3314, 88.6138], "type": "Capital City"},
    {"name": "Agartala", "district_id": "node_agartala", "state": "Tripura", "coordinates": [23.8315, 91.2868], "type": "Capital City"},
    {"name": "Pasighat (East Siang)", "district_id": "node_pasighat", "state": "Arunachal Pradesh", "coordinates": [28.0668, 95.3263], "type": "District Hub"},
    {"name": "Tawang (Sela Pass Sector)", "district_id": "node_tawang", "state": "Arunachal Pradesh", "coordinates": [27.5861, 91.8594], "type": "High Altitude Pass"},
    {"name": "Silchar (Barak Valley)", "district_id": "node_silchar", "state": "Assam", "coordinates": [24.8333, 92.7789], "type": "Logistics Hub"},
    {"name": "Haflong (Dima Hasao)", "district_id": "node_haflong", "state": "Assam", "coordinates": [25.1764, 93.0189], "type": "Hill Corridor"},
    {"name": "Dimapur", "district_id": "node_dimapur", "state": "Nagaland", "coordinates": [25.9068, 93.7273], "type": "Rail / Road Junction"},
    {"name": "Dibrugarh", "district_id": "node_dibrugarh", "state": "Assam", "coordinates": [27.4728, 94.9120], "type": "Brahmaputra Port Hub"},
    {"name": "Jorhat", "district_id": "node_jorhat", "state": "Assam", "coordinates": [26.7509, 94.2037], "type": "Arterial Junction"},
    {"name": "Tezpur", "district_id": "node_tezpur", "state": "Assam", "coordinates": [26.6528, 92.7926], "type": "North Bank Hub"},
    {"name": "Bomdila", "district_id": "node_bomdila", "state": "Arunachal Pradesh", "coordinates": [27.2645, 92.4159], "type": "Mountain Sector"},
    {"name": "Churachandpur", "district_id": "node_churachandpur", "state": "Manipur", "coordinates": [24.3333, 93.6833], "type": "Southern Sector"},
    {"name": "Lunglei", "district_id": "node_lunglei", "state": "Mizoram", "coordinates": [22.8671, 92.7656], "type": "Southern Sector"},
    {"name": "Saraighat Bridge", "district_id": "node_guwahati", "state": "Assam", "coordinates": [26.1728, 91.6845], "type": "Critical Bridge Corridor"},
    {"name": "Bogibeel Bridge", "district_id": "node_dibrugarh", "state": "Assam", "coordinates": [27.3986, 94.8519], "type": "Critical Bridge Corridor"},
    {"name": "Dhola-Sadiya Bridge", "district_id": "node_tinsukia", "state": "Assam", "coordinates": [27.7942, 95.6669], "type": "Longest River Bridge"}
]

class SmartRouteEngine:
    """
    Multi-Factor Resilient Routing Engine for North Eastern Region Logistics.
    Combines Distance, Travel Time, Landslide Probability, Flood Hazard, and Active Blockades.
    """

    def __init__(self):
        self.nodes_dict = {n["id"]: n for n in NER_DISTRICT_NODES}
        self.edges_dict = {e["id"]: e for e in NER_ROAD_EDGES}
        self.build_graph()

    def build_graph(self):
        self.G_distance = nx.Graph()
        self.G_resilient = nx.Graph()

        for node_id, node_data in self.nodes_dict.items():
            self.G_distance.add_node(node_id, **node_data)
            self.G_resilient.add_node(node_id, **node_data)

        # Ingest dynamic edge states if fleet_manager is available
        edges_source = self.edges_dict
        try:
            from app.services.fleet_tracker import fleet_manager
            if hasattr(fleet_manager, 'edges_state') and fleet_manager.edges_state:
                edges_source = {e["id"]: e for e in fleet_manager.edges_state}
        except Exception:
            pass

        for edge_id, edge in edges_source.items():
            u, v = edge["source"], edge["target"]
            dist = edge["distance_km"]
            speed = max(20.0, edge["avg_speed_kmh"])
            travel_time_hours = dist / speed

            # Simple shortest distance graph
            self.G_distance.add_edge(u, v, edge_id=edge_id, weight=dist, travel_time=travel_time_hours, edge_data=edge)

            # AI Multi-factor Resilient Cost Function
            ls_risk = edge.get("landslide_risk", 10.0) / 100.0
            fl_risk = edge.get("flood_risk", 5.0) / 100.0
            rain_factor = min(1.0, edge.get("rainfall_mm", 10.0) / 100.0)

            status_penalty = 1.0
            if edge.get("status") == "blocked":
                status_penalty = 99999.0
            elif edge.get("status") == "critical":
                status_penalty = 15.0
            elif edge.get("status") == "warning":
                status_penalty = 2.5

            resilient_cost = dist * (1.0 + 2.0 * ls_risk + 1.5 * fl_risk + 0.8 * rain_factor) * status_penalty
            self.G_resilient.add_edge(u, v, edge_id=edge_id, weight=resilient_cost, travel_time=travel_time_hours, edge_data=edge)

    def search_places(self, query: str) -> List[Dict[str, Any]]:
        """Search North East places, towns, highways, and logistics hubs"""
        if not query or len(query.strip()) < 2:
            return NER_PLACES_INDEX[:8]

        q = query.lower().strip()
        matches = [
            p for p in NER_PLACES_INDEX
            if q in p["name"].lower() or q in p["state"].lower() or q in p.get("type", "").lower()
        ]
        if not matches:
            # Fallback search in districts
            for n in NER_DISTRICT_NODES:
                if q in n["name"].lower() or q in n["state"].lower():
                    matches.append({
                        "name": n["name"],
                        "district_id": n["id"],
                        "state": n["state"],
                        "coordinates": n["coordinates"],
                        "type": "District"
                    })
        return matches[:8]

    def optimize_route(self, req: RouteRequest) -> RouteOptimizationResponse:
        # Re-sync graph with active edge conditions
        self.build_graph()

        src = req.source_id
        dst = req.destination_id

        # Match name or ID
        if src not in self.nodes_dict:
            src_node = next((n for n in NER_DISTRICT_NODES if src.lower() in n["name"].lower() or src.lower() in n["id"].lower()), NER_DISTRICT_NODES[0])
            src = src_node["id"]
        if dst not in self.nodes_dict:
            dst_node = next((n for n in NER_DISTRICT_NODES if dst.lower() in n["name"].lower() or dst.lower() in n["id"].lower()), NER_DISTRICT_NODES[2])
            dst = dst_node["id"]

        src_name = self.nodes_dict[src]["name"]
        dst_name = self.nodes_dict[dst]["name"]

        # 1. Primary Shortest Route (Standard Highway)
        try:
            primary_path = nx.shortest_path(self.G_distance, source=src, target=dst, weight="weight")
            primary_plan = self._build_route_plan(
                path_nodes=primary_path,
                route_id="route_primary_direct",
                is_primary=True,
                title="Route A: Fastest Highway (Shortest Distance)"
            )
        except Exception:
            primary_plan = None

        # 2. Resilient AI Route (Avoiding high hazards & blockages)
        G_active = self.G_resilient.copy()
        for node_id in req.custom_avoid_nodes:
            if G_active.has_node(node_id):
                G_active.remove_node(node_id)
        for edge_id in req.custom_avoid_edges:
            for u, v, data in list(G_active.edges(data=True)):
                if data.get("edge_id") == edge_id:
                    G_active.remove_edge(u, v)

        try:
            resilient_path = nx.shortest_path(G_active, source=src, target=dst, weight="weight")
            resilient_plan = self._build_route_plan(
                path_nodes=resilient_path,
                route_id="route_ai_resilient",
                is_primary=False,
                title="Route B: Recommended Safe Corridor (Risk-Mitigated Bypass)"
            )
        except Exception:
            resilient_plan = primary_plan

        # Metrics
        if primary_plan and resilient_plan:
            time_diff_min = int((resilient_plan.total_travel_time_hours - primary_plan.total_travel_time_hours) * 60)
            risk_diff = max(0.0, round(primary_plan.aggregate_risk_score - resilient_plan.aggregate_risk_score, 1))
        else:
            time_diff_min = 0
            risk_diff = 0.0

        # 3. Secondary Contingency Detour
        contingency_plan = None
        if resilient_plan and len(resilient_plan.segments) > 1:
            try:
                paths = list(nx.shortest_simple_paths(G_active, source=src, target=dst, weight="weight"))
                if len(paths) > 1:
                    alt_path = paths[1]
                    contingency_plan = self._build_route_plan(
                        path_nodes=alt_path,
                        route_id="route_contingency_secondary",
                        is_primary=False,
                        title="Route C: Secondary Strategic Reserve Corridor"
                    )
            except Exception:
                pass

        return RouteOptimizationResponse(
            source_name=src_name,
            destination_name=dst_name,
            recommended_route=resilient_plan or primary_plan,
            alternative_route=primary_plan if primary_plan != resilient_plan else contingency_plan,
            contingency_detour=contingency_plan,
            delay_delta_minutes=time_diff_min,
            risk_reduction_pct=risk_diff
        )

    def _build_route_plan(self, path_nodes: List[str], route_id: str, is_primary: bool, title: str) -> RoutePlan:
        total_dist = 0.0
        total_time_h = 0.0
        weighted_risk_sum = 0.0
        ls_exposure_km = 0.0
        flood_exposure_km = 0.0
        segments: List[RouteSegment] = []
        path_coords: List[List[float]] = []

        src_coords = self.nodes_dict[path_nodes[0]]["coordinates"]
        path_coords.append(src_coords)

        for i in range(len(path_nodes) - 1):
            u = path_nodes[i]
            v = path_nodes[i+1]
            edge_data = self.G_distance.get_edge_data(u, v)["edge_data"]

            d = edge_data["distance_km"]
            speed = max(20.0, edge_data["avg_speed_kmh"])
            t_min = (d / speed) * 60.0
            ls_r = edge_data.get("landslide_risk", 10.0)
            fl_r = edge_data.get("flood_risk", 5.0)

            total_dist += d
            total_time_h += (t_min / 60.0)

            seg_risk = max(ls_r, fl_r * 0.8)
            weighted_risk_sum += (seg_risk * d)

            if ls_r > 40.0:
                ls_exposure_km += d
            if fl_r > 30.0:
                flood_exposure_km += d

            u_name = self.nodes_dict[u]["name"].split(" (")[0]
            v_name = self.nodes_dict[v]["name"].split(" (")[0]

            instruction = f"Proceed on {edge_data['highway_code']} from {u_name} towards {v_name} ({d} km, ~{int(t_min)} mins)."
            if edge_data.get("status") == "warning":
                instruction += f" ⚠️ CAUTION: {edge_data.get('closure_reason', 'Hazard detected')}"
            elif edge_data.get("status") == "blocked":
                instruction += f" 🚫 BLOCKED: {edge_data.get('closure_reason', 'Road severed')}"

            poly = edge_data.get("coordinates_polyline", [self.nodes_dict[u]["coordinates"], self.nodes_dict[v]["coordinates"]])
            for pt in poly:
                if not path_coords or path_coords[-1] != pt:
                    path_coords.append(pt)

            segments.append(RouteSegment(
                edge_id=edge_data["id"],
                name=f"{edge_data['highway_code']} ({u_name} → {v_name})",
                distance_km=round(d, 1),
                travel_time_min=round(t_min, 1),
                landslide_risk=round(ls_r, 1),
                flood_risk=round(fl_r, 1),
                status=edge_data.get("status", "open"),
                instructions=instruction,
                coordinates=poly
            ))

        agg_risk = round(weighted_risk_sum / max(1.0, total_dist), 1) if total_dist > 0 else 0.0

        if agg_risk < 25.0:
            weather_adv = "Optimal Transit Weather: Roads dry and stable across corridor. Green route active."
        elif agg_risk < 55.0:
            weather_adv = "Moderate Caution: Light-to-medium rain showers in hill segments. Reduce speed on hairpins."
        else:
            weather_adv = "Severe Warning: Heavy precipitation & saturated slopes. Slopes prone to sliding. Safe bypass recommended."

        summary = f"{title}: Total {round(total_dist, 1)} km ({round(total_time_h, 1)} hrs, Risk: {agg_risk}%)."

        return RoutePlan(
            route_id=route_id,
            is_primary=is_primary,
            title=title,
            total_distance_km=round(total_dist, 1),
            total_travel_time_hours=round(total_time_h, 1),
            aggregate_risk_score=agg_risk,
            landslide_exposure_km=round(ls_exposure_km, 1),
            flood_exposure_km=round(flood_exposure_km, 1),
            segments=segments,
            path_coordinates=path_coords,
            summary=summary,
            weather_advisory=weather_adv
        )

smart_route_engine = SmartRouteEngine()
