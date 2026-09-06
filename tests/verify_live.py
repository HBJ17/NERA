import urllib.request
import json

def run_checks():
    # 1. HTML Verification
    with urllib.request.urlopen("http://127.0.0.1:8000/") as res:
        html = res.read().decode("utf-8")
        assert "btn-pin-mode" in html, "Missing btn-pin-mode in HTML"
        assert "modal-map-settings" in html, "Missing modal-map-settings in HTML"
        assert "Open in Google Maps" in html, "Missing Open in Google Maps in HTML"
        print("[OK] HTML & Controls: OK")

    # 2. Digital Twin State
    with urllib.request.urlopen("http://127.0.0.1:8000/api/twin/state") as res:
        data = json.loads(res.read().decode("utf-8"))
        num_districts = len(data["districts"])
        num_highways = len(data["highways"])
        num_bridges = len(data["bridges"])
        assert num_districts == 84, f"Expected 84 districts, got {num_districts}"
        assert num_highways == 119, f"Expected 119 highways, got {num_highways}"
        assert num_bridges == 14, f"Expected 14 bridges, got {num_bridges}"
        print(f"[OK] Digital Twin State: {num_districts} Hubs, {num_highways} Highway Corridors, {num_bridges} Bridges: OK")

    # 3. Smart Routing
    payload = json.dumps({
        "source_id": "node_guwahati",
        "destination_id": "node_tawang",
        "avoid_high_risk": True
    }).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/routing/optimize",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as res:
        route_data = json.loads(res.read().decode("utf-8"))
        dist = route_data["recommended_route"]["total_distance_km"]
        assert dist > 0, "Distance should be > 0"
        print(f"[OK] Route Guwahati -> Tawang: {dist} km, {len(route_data['recommended_route']['segments'])} segments: OK")

    # 4. Search & Geocoding
    with urllib.request.urlopen("http://127.0.0.1:8000/api/routing/search?q=Kohima") as res:
        places = json.loads(res.read().decode("utf-8"))
        assert len(places) > 0, "Search for Kohima should return results"
        print(f"[OK] Search / Geocoding for 'Kohima': {len(places)} results: OK")

    # 5. Fleet Telemetry & Categories (Cars vs Logistics)
    with urllib.request.urlopen("http://127.0.0.1:8000/api/fleet/live") as res:
        fleet = json.loads(res.read().decode("utf-8"))
        cars = [v for v in fleet if v.get("category") == "car"]
        logistics = [v for v in fleet if v.get("category") == "logistics"]
        assert len(cars) >= 4, f"Expected at least 4 civilian cars, got {len(cars)}"
        assert len(logistics) >= 6, f"Expected at least 6 logistics trucks, got {len(logistics)}"
        print(f"[OK] Live Fleet: {len(cars)} Blue Civilian Cars, {len(logistics)} Red Logistics Freight Trucks: OK")

    # 6. Point Hazard Simulation (Map click hazard trigger)
    point_payload = json.dumps({
        "lat": 25.8200,
        "lng": 91.8600,
        "disaster_type": "landslide",
        "severity": "TOTAL_BREACH"
    }).encode("utf-8")
    p_req = urllib.request.Request(
        "http://127.0.0.1:8000/api/simulation/trigger-point",
        data=point_payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(p_req) as res:
        hazard_data = json.loads(res.read().decode("utf-8"))
        assert hazard_data["status"] == "hazard_triggered"
        assert "severed_highway" in hazard_data
        print(f"[OK] Map Point Hazard Trigger: Severed {hazard_data['severed_highway']} at [25.82, 91.86]: OK")

    # 7. AI Scientific Risk Breakdown
    with urllib.request.urlopen(req) as res:
        route_data = json.loads(res.read().decode("utf-8"))
        ai_breakdown = route_data.get("ai_risk_breakdown")
        assert ai_breakdown is not None, "Missing ai_risk_breakdown in route response"
        assert "model_formula" in ai_breakdown
        assert len(ai_breakdown["factors"]) >= 3
        print(f"[OK] AI Scientific Geohazard Risk Model: Formula '{ai_breakdown['model_formula']}', Score {ai_breakdown['composite_risk_score']}%: OK")

    # Reset simulation
    reset_req = urllib.request.Request("http://127.0.0.1:8000/api/simulation/reset", data=b"{}", headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(reset_req) as res:
        assert res.status == 200
        print("[OK] Simulation Reset to baseline: OK")

    print("\nALL LIVE ENDPOINTS AND SERVICES VERIFIED 100% HEALTHY!")

if __name__ == "__main__":
    run_checks()
