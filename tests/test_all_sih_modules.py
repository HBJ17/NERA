import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

class TestAllSIHModules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_digital_twin_topology(self):
        """Req a: Real-time road, bridge, and transport accessibility monitoring"""
        res = self.client.get("/api/twin/state")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("districts", data)
        self.assertIn("highways", data)
        self.assertIn("bridges", data)
        self.assertGreaterEqual(len(data["districts"]), 32)
        self.assertGreaterEqual(len(data["bridges"]), 10)

    def test_02_open_meteo_live_weather(self):
        """Req b: Real-time meteorological telemetry & Doppler radar integration"""
        res = self.client.get("/api/weather/live-status")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("total_stations", data)
        self.assertGreaterEqual(data["total_stations"], 32)

        radar_res = self.client.get("/api/weather/radar-overlays")
        self.assertEqual(radar_res.status_code, 200)
        self.assertIsInstance(radar_res.json(), list)

    def test_03_ai_landslide_physics_engine(self):
        """Req b: Landslide probability prediction model"""
        res = self.client.post("/api/predict/landslide", json={
            "rainfall_mm": 120.0,
            "slope_degrees": 38.0,
            "soil_saturation_pct": 85.0,
            "historical_landslide_count": 6,
            "seismic_zone": 5
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("landslide_risk_pct", data)
        self.assertGreater(data["landslide_risk_pct"], 50.0)
        self.assertIn("factor_breakdown", data)

    def test_04_ai_river_flood_inundation(self):
        """Req b: River basin flood inundation prediction"""
        res = self.client.post("/api/predict/flood", json={
            "rainfall_mm": 110.0,
            "river_discharge_cumec": 45000.0,
            "current_gauge_m": 9.2,
            "danger_mark_m": 8.5,
            "catchment_elevation_m": 120.0
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("flood_risk_pct", data)
        self.assertIn("risk_tier", data)

    def test_05_smart_routing_resilient_detour(self):
        """Req c: AI alternate route suggestions and travel delays"""
        res = self.client.post("/api/routing/optimize", json={
            "source_id": "node_guwahati",
            "destination_id": "node_tawang",
            "avoid_high_risk": True
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("recommended_route", data)
        rec = data["recommended_route"]
        self.assertGreater(rec["total_distance_km"], 0)
        self.assertIn("ai_risk_breakdown", data)

    def test_06_what_if_disaster_simulation(self):
        """Req b & g: Network resilience stress-testing and isolated districts"""
        res = self.client.post("/api/simulation/run", json={
            "scenario_id": "scenario_sela_pass",
            "disaster_severity": "EXTREME",
            "weather_multiplier": 1.8
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("isolated_districts", data)
        self.assertIn("delayed_vehicles", data)
        self.client.post("/api/simulation/reset")

    def test_07_closed_loop_field_reporting(self):
        """Req e & f: Geotagged incident reporting & closed-loop edge severance"""
        res = self.client.post("/api/reports/submit", json={
            "location_name": "Haflong Hill Cut",
            "latitude": 25.1680,
            "longitude": 93.0180,
            "incident_type": "Landslide",
            "severity": "BLOCKING",
            "nearest_highway": "NH-27",
            "description": "Mud debris blocking both lanes of NH-27.",
            "officer_name": "Er. PWD Inspector",
            "department": "PWD Engineer",
            "reporter_role": "gov_employee",
            "confidence_score": 95.0
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("id", data)

        # Verify emergency alert was broadcast
        alerts = self.client.get("/api/alerts/active").json()
        self.assertGreaterEqual(len(alerts), 1)

    def test_08_pwa_offline_service_worker(self):
        """Req h: Offline PWA manifest and service worker caching"""
        m_res = self.client.get("/static/manifest.json")
        self.assertEqual(m_res.status_code, 200)
        self.assertIn("NERA", m_res.json()["name"])

        sw_res = self.client.get("/static/sw.js")
        self.assertEqual(sw_res.status_code, 200)
        self.assertIn("CACHE_NAME", sw_res.text)

    def test_09_district_vulnerability_index_and_spof(self):
        """Req g: District-wise connectivity status & supply chain bottlenecks"""
        dvi_res = self.client.get("/api/analytics/dvi-matrix")
        self.assertEqual(dvi_res.status_code, 200)
        dvi_data = dvi_res.json()
        self.assertGreaterEqual(dvi_data["total_districts"], 32)

        spof_res = self.client.get("/api/analytics/spof-bottlenecks")
        self.assertEqual(spof_res.status_code, 200)
        self.assertGreaterEqual(spof_res.json()["choke_points_count"], 4)

    def test_10_multimodal_emergency_logistics(self):
        """Req c & g: NW-2 barge routes, airbridge sorties, and Bailey bridging"""
        ww_res = self.client.get("/api/emergency/inland-waterways")
        self.assertEqual(ww_res.status_code, 200)
        self.assertGreaterEqual(len(ww_res.json()), 6)

        alg_res = self.client.get("/api/emergency/airbridge-algs")
        self.assertEqual(alg_res.status_code, 200)
        self.assertGreaterEqual(len(alg_res.json()), 6)

        mm_res = self.client.get("/api/emergency/multimodal-contingency?origin=Guwahati&destination=Tawang")
        self.assertEqual(mm_res.status_code, 200)
        self.assertIn("waterway_nw2", mm_res.json())
        self.assertIn("airbridge", mm_res.json())
        self.assertIn("bro_bailey_bridge", mm_res.json())

if __name__ == "__main__":
    unittest.main()
