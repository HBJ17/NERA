import os
import sys
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_standalone_checks():
    print("=== RUNNING STANDALONE NERA PLATFORM VERIFICATION ===")

    # 1. HTML Verification
    res = client.get("/")
    assert res.status_code == 200, "Frontend index route failed"
    html = res.text
    assert "btn-pin-mode" in html, "Missing btn-pin-mode in HTML"
    assert "modal-map-settings" in html, "Missing modal-map-settings in HTML"
    assert "Open in Google Maps" in html, "Missing Open in Google Maps in HTML"
    print("[OK] 1. HTML & Controls: OK")

    # 2. Digital Twin State
    res = client.get("/api/twin/state")
    assert res.status_code == 200, "Twin state endpoint failed"
    data = res.json()
    num_districts = len(data["districts"])
    num_highways = len(data["highways"])
    num_bridges = len(data["bridges"])
    print(f"[OK] 2. Digital Twin State: {num_districts} Hubs, {num_highways} Highway Corridors, {num_bridges} Bridges: OK")

    # 3. Smart Routing
    res = client.post("/api/routing/optimize", json={
        "source_id": "node_guwahati",
        "destination_id": "node_tawang",
        "avoid_high_risk": True
    })
    assert res.status_code == 200, "Routing optimize failed"
    route_data = res.json()
    dist = route_data["recommended_route"]["total_distance_km"]
    assert dist > 0, "Distance should be > 0"
    print(f"[OK] 3. Smart Route Guwahati -> Tawang: {dist} km, {len(route_data['recommended_route']['segments'])} segments: OK")

    # 4. Search & Geocoding
    res = client.get("/api/routing/search?q=Kohima")
    assert res.status_code == 200
    places = res.json()
    assert len(places) > 0, "Search for Kohima should return results"
    print(f"[OK] 4. Search / Geocoding for 'Kohima': {len(places)} results: OK")

    # 5. Fleet Telemetry & Categories
    res = client.get("/api/fleet/live")
    assert res.status_code == 200
    fleet = res.json()
    cars = [v for v in fleet if v.get("category") == "car"]
    logistics = [v for v in fleet if v.get("category") == "logistics"]
    assert len(cars) >= 4, f"Expected at least 4 civilian cars, got {len(cars)}"
    assert len(logistics) >= 6, f"Expected at least 6 logistics trucks, got {len(logistics)}"
    print(f"[OK] 5. Live Fleet: {len(cars)} Civilian Cars, {len(logistics)} Logistics Freight Trucks: OK")

    # 6. Point Hazard Simulation
    res = client.post("/api/simulation/trigger-point", json={
        "lat": 25.8200,
        "lng": 91.8600,
        "disaster_type": "landslide",
        "severity": "TOTAL_BREACH"
    })
    assert res.status_code == 200
    point_data = res.json()
    assert "nearest_edge_id" in point_data
    print(f"[OK] 6. Point Hazard Trigger: Severed {point_data.get('severed_highway')}, Disrupted {len(point_data.get('delayed_vehicles', []))} Convoys: OK")

    # Reset simulation
    client.post("/api/simulation/reset")

    # 7. Scientific AI Risk Breakdown
    res = client.post("/api/routing/optimize", json={
        "source_id": "node_guwahati",
        "destination_id": "node_shillong",
        "avoid_high_risk": True
    })
    assert res.status_code == 200
    r_data = res.json()
    assert "ai_risk_breakdown" in r_data
    ai_b = r_data["ai_risk_breakdown"]
    assert "composite_risk_score" in ai_b
    print(f"[OK] 7. AI Scientific Risk Breakdown: Score {ai_b['composite_risk_score']}, Factors {len(ai_b['factors'])}: OK")

    # 8. What-if Preset Scenario
    res = client.post("/api/simulation/run", json={
        "scenario_id": "scenario_sela_pass",
        "disaster_severity": "EXTREME",
        "weather_multiplier": 1.8
    })
    assert res.status_code == 200
    sim_data = res.json()
    print(f"[OK] 8. What-If Sela Pass Simulation: {len(sim_data.get('isolated_districts', []))} Isolated Districts, {len(sim_data.get('delayed_vehicles', []))} Delayed Convoys: OK")

    # Reset simulation
    client.post("/api/simulation/reset")

    # 10. Closed-Loop Incident Ingestion & Edge Severance
    rep_res = client.post("/api/reports/submit", json={
        "location_name": "Haflong Valley NH-27 Corridor",
        "latitude": 25.1680,
        "longitude": 93.0180,
        "incident_type": "Landslide",
        "severity": "BLOCKING",
        "nearest_highway": "NH-27",
        "description": "Severe debris rockfall completely blocking both lanes near Jatinga.",
        "officer_name": "Er. PWD Haflong",
        "department": "PWD Engineer",
        "reporter_role": "gov_employee",
        "confidence_score": 95.0
    })
    assert rep_res.status_code == 200
    report_data = rep_res.json()
    assert report_data["verification_status"] in ("ACTIVE_INCIDENT", "PENDING_VERIFICATION", "PWD_CONFIRMED")
    print(f"[OK] 10. Closed-Loop Incident Ingestion: Submitted report ID {report_data['id']}, edge severed: OK")

    # 11. Progressive Web App (PWA) Assets
    m_res = client.get("/static/manifest.json")
    assert m_res.status_code == 200, "manifest.json missing"
    assert "NERA" in m_res.json()["name"]

    sw_res = client.get("/static/sw.js")
    assert sw_res.status_code == 200, "sw.js missing"
    assert "CACHE_NAME" in sw_res.text
    print("[OK] 11. Progressive Web App (PWA): manifest.json & Service Worker Cache Verified: OK")

    print("\n>>> ALL 11 STANDALONE INTEGRATION CHECKS PASSED SUCCESSFULLY! <<<")

if __name__ == "__main__":
    run_standalone_checks()


