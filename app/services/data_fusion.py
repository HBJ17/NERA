"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Module 14: 4-Stream Multi-Source Data Fusion Engine

Fuses:
1. Weather Radar & Precipitation Telemetry
2. Government Infrastructure & PWD Status
3. Real-Time Vehicle GPS Speeds & Convoy Delays
4. Crowdsourced & Official Verified Field Reports
"""
from typing import Dict, List, Any
from app.services.weather_engine import weather_engine
from app.services.fleet_tracker import fleet_manager
from app.services.digital_twin_data import NER_ROAD_EDGES, NER_DISTRICT_NODES

class DataFusionEngine:
    """
    4-Stream Multi-Source Geospatial Fusion Engine for Disaster & Supply Resilience.
    Synthesizes composite risk indices (CRI) by merging physical sensor, crowdsourced, and institutional telemetry.
    """

    def compute_composite_risk_matrix(self) -> Dict[str, Any]:
        weather_stations = {s["district_id"]: s for s in weather_engine.get_all_stations()}
        edges = fleet_manager.edges_state
        fleet = fleet_manager.get_fleet()
        reports = fleet_manager.get_field_reports()

        fused_corridors = []
        for e in edges:
            src, tgt = e["source"], e["target"]
            w_src = weather_stations.get(src, {})
            w_tgt = weather_stations.get(tgt, {})
            
            # Stream 1: Weather Precipitation Factor (0-100)
            avg_rain = (w_src.get("rainfall_24h_mm", 20.0) + w_tgt.get("rainfall_24h_mm", 20.0)) / 2.0
            weather_score = min(100.0, avg_rain * 0.75)

            # Stream 2: PWD Infrastructure Status (0-100)
            infra_score = 10.0
            if e.get("status") == "blocked":
                infra_score = 100.0
            elif e.get("status") == "warning":
                infra_score = 60.0

            # Stream 3: GPS Telemetry & Vehicle Delays
            hw_code = e["highway_code"]
            active_vehicles_on_corridor = [v for v in fleet if v.get("assigned_route_id") == e["id"] or hw_code.replace("-","") in v.get("destination", "").replace("-","")]
            delay_minutes = sum(v.get("delay_minutes", 0) for v in active_vehicles_on_corridor)
            gps_score = min(100.0, delay_minutes * 1.5 + (20.0 if any(v.get("status") == "delayed" for v in active_vehicles_on_corridor) else 0.0))

            # Stream 4: Field Reports (Active / Verified)
            relevant_reports = [
                r for r in reports
                if hw_code.replace("-","") in r.get("nearest_highway", "").replace("-","") and r.get("verification_status") != "REJECTED"
            ]
            field_score = min(100.0, len(relevant_reports) * 35.0)

            # Weighted 4-Stream Composite Risk Index (CRI)
            # Weather: 30%, PWD/Infra: 30%, GPS Delay: 20%, Field Reports: 20%
            cri = round(0.30 * weather_score + 0.30 * infra_score + 0.20 * gps_score + 0.20 * field_score, 1)

            tier = "LOW" if cri < 30 else ("MODERATE" if cri < 60 else ("HIGH" if cri < 85 else "CRITICAL_HAZARD"))

            fused_corridors.append({
                "edge_id": e["id"],
                "highway_code": e["highway_code"],
                "source": src,
                "target": tgt,
                "composite_risk_score": cri,
                "risk_tier": tier,
                "streams_breakdown": {
                    "weather_stream_pct": round(weather_score, 1),
                    "infrastructure_stream_pct": round(infra_score, 1),
                    "gps_telemetry_stream_pct": round(gps_score, 1),
                    "field_reports_stream_pct": round(field_score, 1)
                }
            })

        return {
            "fusion_status": "SYNCHRONIZED",
            "active_streams_count": 4,
            "stream_sources": [
                "Stream 1: Doppler Radar & IMD Precipitation",
                "Stream 2: PWD Highway Embankment Health",
                "Stream 3: Satellite AIS/GPS Convoy Kinetic Telemetry",
                "Stream 4: Crowdsourced Ground Truth Ingestion"
            ],
            "fused_corridors_count": len(fused_corridors),
            "corridors": fused_corridors
        }

data_fusion_engine = DataFusionEngine()
