"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Module 2 & 9: Multi-Factor Resilient Routing & Safe-Corridor Engine

Features:
- Dual Graph Network Architecture: Physical Distance Graph vs Hazard Cost Graph
- Dynamic Dijkstra & Yen's K-Shortest Simple Paths Algorithm
- Simultaneous 3-Way Corridor Comparison: Primary Highway vs AI Safe Bypass vs Detour
- Polyline Coordinate Interpolation & Step-by-Step Navigation Advisories
"""
import networkx as nx
from typing import Dict, Any, List, Optional, Tuple
from app.services.digital_twin_data import NER_DISTRICT_NODES, NER_ROAD_EDGES
from app.models.schemas import (
    RouteRequest,
    RouteOptimizationResponse,
    RoutePlan,
    RouteSegment
)

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

        for edge_id, edge in self.edges_dict.items():
            u, v = edge["source"], edge["target"]
            dist = edge["distance_km"]
            speed = max(20.0, edge["avg_speed_kmh"])
            travel_time_hours = dist / speed

            # Simple shortest distance graph
            self.G_distance.add_edge(u, v, edge_id=edge_id, weight=dist, travel_time=travel_time_hours, edge_data=edge)

            # AI Multi-factor Resilient Cost Function
            # Score = Distance * [1.0 + w_ls * LandslideRisk + w_fl * FloodRisk + w_rain * RainPenalty + BlockadePenalty]
            ls_risk = edge["landslide_risk"] / 100.0
            fl_risk = edge["flood_risk"] / 100.0
            rain_factor = min(1.0, edge["rainfall_mm"] / 100.0)

            status_penalty = 1.0
            if edge["status"] == "blocked":
                status_penalty = 99999.0
            elif edge["status"] == "warning":
                status_penalty = 2.2
            elif edge["status"] == "critical":
                status_penalty = 10.0

            resilient_cost = dist * (1.0 + 1.8 * ls_risk + 1.2 * fl_risk + 0.6 * rain_factor) * status_penalty

            self.G_resilient.add_edge(u, v, edge_id=edge_id, weight=resilient_cost, travel_time=travel_time_hours, edge_data=edge)

    def optimize_route(self, req: RouteRequest) -> RouteOptimizationResponse:
        src = req.source_id
        dst = req.destination_id

        if src not in self.nodes_dict or dst not in self.nodes_dict:
            # Fallback or error
            src_node = next((n for n in NER_DISTRICT_NODES if src in n["name"].lower() or src in n["id"]), NER_DISTRICT_NODES[0])
            dst_node = next((n for n in NER_DISTRICT_NODES if dst in n["name"].lower() or dst in n["id"]), NER_DISTRICT_NODES[2])
            src = src_node["id"]
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
                title="Primary National Highway Route (Shortest Distance)"
            )
        except Exception:
            primary_plan = None

        # 2. Resilient AI Route (Avoiding high hazards & blockages)
        # Create a dynamic graph respecting custom avoid nodes/edges
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
                title="AI Safe-Corridor Route (Risk-Optimized Bypass)"
            )
        except Exception:
            resilient_plan = primary_plan

        # Calculate metrics
        if primary_plan and resilient_plan:
            time_diff_min = int((resilient_plan.total_travel_time_hours - primary_plan.total_travel_time_hours) * 60)
            risk_diff = max(0.0, round(primary_plan.aggregate_risk_score - resilient_plan.aggregate_risk_score, 1))
        else:
            time_diff_min = 0
            risk_diff = 0.0

        # Create alternative contingency route if available
        contingency_plan = None
        if resilient_plan and len(resilient_plan.segments) > 1:
            # Try finding 2nd k-shortest path
            try:
                paths = list(nx.shortest_simple_paths(G_active, source=src, target=dst, weight="weight"))
                if len(paths) > 1:
                    alt_path = paths[1]
                    contingency_plan = self._build_route_plan(
                        path_nodes=alt_path,
                        route_id="route_contingency_secondary",
                        is_primary=False,
                        title="Secondary Strategic Reserve Corridor"
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

        # Add origin coordinate
        src_coords = self.nodes_dict[path_nodes[0]]["coordinates"]
        path_coords.append(src_coords)

        for i in range(len(path_nodes) - 1):
            u = path_nodes[i]
            v = path_nodes[i+1]
            edge_data = self.G_distance.get_edge_data(u, v)["edge_data"]

            d = edge_data["distance_km"]
            speed = max(20.0, edge_data["avg_speed_kmh"])
            t_min = (d / speed) * 60.0
            ls_r = edge_data["landslide_risk"]
            fl_r = edge_data["flood_risk"]

            total_dist += d
            total_time_h += (t_min / 60.0)

            # Combined risk
            seg_risk = max(ls_r, fl_r * 0.8)
            weighted_risk_sum += (seg_risk * d)

            if ls_r > 40.0:
                ls_exposure_km += d
            if fl_r > 30.0:
                flood_exposure_km += d

            u_name = self.nodes_dict[u]["name"].split(" (")[0]
            v_name = self.nodes_dict[v]["name"].split(" (")[0]

            instruction = f"Proceed on {edge_data['highway_code']} from {u_name} towards {v_name} ({d} km, ~{int(t_min)} mins)."
            if edge_data["status"] == "warning":
                instruction += f" ⚠️ CAUTION: {edge_data.get('closure_reason', 'Hazard detected')}"

            # Append polyline points
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
                status=edge_data["status"],
                instructions=instruction,
                coordinates=poly
            ))

        agg_risk = round(weighted_risk_sum / max(1.0, total_dist), 1) if total_dist > 0 else 0.0

        if agg_risk < 20.0:
            weather_adv = "Optimal Transit Weather: Roads dry and stable across corridor."
        elif agg_risk < 50.0:
            weather_adv = "Moderate Caution: Light-to-medium rain showers in hill segments. Reduce speed on hairpins."
        else:
            weather_adv = "Severe Warning: Heavy precipitation & saturated slopes. Continuous convoy satellite tracking advised."

        summary = f"{title}: Total {round(total_dist, 1)} km across {len(segments)} highway legs, Estimated Time: {round(total_time_h, 1)} Hours (Risk Index: {agg_risk}/100)."

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
