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
import json
import urllib.request
import urllib.parse
import networkx as nx
from typing import Dict, Any, List, Optional, Tuple
from app.services.digital_twin_data import NER_DISTRICT_NODES, NER_ROAD_EDGES, NER_BRIDGES
from app.models.schemas import (
    RouteRequest,
    RouteOptimizationResponse,
    RoutePlan,
    RouteSegment,
    LandslidePredictionRequest
)
from app.services.ai_predictor import AIPredictionEngine

# Places database dynamically aggregated across all 84 district hubs, 14 bridges, passes & border gates
NER_PLACES_INDEX: List[Dict[str, Any]] = [
    {
        "name": n["name"],
        "district_id": n["id"],
        "state": n["state"],
        "coordinates": n["coordinates"],
        "type": "Strategic District Hub"
    }
    for n in NER_DISTRICT_NODES
] + [
    {
        "name": b["name"],
        "district_id": b["id"],
        "state": b["state"],
        "coordinates": b["coordinates"],
        "type": "Critical River Bridge"
    }
    for b in NER_BRIDGES
] + [
    {"name": "Sela Pass (13,700 ft) & Tunnel", "district_id": "node_tawang", "state": "Arunachal Pradesh", "coordinates": [27.5055, 92.1037], "type": "High Altitude Pass"},
    {"name": "Nathu La Pass (14,140 ft Silk Pass)", "district_id": "node_nathula", "state": "Sikkim", "coordinates": [27.3865, 88.8310], "type": "International Border Pass"},
    {"name": "Moreh Border Gate (AH-1 Myanmar)", "district_id": "node_moreh", "state": "Manipur", "coordinates": [24.2500, 94.3000], "type": "Asian Highway Border Terminal"},
    {"name": "Dawki Border Trade Gate (to Bangladesh)", "district_id": "node_dawki", "state": "Meghalaya", "coordinates": [25.1950, 92.0190], "type": "International Trade Gate"},
    {"name": "Maitri Setu Feni River Gateway", "district_id": "node_sabroom", "state": "Tripura", "coordinates": [23.0111, 91.7333], "type": "Seaport Access Corridor"},
    {"name": "Jatinga Valley Hazard Sector", "district_id": "node_haflong", "state": "Assam", "coordinates": [25.1200, 93.0300], "type": "Mountain Debris Sector"},
    {"name": "29th Mile Teesta Gorge Sector", "district_id": "node_gangtok", "state": "Sikkim", "coordinates": [27.0500, 88.4800], "type": "Active Debris Zone"},
    {"name": "Balemu - Kalaktang Bypass", "district_id": "node_bomdila", "state": "Arunachal Pradesh", "coordinates": [27.0800, 92.1800], "type": "Disaster Alternate Pass"},
    {"name": "Phesama Sinking Sector", "district_id": "node_kohima", "state": "Nagaland", "coordinates": [25.6200, 94.1000], "type": "Geological Sinking Sector"}
]

class SmartRouteEngine:
    """
    Multi-Factor Resilient Routing Engine for North Eastern Region Logistics.
    Combines Distance, Travel Time, Real OSRM Navigation, Landslide Probability,
    Flood Hazard, and Active Blockades.
    """

    def __init__(self):
        self.nodes_dict = {n["id"]: n for n in NER_DISTRICT_NODES}
        self.edges_dict = {e["id"]: e for e in NER_ROAD_EDGES}
        self._osrm_cache: Dict[str, Any] = {}
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
        """Search North East places, towns, highways, passes, and open geocoding"""
        if not query or len(query.strip()) < 2:
            return NER_PLACES_INDEX[:10]

        q = query.lower().strip()
        matches = [
            p for p in NER_PLACES_INDEX
            if q in p["name"].lower() or q in p["state"].lower() or q in p.get("type", "").lower()
        ]

        # Supplement with district nodes index
        if len(matches) < 5:
            existing_ids = {m.get("district_id") for m in matches if m.get("district_id")}
            for n in NER_DISTRICT_NODES:
                if (q in n["name"].lower() or q in n["state"].lower()) and n["id"] not in existing_ids:
                    matches.append({
                        "name": n["name"],
                        "district_id": n["id"],
                        "state": n["state"],
                        "coordinates": n["coordinates"],
                        "type": "District Hub"
                    })
                    existing_ids.add(n["id"])

        # Try OpenStreetMap Nominatim live geocoding fallback only if no matches found
        if len(matches) == 0:
            try:
                encoded_q = urllib.parse.quote(f"{query}, North East India")
                url = f"https://nominatim.openstreetmap.org/search?q={encoded_q}&format=json&countrycodes=in&limit=4"
                req = urllib.request.Request(url, headers={'User-Agent': 'NERA-Resilience-Engine/2.0'})
                with urllib.request.urlopen(req, timeout=1.5) as response:
                    if response.status == 200:
                        geo_data = json.loads(response.read().decode())
                        for item in geo_data:
                            lat = float(item["lat"])
                            lon = float(item["lon"])
                            # Check if roughly in North East bounding box (21 to 30 N, 88 to 97.5 E)
                            if 21.0 <= lat <= 30.0 and 88.0 <= lon <= 97.5:
                                matches.append({
                                    "name": item.get("display_name", "").split(",")[0],
                                    "district_id": self._find_closest_district(lat, lon),
                                    "state": "North East India",
                                    "coordinates": [lat, lon],
                                    "type": "OSM Geocoded Place"
                                })
            except Exception:
                pass

        return matches[:12]

    def _find_closest_district(self, lat: float, lng: float) -> str:
        """Finds nearest Digital Twin district ID to any arbitrary coordinates"""
        best_id = "node_guwahati"
        best_dist = float("inf")
        for node in NER_DISTRICT_NODES:
            n_lat, n_lng = node["coordinates"]
            d = math.hypot(n_lat - lat, n_lng - lng)
            if d < best_dist:
                best_dist = d
                best_id = node["id"]
        return best_id

    def fetch_osrm_real_route(self, src_coords: List[float], dst_coords: List[float], timeout_sec: float = 0.8) -> Optional[Dict[str, Any]]:
        """
        Queries free public OpenStreetMap OSRM Routing API (Zero API key needed)
        Returns real road polyline geometry and turn-by-turn guidance.
        """
        cache_key = f"{round(src_coords[0], 3)},{round(src_coords[1], 3)};{round(dst_coords[0], 3)},{round(dst_coords[1], 3)}"
        if cache_key in self._osrm_cache:
            return self._osrm_cache[cache_key]

        try:
            # OSRM expects: /route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson&steps=true
            url = f"https://router.project-osrm.org/route/v1/driving/{src_coords[1]},{src_coords[0]};{dst_coords[1]},{dst_coords[0]}?overview=full&geometries=geojson&steps=true"
            req = urllib.request.Request(url, headers={'User-Agent': 'NERA-Logistics-Platform/2.0'})
            with urllib.request.urlopen(req, timeout=timeout_sec) as res:
                if res.status == 200:
                    data = json.loads(res.read().decode())
                    if data.get("code") == "Ok" and len(data.get("routes", [])) > 0:
                        route = data["routes"][0]
                        # GeoJSON coordinates are [lon, lat] -> convert to Leaflet [lat, lon]
                        geojson_coords = route["geometry"]["coordinates"]
                        leaflet_coords = [[pt[1], pt[0]] for pt in geojson_coords]
                        
                        steps = []
                        for leg in route.get("legs", []):
                            for step in leg.get("steps", []):
                                man = step.get("maneuver", {})
                                step_name = step.get("name", "Highway")
                                if not step_name:
                                    step_name = "Road Corridor"
                                instruction = f"{man.get('type', 'Proceed').capitalize()} on {step_name} ({round(step.get('distance', 0)/1000.0, 1)} km)"
                                steps.append({
                                    "name": step_name,
                                    "distance_km": round(step.get("distance", 0) / 1000.0, 1),
                                    "duration_min": round(step.get("duration", 0) / 60.0, 1),
                                    "instructions": instruction,
                                    "coordinates": [[pt[1], pt[0]] for pt in step.get("geometry", {}).get("coordinates", [])] if isinstance(step.get("geometry"), dict) else []
                                })

                        result = {
                            "distance_km": round(route["distance"] / 1000.0, 1),
                            "duration_hours": round(route["duration"] / 3600.0, 1),
                            "coordinates": leaflet_coords,
                            "steps": steps
                        }
                        self._osrm_cache[cache_key] = result
                        return result
        except Exception:
            pass
        return None

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
        src_coords = self.nodes_dict[src]["coordinates"]
        dst_coords = self.nodes_dict[dst]["coordinates"]

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

        # 2. Resilient AI Route (Strictly avoiding high hazards & blockages)
        G_active = self.G_resilient.copy()
        for node_id in req.custom_avoid_nodes:
            if G_active.has_node(node_id):
                G_active.remove_node(node_id)
        for edge_id in req.custom_avoid_edges:
            for u, v, data in list(G_active.edges(data=True)):
                if data.get("edge_id") == edge_id:
                    G_active.remove_edge(u, v)

        # Enforce Zero Red-Zone Safe Corridors when avoid_high_risk is enabled
        if req.avoid_high_risk:
            G_safe = G_active.copy()
            for u, v, data in list(G_safe.edges(data=True)):
                e_data = data.get("edge_data", {})
                if e_data.get("status") != "open" or e_data.get("landslide_risk", 0) > 50.0 or e_data.get("flood_risk", 0) > 50.0:
                    G_safe.remove_edge(u, v)

            if nx.has_path(G_safe, source=src, target=dst):
                G_search = G_safe
            else:
                # Fallback with massive penalty on red zones (only used if terminus pass is unavoidable)
                G_search = G_active
                for u, v, data in G_search.edges(data=True):
                    e_data = data.get("edge_data", {})
                    if e_data.get("status") != "open" or e_data.get("landslide_risk", 0) > 50.0 or e_data.get("flood_risk", 0) > 50.0:
                        data["weight"] = data["weight"] * 10000.0
        else:
            G_search = G_active

        try:
            resilient_path = nx.shortest_path(G_search, source=src, target=dst, weight="weight")
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
                paths = []
                for p in nx.shortest_simple_paths(G_search, source=src, target=dst, weight="weight"):
                    paths.append(p)
                    if len(paths) >= 2:
                        break
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

        rec_route = resilient_plan or primary_plan
        alt_route = primary_plan if primary_plan != resilient_plan else contingency_plan

        primary_red = primary_plan.red_zone_count if primary_plan else 0
        safe_red = rec_route.red_zone_count if rec_route else 0
        avoided_count = max(0, primary_red - safe_red)

        return RouteOptimizationResponse(
            source_name=src_name,
            destination_name=dst_name,
            recommended_route=rec_route,
            alternative_route=alt_route,
            contingency_detour=contingency_plan,
            delay_delta_minutes=time_diff_min,
            risk_reduction_pct=risk_diff,
            red_zones_avoided=avoided_count,
            ai_risk_breakdown=rec_route.ai_risk_breakdown if rec_route else None
        )

    def _build_route_plan(self, path_nodes: List[str], route_id: str, is_primary: bool, title: str) -> RoutePlan:
        total_dist = 0.0
        total_time_h = 0.0
        weighted_risk_sum = 0.0
        ls_exposure_km = 0.0
        flood_exposure_km = 0.0
        weighted_rainfall = 0.0
        max_slope = 8.0
        weighted_soil = 0.0
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
            rain_mm = edge_data.get("rainfall_mm", 15.0)
            slope_deg = edge_data.get("slope_deg", 12.0)
            soil_sat = min(98.0, 30.0 + rain_mm * 0.7)

            total_dist += d
            total_time_h += (t_min / 60.0)
            weighted_rainfall += (rain_mm * d)
            weighted_soil += (soil_sat * d)
            if slope_deg > max_slope:
                max_slope = slope_deg

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

            poly = list(edge_data.get("coordinates_polyline", [self.nodes_dict[u]["coordinates"], self.nodes_dict[v]["coordinates"]]))
            if len(poly) >= 2:
                # Ensure polyline connects sequentially from u -> v
                u_coord = self.nodes_dict[u]["coordinates"]
                v_coord = self.nodes_dict[v]["coordinates"]
                d_start_u = (poly[0][0] - u_coord[0])**2 + (poly[0][1] - u_coord[1])**2
                d_start_v = (poly[0][0] - v_coord[0])**2 + (poly[0][1] - v_coord[1])**2
                if d_start_v < d_start_u:
                    poly = list(reversed(poly))

            for pt in poly:
                if not path_coords or (path_coords[-1][0] != pt[0] or path_coords[-1][1] != pt[1]):
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

        avg_rainfall = round(weighted_rainfall / max(1.0, total_dist), 1) if total_dist > 0 else 18.0
        avg_soil = round(weighted_soil / max(1.0, total_dist), 1) if total_dist > 0 else 45.0
        history_cnt = max(1, int(ls_exposure_km / 12.0))

        # Scientific derivation of Route Risk Score using empirical AIPredictionEngine
        ai_breakdown = None
        try:
            pred_req = LandslidePredictionRequest(
                rainfall_mm=avg_rainfall,
                slope_degrees=max_slope,
                soil_saturation_pct=avg_soil,
                historical_landslide_count=history_cnt,
                seismic_zone=5,
                vegetation_index=0.62
            )
            pred_res = AIPredictionEngine.predict_landslide(pred_req)
            agg_risk = round(pred_res.landslide_risk_pct, 1)

            ai_breakdown = {
                "model_name": "NERA Physics-Informed Geohazard Ensemble (IMD / GSI Calibrated)",
                "model_formula": "CRI = 0.35 × R(Rainfall) + 0.30 × S(Slope) + 0.20 × M(Soil Moisture) + 0.15 × H(Historical/Seismic) - V_attenuation",
                "composite_risk_score": agg_risk,
                "landslide_risk_pct": agg_risk,
                "risk_level": pred_res.risk_level,
                "action_protocol": pred_res.action_protocol,
                "factors": [
                    {
                        "name": f.name,
                        "contribution_pct": f.contribution_pct,
                        "description": f.description
                    }
                    for f in pred_res.factor_breakdown
                ],
                "environmental_telemetry": {
                    "avg_rainfall_mm": avg_rainfall,
                    "max_slope_deg": max_slope,
                    "soil_moisture_pct": avg_soil,
                    "seismic_zone": "Zone V (Severe Himalayan Fault Line)",
                    "hazard_exposure_km": round(ls_exposure_km + flood_exposure_km, 1)
                }
            }
        except Exception:
            agg_risk = round(weighted_risk_sum / max(1.0, total_dist), 1) if total_dist > 0 else 0.0

        if agg_risk < 25.0:
            weather_adv = "Optimal Transit Weather: Roads dry and stable across corridor. Green route active."
        elif agg_risk < 55.0:
            weather_adv = "Moderate Caution: Light-to-medium rain showers in hill segments. Reduce speed on hairpins."
        else:
            weather_adv = "Severe Warning: Heavy precipitation & saturated slopes. Slopes prone to sliding. Safe bypass recommended."

        summary = f"{title}: Total {round(total_dist, 1)} km ({round(total_time_h, 1)} hrs, AI Risk Score: {agg_risk}%)."

        red_count = sum(1 for s in segments if s.landslide_risk > 50.0 or s.flood_risk > 50.0 or s.status != "open")

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
            weather_advisory=weather_adv,
            red_zone_count=red_count,
            ai_risk_breakdown=ai_breakdown
        )

smart_route_engine = SmartRouteEngine()
