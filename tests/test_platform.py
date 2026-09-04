import os
import urllib.request
import json
import unittest

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000").rstrip("/")

def get(path):
    req = urllib.request.Request(f"{BASE_URL}{path}")
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode('utf-8'))

def post(path, payload):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode('utf-8'))

class TestNERLogisticsPlatform(unittest.TestCase):

    def test_01_health_and_root(self):
        status, data = get("/health")
        self.assertEqual(status, 200)
        self.assertEqual(data["status"], "healthy")

    def test_02_digital_twin_state(self):
        status, data = get("/api/twin/state")
        self.assertEqual(status, 200)
        self.assertIn("districts", data)
        self.assertIn("bridges", data)
        self.assertIn("highways", data)
        self.assertIn("fleet", data)
        self.assertGreaterEqual(len(data["districts"]), 30)
        self.assertGreaterEqual(len(data["bridges"]), 8)
        self.assertGreaterEqual(len(data["highways"]), 15)
        self.assertGreaterEqual(len(data["fleet"]), 5)

    def test_03_ai_landslide_prediction(self):
        status, data = post("/api/predict/landslide", {
            "rainfall_mm": 130.0,
            "slope_degrees": 38.0,
            "soil_saturation_pct": 85.0,
            "historical_landslide_count": 5
        })
        self.assertEqual(status, 200)
        self.assertGreaterEqual(data["landslide_risk_pct"], 75.0)
        self.assertIn("factor_breakdown", data)
        self.assertEqual(len(data["factor_breakdown"]), 4)

    def test_04_ai_flood_prediction(self):
        status, data = post("/api/predict/flood", {
            "rainfall_mm": 90.0,
            "river_discharge_cumec": 45000.0,
            "current_gauge_m": 8.9,
            "danger_mark_m": 8.5,
            "catchment_elevation_m": 50.0
        })
        self.assertEqual(status, 200)
        self.assertGreaterEqual(data["flood_risk_pct"], 70.0)

    def test_05_smart_route_optimizer(self):
        status, data = post("/api/routing/optimize", {
            "source_id": "node_guwahati",
            "destination_id": "node_tawang",
            "avoid_high_risk": True
        })
        self.assertEqual(status, 200)
        self.assertIn("recommended_route", data)
        rec = data["recommended_route"]
        self.assertGreater(rec["total_distance_km"], 0)
        self.assertGreater(len(rec["segments"]), 0)
        self.assertGreater(len(rec["path_coordinates"]), 0)

    def test_06_what_if_simulation_sandbox(self):
        status, data = post("/api/simulation/run", {
            "scenario_id": "scenario_sela_landslide",
            "disaster_severity": "HIGH",
            "weather_multiplier": 1.5
        })
        self.assertEqual(status, 200)
        self.assertIn("isolated_districts", data)
        self.assertIn("delayed_vehicles", data)
        self.assertIn("critical_supplies_at_risk", data)
        self.assertIn("ai_generated_reroutes", data)
        self.assertIn("emergency_action_recommendations", data)

    def test_07_field_report_and_twin_propagation(self):
        # Submit a field report
        status, data = post("/api/reports/submit", {
            "officer_name": "Test PWD Inspector",
            "department": "PWD Engineer",
            "incident_type": "Landslide",
            "severity": "HIGH",
            "latitude": 25.1764,
            "longitude": 93.0189,
            "location_name": "Jatinga Valley Km 140",
            "nearest_highway": "NH-27",
            "description": "Active debris sliding",
            "estimated_clearance_hrs": 3.0
        })
        self.assertEqual(status, 200)
        self.assertIn("id", data)

        # Verify alerts contain new report
        status, alerts = get("/api/alerts/active")
        self.assertEqual(status, 200)
        self.assertGreater(len(alerts), 0)

if __name__ == "__main__":
    unittest.main()
