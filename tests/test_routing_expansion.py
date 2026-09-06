import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import networkx as nx
from fastapi.testclient import TestClient
from app.main import app
from app.services.digital_twin_data import NER_DISTRICT_NODES, NER_ROAD_EDGES
from app.services.routing_engine import smart_route_engine

client = TestClient(app)

class TestRoutingExpansion(unittest.TestCase):

    def test_01_all_nodes_connected_in_graph(self):
        """Verify that every single district node has road edges and the entire graph is fully connected"""
        smart_route_engine.build_graph()
        G = smart_route_engine.G_distance
        
        # Check every district node exists in graph
        for node in NER_DISTRICT_NODES:
            self.assertTrue(G.has_node(node["id"]), f"Node {node['id']} missing from graph")
            # Verify degree > 0 (not an isolated island)
            degree = G.degree(node["id"])
            self.assertGreater(degree, 0, f"District {node['name']} ({node['id']}) has degree 0 (no road edges connected!)")

        # Verify full connectivity (single connected component)
        self.assertTrue(nx.is_connected(G), "The transport network graph is not fully connected!")

    def test_02_routing_across_all_states(self):
        """Test routing between key nodes across all 8 states"""
        state_nodes = [
            ("node_siliguri", "node_gangtok"),     # West Bengal -> Sikkim
            ("node_guwahati", "node_tawang"),      # Assam -> Arunachal Pradesh
            ("node_guwahati", "node_shillong"),    # Assam -> Meghalaya
            ("node_guwahati", "node_kohima"),      # Assam -> Nagaland
            ("node_guwahati", "node_imphal"),      # Assam -> Manipur
            ("node_guwahati", "node_aizawl"),      # Assam -> Mizoram
            ("node_guwahati", "node_agartala"),    # Assam -> Tripura
            ("node_tura", "node_mokokchung"),      # Meghalaya -> Nagaland
            ("node_dhubri", "node_pasighat"),      # Lower Assam -> Upper Arunachal
            ("node_gangtok", "node_lunglei"),      # Sikkim -> South Mizoram
        ]

        for src, dst in state_nodes:
            resp = client.post("/api/routing/optimize", json={
                "source_id": src,
                "destination_id": dst,
                "avoid_high_risk": True
            })
            self.assertEqual(resp.status_code, 200, f"Failed routing {src} -> {dst}")
            data = resp.json()
            self.assertIn("recommended_route", data)
            rec = data["recommended_route"]
            self.assertGreater(rec["total_distance_km"], 0)
            self.assertGreater(len(rec["segments"]), 0)
            self.assertGreater(len(rec["path_coordinates"]), 1)

    def test_03_search_places_geocoding(self):
        """Test autocomplete and geocoding search for districts, bridges, and passes"""
        queries = ["Guwahati", "Kohima", "Sela", "Saraighat", "Tura", "Mokokchung", "Dhubri"]
        for q in queries:
            resp = client.get(f"/api/routing/search?q={q}")
            self.assertEqual(resp.status_code, 200)
            places = resp.json()
            self.assertGreater(len(places), 0, f"No places returned for query '{q}'")

    def test_04_osrm_endpoint_fallback(self):
        """Test /api/routing/osrm-road endpoint handles coordinates cleanly"""
        resp = client.get("/api/routing/osrm-road?src_lat=26.1445&src_lng=91.7362&dst_lat=25.5788&dst_lng=91.8933")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("status", data)

    def test_05_disaster_simulation_and_reroute(self):
        """Test What-If simulation blockades and alternate bypass calculation"""
        resp = client.post("/api/simulation/run", json={
            "scenario_id": "scenario_haflong_breach",
            "disaster_severity": "HIGH",
            "weather_multiplier": 1.5
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("scenario_title", data)
        self.assertIn("isolated_districts", data)
        self.assertIn("delayed_vehicles", data)

        # Reset simulation
        reset_resp = client.post("/api/simulation/reset")
        self.assertEqual(reset_resp.status_code, 200)

    def test_06_point_hazard_simulation_and_reroute(self):
        """Test clicking map location to trigger disaster hazard and dynamic rerouting"""
        # Trigger point hazard near Guwahati-Shillong corridor (lat: 25.82, lng: 91.86)
        resp = client.post("/api/simulation/trigger-point", json={
            "lat": 25.8200,
            "lng": 91.8600,
            "disaster_type": "landslide",
            "severity": "TOTAL_BREACH"
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("nearest_edge_id", data)
        self.assertIn("severed_highway", data)
        self.assertIn("delayed_vehicles", data)
        self.assertIn("ai_generated_reroutes", data)

        # Verify edge is blocked in twin
        twin_resp = client.get("/api/twin/state")
        self.assertEqual(twin_resp.status_code, 200)
        twin_data = twin_resp.json()
        blocked_edges = [e for e in twin_data["highways"] if e["status"] == "blocked"]
        self.assertGreaterEqual(len(blocked_edges), 1)

        # Reset
        client.post("/api/simulation/reset")

    def test_07_fleet_cars_and_logistics(self):
        """Test fleet has both civilian cars and logistics trucks with driver info"""
        resp = client.get("/api/fleet/live")
        self.assertEqual(resp.status_code, 200)
        fleet = resp.json()
        self.assertGreaterEqual(len(fleet), 10)

        cars = [v for v in fleet if v.get("category") == "car"]
        logistics = [v for v in fleet if v.get("category") == "logistics"]

        self.assertGreaterEqual(len(cars), 4, "Expected at least 4 civilian cars")
        self.assertGreaterEqual(len(logistics), 6, "Expected at least 6 logistics trucks")

        # Verify driver & cargo details
        for v in cars + logistics:
            self.assertIn("driver_name", v)
            self.assertIn("driver_phone", v)
            self.assertIn("cargo_type", v)
            self.assertIn("source", v)
            self.assertIn("destination", v)

    def test_08_scientific_ai_risk_breakdown(self):
        """Test route optimization response contains empirical physics-informed AI risk breakdown"""
        resp = client.post("/api/routing/optimize", json={
            "source_id": "node_guwahati",
            "destination_id": "node_tawang",
            "avoid_high_risk": True
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("ai_risk_breakdown", data)
        ai_breakdown = data["ai_risk_breakdown"]
        self.assertIsNotNone(ai_breakdown)
        self.assertIn("model_formula", ai_breakdown)
        self.assertIn("composite_risk_score", ai_breakdown)
        self.assertIn("factors", ai_breakdown)
        self.assertGreaterEqual(len(ai_breakdown["factors"]), 3)
        self.assertIn("environmental_telemetry", ai_breakdown)

        # Recommended route should match composite score
        rec = data["recommended_route"]
        self.assertEqual(rec["aggregate_risk_score"], ai_breakdown["composite_risk_score"])
        self.assertIsNotNone(rec.get("ai_risk_breakdown"))

if __name__ == "__main__":
    unittest.main()
