import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestNERLogisticsPlatform(unittest.TestCase):

    def test_01_health_and_root(self):
        resp = client.get("/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "healthy")

    def test_02_roles_and_persona_switching(self):
        # 1. Get available roles
        resp = client.get("/api/roles/list")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("roles", data)
        self.assertIn("districts", data)
        self.assertEqual(len(data["roles"]), 3)
        role_ids = [r["id"] for r in data["roles"]]
        self.assertIn("admin", role_ids)
        self.assertIn("user", role_ids)
        self.assertIn("gov_employee", role_ids)

        # 2. Switch to Government Employee in Kohima
        resp = client.post("/api/roles/switch", json={
            "role": "gov_employee",
            "district_id": "node_kohima"
        })
        self.assertEqual(resp.status_code, 200)
        switched = resp.json()
        self.assertEqual(switched["role"], "gov_employee")
        self.assertEqual(switched["district_id"], "node_kohima")
        self.assertIn("Nagaland", switched["profile"]["department"])

        # 3. Get district summary for Kohima
        resp = client.get("/api/roles/district-summary/node_kohima")
        self.assertEqual(resp.status_code, 200)
        summary = resp.json()
        self.assertEqual(summary["district_id"], "node_kohima")
        self.assertIn("metrics", summary)
        self.assertIn("active_incidents", summary["metrics"])

    def test_03_digital_twin_state(self):
        resp = client.get("/api/twin/state")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("districts", data)
        self.assertIn("bridges", data)
        self.assertIn("highways", data)
        self.assertIn("fleet", data)
        self.assertGreaterEqual(len(data["districts"]), 30)
        self.assertGreaterEqual(len(data["bridges"]), 8)
        self.assertGreaterEqual(len(data["highways"]), 15)
        self.assertGreaterEqual(len(data["fleet"]), 5)

    def test_04_ai_landslide_prediction(self):
        resp = client.post("/api/predict/landslide", json={
            "rainfall_mm": 130.0,
            "slope_degrees": 38.0,
            "soil_saturation_pct": 85.0,
            "historical_landslide_count": 5
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertGreaterEqual(data["landslide_risk_pct"], 75.0)
        self.assertIn("factor_breakdown", data)
        self.assertEqual(len(data["factor_breakdown"]), 4)

    def test_05_ai_flood_prediction(self):
        resp = client.post("/api/predict/flood", json={
            "rainfall_mm": 90.0,
            "river_discharge_cumec": 45000.0,
            "current_gauge_m": 8.9,
            "danger_mark_m": 8.5,
            "catchment_elevation_m": 50.0
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertGreaterEqual(data["flood_risk_pct"], 70.0)

    def test_06_smart_route_optimizer(self):
        resp = client.post("/api/routing/optimize", json={
            "source_id": "node_guwahati",
            "destination_id": "node_tawang",
            "avoid_high_risk": True
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("recommended_route", data)
        rec = data["recommended_route"]
        self.assertGreater(rec["total_distance_km"], 0)
        self.assertGreater(len(rec["segments"]), 0)
        self.assertGreater(len(rec["path_coordinates"]), 0)

    def test_07_what_if_simulation_sandbox(self):
        resp = client.post("/api/simulation/run", json={
            "scenario_id": "scenario_sela_landslide",
            "disaster_severity": "HIGH",
            "weather_multiplier": 1.5
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("isolated_districts", data)
        self.assertIn("delayed_vehicles", data)
        self.assertIn("critical_supplies_at_risk", data)
        self.assertIn("ai_generated_reroutes", data)
        self.assertIn("emergency_action_recommendations", data)

    def test_08_field_report_and_twin_propagation(self):
        # Submit a field report
        resp = client.post("/api/reports/submit", json={
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
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("id", data)

        # Verify alerts contain new report
        resp = client.get("/api/alerts/active")
        self.assertEqual(resp.status_code, 200)
        alerts = resp.json()
        self.assertGreater(len(alerts), 0)

if __name__ == "__main__":
    unittest.main()
