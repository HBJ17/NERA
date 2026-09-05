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

    def test_06b_place_search_and_dynamic_rerouting(self):
        # 1. Place Search Geocoding
        resp = client.get("/api/routing/search?q=Kohima")
        self.assertEqual(resp.status_code, 200)
        places = resp.json()
        self.assertGreaterEqual(len(places), 1)
        self.assertIn("Kohima", places[0]["name"])

        # 2. Dynamic Rerouting
        resp = client.post("/api/routing/reroute", json={
            "source_id": "node_guwahati",
            "destination_id": "node_kohima",
            "custom_avoid_edges": ["edge_nagaon_dimapur"]
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("recommended_route", data)

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

    def test_08b_field_report_verification_and_offline_sync(self):
        # 1. Citizen submits pending report
        resp = client.post("/api/reports/submit", json={
            "officer_name": "Citizen Traveler",
            "department": "Local Citizen",
            "reporter_role": "user",
            "incident_type": "Flood",
            "severity": "HIGH",
            "latitude": 26.1800,
            "longitude": 91.7500,
            "location_name": "Guwahati North Bank",
            "nearest_highway": "NH-27",
            "description": "Water logging near bridge",
            "confidence_score": 65.0
        })
        self.assertEqual(resp.status_code, 200)
        citizen_rpt = resp.json()
        self.assertEqual(citizen_rpt["verification_status"], "PENDING_VERIFICATION")

        # 2. Government Employee verifies report
        resp = client.post(f"/api/reports/verify/{citizen_rpt['id']}", json={
            "action": "CONFIRM",
            "verifier_name": "Er. T. Jamir",
            "verifier_department": "PWD / SDMA"
        })
        self.assertEqual(resp.status_code, 200)
        verify_data = resp.json()
        self.assertEqual(verify_data["status"], "success")
        self.assertEqual(verify_data["report"]["verification_status"], "ACTIVE_INCIDENT")

        # 3. Offline Batch Sync
        resp = client.post("/api/reports/sync-batch", json=[
            {
                "officer_name": "Offline Patroller",
                "department": "Traffic Police",
                "reporter_role": "gov_employee",
                "incident_type": "Road Blockage",
                "severity": "BLOCKING",
                "latitude": 27.5000,
                "longitude": 92.1000,
                "location_name": "Sela Sector",
                "nearest_highway": "NH-13",
                "description": "Fallen boulders",
                "emergency_flag": True
            }
        ])
        self.assertEqual(resp.status_code, 200)
        sync_res = resp.json()
        self.assertEqual(sync_res["status"], "synced")
        self.assertEqual(sync_res["synced_count"], 1)

    def test_09_government_employee_district_workflow(self):
        # 1. Fetch District Dashboard for Kohima
        resp = client.get("/api/district/dashboard/node_kohima")
        self.assertEqual(resp.status_code, 200)
        dash = resp.json()
        self.assertEqual(dash["district_id"], "node_kohima")
        self.assertIn("metrics", dash)
        self.assertIn("hospital_stock_runway", dash)
        self.assertGreaterEqual(dash["trust_score"], 90.0)

        # 2. Submit official employee report (High Trust 92%)
        resp = client.post("/api/district/official-report", json={
            "officer_name": "Er. T. Jamir",
            "department": "PWD Highway Division Kohima",
            "incident_type": "Landslide",
            "severity": "HIGH",
            "latitude": 25.6751,
            "longitude": 94.1086,
            "location_name": "NH-29 Km 12 near Kohima",
            "nearest_highway": "NH-29",
            "description": "Mudslide on NH-29 single lane blocked",
            "emergency_flag": True
        })
        self.assertEqual(resp.status_code, 200)
        off_rpt = resp.json()
        self.assertEqual(off_rpt["reporter_role"], "gov_employee")
        self.assertEqual(off_rpt["confidence_score"], 92.0)
        self.assertEqual(off_rpt["verification_status"], "ACTIVE_INCIDENT")

        # 3. Employee verifies via district router
        resp = client.post("/api/district/verify", json={
            "report_id": off_rpt["id"],
            "action": "CONFIRM",
            "officer_name": "Er. T. Jamir",
            "department": "SDMA Kohima"
        })
        self.assertEqual(resp.status_code, 200)
        v_res = resp.json()
        self.assertEqual(v_res["status"], "success")

if __name__ == "__main__":
    unittest.main()
