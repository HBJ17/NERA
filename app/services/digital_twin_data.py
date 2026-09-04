"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Digital Twin Geospatial Infrastructure & Topology Store

Models:
- 32 Strategic District Logistics Hubs (Across all 8 North Eastern States)
- 10 Vital River Bridges (Brahmaputra, Barak, Teesta, Lohit)
- 18 Arterial Highway Corridors (NH-27, NH-13, NH-10, NH-06, etc.) with Polyline Vectors
- Active Emergency & Commercial Fleet Vehicles
"""
from typing import Dict, List, Any

# 32 Key NER Logistics Nodes with real coordinates, state, population, health inventory
NER_DISTRICT_NODES: List[Dict[str, Any]] = [
    # --- Assam ---
    {
        "id": "node_guwahati",
        "name": "Guwahati (Kamrup Metro)",
        "state": "Assam",
        "coordinates": [26.1445, 91.7362],
        "status": "connected",
        "hospitals": 14,
        "population": 1120000,
        "stock_oxygen_days": 18.5,
        "stock_rations_days": 45.0,
        "stock_medicines_days": 30.0,
        "critical_alert": None
    },
    {
        "id": "node_tezpur",
        "name": "Tezpur (Sonitpur)",
        "state": "Assam",
        "coordinates": [26.6528, 92.7926],
        "status": "connected",
        "hospitals": 6,
        "population": 380000,
        "stock_oxygen_days": 12.0,
        "stock_rations_days": 28.0,
        "stock_medicines_days": 22.0,
        "critical_alert": None
    },
    {
        "id": "node_nagaon",
        "name": "Nagaon",
        "state": "Assam",
        "coordinates": [26.3452, 92.6841],
        "status": "connected",
        "hospitals": 5,
        "population": 420000,
        "stock_oxygen_days": 10.5,
        "stock_rations_days": 32.0,
        "stock_medicines_days": 20.0,
        "critical_alert": None
    },
    {
        "id": "node_jorhat",
        "name": "Jorhat",
        "state": "Assam",
        "coordinates": [26.7509, 94.2037],
        "status": "connected",
        "hospitals": 7,
        "population": 390000,
        "stock_oxygen_days": 11.2,
        "stock_rations_days": 26.0,
        "stock_medicines_days": 18.5,
        "critical_alert": None
    },
    {
        "id": "node_dibrugarh",
        "name": "Dibrugarh",
        "state": "Assam",
        "coordinates": [27.4728, 94.9120],
        "status": "connected",
        "hospitals": 8,
        "population": 540000,
        "stock_oxygen_days": 14.0,
        "stock_rations_days": 35.0,
        "stock_medicines_days": 24.0,
        "critical_alert": None
    },
    {
        "id": "node_tinsukia",
        "name": "Tinsukia",
        "state": "Assam",
        "coordinates": [27.4922, 95.3468],
        "status": "connected",
        "hospitals": 5,
        "population": 360000,
        "stock_oxygen_days": 9.5,
        "stock_rations_days": 25.0,
        "stock_medicines_days": 16.0,
        "critical_alert": None
    },
    {
        "id": "node_silchar",
        "name": "Silchar (Cachar / Barak Valley)",
        "state": "Assam",
        "coordinates": [24.8333, 92.7789],
        "status": "limited",
        "hospitals": 6,
        "population": 520000,
        "stock_oxygen_days": 4.5,
        "stock_rations_days": 12.0,
        "stock_medicines_days": 6.5,
        "critical_alert": "NH-27 Haflong section vulnerable to monsoon mudslides"
    },
    {
        "id": "node_haflong",
        "name": "Haflong (Dima Hasao)",
        "state": "Assam",
        "coordinates": [25.1764, 93.0189],
        "status": "limited",
        "hospitals": 2,
        "population": 120000,
        "stock_oxygen_days": 3.0,
        "stock_rations_days": 8.0,
        "stock_medicines_days": 5.0,
        "critical_alert": "Steep hillside cuts experiencing high soil saturation"
    },
    {
        "id": "node_karimganj",
        "name": "Karimganj",
        "state": "Assam",
        "coordinates": [24.8649, 92.3590],
        "status": "limited",
        "hospitals": 3,
        "population": 310000,
        "stock_oxygen_days": 5.2,
        "stock_rations_days": 14.0,
        "stock_medicines_days": 8.0,
        "critical_alert": None
    },
    {
        "id": "node_goalpara",
        "name": "Goalpara",
        "state": "Assam",
        "coordinates": [26.1806, 90.6247],
        "status": "connected",
        "hospitals": 3,
        "population": 290000,
        "stock_oxygen_days": 8.0,
        "stock_rations_days": 22.0,
        "stock_medicines_days": 14.0,
        "critical_alert": None
    },
    {
        "id": "node_dhubri",
        "name": "Dhubri",
        "state": "Assam",
        "coordinates": [26.0207, 89.9740],
        "status": "connected",
        "hospitals": 4,
        "population": 340000,
        "stock_oxygen_days": 7.5,
        "stock_rations_days": 20.0,
        "stock_medicines_days": 12.0,
        "critical_alert": None
    },

    # --- Arunachal Pradesh ---
    {
        "id": "node_itanagar",
        "name": "Itanagar (Papum Pare)",
        "state": "Arunachal Pradesh",
        "coordinates": [27.0844, 93.6053],
        "status": "connected",
        "hospitals": 5,
        "population": 195000,
        "stock_oxygen_days": 8.5,
        "stock_rations_days": 21.0,
        "stock_medicines_days": 15.0,
        "critical_alert": None
    },
    {
        "id": "node_tawang",
        "name": "Tawang",
        "state": "Arunachal Pradesh",
        "coordinates": [27.5861, 91.8594],
        "status": "limited",
        "hospitals": 2,
        "population": 55000,
        "stock_oxygen_days": 3.8,
        "stock_rations_days": 18.0,
        "stock_medicines_days": 7.0,
        "critical_alert": "Sela Pass corridor subject to dense fog and rockfalls"
    },
    {
        "id": "node_bomdila",
        "name": "Bomdila (West Kameng)",
        "state": "Arunachal Pradesh",
        "coordinates": [27.2645, 92.4159],
        "status": "connected",
        "hospitals": 2,
        "population": 68000,
        "stock_oxygen_days": 6.0,
        "stock_rations_days": 20.0,
        "stock_medicines_days": 11.0,
        "critical_alert": None
    },
    {
        "id": "node_pasighat",
        "name": "Pasighat (East Siang)",
        "state": "Arunachal Pradesh",
        "coordinates": [28.0668, 95.3263],
        "status": "connected",
        "hospitals": 3,
        "population": 92000,
        "stock_oxygen_days": 7.0,
        "stock_rations_days": 19.0,
        "stock_medicines_days": 13.0,
        "critical_alert": None
    },

    # --- Meghalaya ---
    {
        "id": "node_shillong",
        "name": "Shillong (East Khasi Hills)",
        "state": "Meghalaya",
        "coordinates": [25.5788, 91.8933],
        "status": "connected",
        "hospitals": 9,
        "population": 360000,
        "stock_oxygen_days": 15.0,
        "stock_rations_days": 30.0,
        "stock_medicines_days": 25.0,
        "critical_alert": None
    },
    {
        "id": "node_jowai",
        "name": "Jowai (West Jaintia Hills)",
        "state": "Meghalaya",
        "coordinates": [25.4526, 92.2038],
        "status": "connected",
        "hospitals": 3,
        "population": 115000,
        "stock_oxygen_days": 7.5,
        "stock_rations_days": 22.0,
        "stock_medicines_days": 14.0,
        "critical_alert": None
    },
    {
        "id": "node_tura",
        "name": "Tura (West Garo Hills)",
        "state": "Meghalaya",
        "coordinates": [25.5144, 90.2034],
        "status": "connected",
        "hospitals": 3,
        "population": 140000,
        "stock_oxygen_days": 6.8,
        "stock_rations_days": 24.0,
        "stock_medicines_days": 12.5,
        "critical_alert": None
    },

    # --- Nagaland ---
    {
        "id": "node_dimapur",
        "name": "Dimapur",
        "state": "Nagaland",
        "coordinates": [25.9068, 93.7273],
        "status": "connected",
        "hospitals": 6,
        "population": 280000,
        "stock_oxygen_days": 11.0,
        "stock_rations_days": 30.0,
        "stock_medicines_days": 19.0,
        "critical_alert": None
    },
    {
        "id": "node_kohima",
        "name": "Kohima",
        "state": "Nagaland",
        "coordinates": [25.6751, 94.1086],
        "status": "connected",
        "hospitals": 4,
        "population": 175000,
        "stock_oxygen_days": 8.0,
        "stock_rations_days": 25.0,
        "stock_medicines_days": 16.0,
        "critical_alert": None
    },
    {
        "id": "node_mokokchung",
        "name": "Mokokchung",
        "state": "Nagaland",
        "coordinates": [26.3248, 94.5161],
        "status": "connected",
        "hospitals": 2,
        "population": 85000,
        "stock_oxygen_days": 5.5,
        "stock_rations_days": 18.0,
        "stock_medicines_days": 9.5,
        "critical_alert": None
    },

    # --- Manipur ---
    {
        "id": "node_imphal",
        "name": "Imphal (Manipur Central)",
        "state": "Manipur",
        "coordinates": [24.8170, 93.9368],
        "status": "connected",
        "hospitals": 8,
        "population": 460000,
        "stock_oxygen_days": 9.0,
        "stock_rations_days": 24.0,
        "stock_medicines_days": 17.0,
        "critical_alert": None
    },
    {
        "id": "node_senapati",
        "name": "Senapati",
        "state": "Manipur",
        "coordinates": [25.2678, 94.0201],
        "status": "connected",
        "hospitals": 2,
        "population": 95000,
        "stock_oxygen_days": 6.0,
        "stock_rations_days": 20.0,
        "stock_medicines_days": 10.0,
        "critical_alert": None
    },
    {
        "id": "node_churachandpur",
        "name": "Churachandpur",
        "state": "Manipur",
        "coordinates": [24.3333, 93.6833],
        "status": "connected",
        "hospitals": 3,
        "population": 180000,
        "stock_oxygen_days": 5.8,
        "stock_rations_days": 18.0,
        "stock_medicines_days": 11.0,
        "critical_alert": None
    },

    # --- Mizoram ---
    {
        "id": "node_aizawl",
        "name": "Aizawl",
        "state": "Mizoram",
        "coordinates": [23.7271, 92.7176],
        "status": "connected",
        "hospitals": 5,
        "population": 310000,
        "stock_oxygen_days": 7.5,
        "stock_rations_days": 26.0,
        "stock_medicines_days": 15.0,
        "critical_alert": None
    },
    {
        "id": "node_lunglei",
        "name": "Lunglei",
        "state": "Mizoram",
        "coordinates": [22.8671, 92.7655],
        "status": "limited",
        "hospitals": 2,
        "population": 120000,
        "stock_oxygen_days": 4.5,
        "stock_rations_days": 16.0,
        "stock_medicines_days": 8.0,
        "critical_alert": None
    },

    # --- Tripura ---
    {
        "id": "node_agartala",
        "name": "Agartala",
        "state": "Tripura",
        "coordinates": [23.8315, 91.2868],
        "status": "connected",
        "hospitals": 7,
        "population": 420000,
        "stock_oxygen_days": 11.5,
        "stock_rations_days": 35.0,
        "stock_medicines_days": 22.0,
        "critical_alert": None
    },
    {
        "id": "node_dharmanagar",
        "name": "Dharmanagar (North Tripura)",
        "state": "Tripura",
        "coordinates": [24.3756, 92.1627],
        "status": "connected",
        "hospitals": 3,
        "population": 160000,
        "stock_oxygen_days": 8.0,
        "stock_rations_days": 28.0,
        "stock_medicines_days": 14.0,
        "critical_alert": None
    },

    # --- Sikkim & North Bengal Gateway ---
    {
        "id": "node_gangtok",
        "name": "Gangtok (East Sikkim)",
        "state": "Sikkim",
        "coordinates": [27.3389, 88.6065],
        "status": "limited",
        "hospitals": 4,
        "population": 110000,
        "stock_oxygen_days": 6.2,
        "stock_rations_days": 22.0,
        "stock_medicines_days": 12.0,
        "critical_alert": "NH-10 Teesta River gorge active sliding zone"
    },
    {
        "id": "node_mangan",
        "name": "Mangan (North Sikkim)",
        "state": "Sikkim",
        "coordinates": [27.5054, 88.5298],
        "status": "limited",
        "hospitals": 1,
        "population": 45000,
        "stock_oxygen_days": 3.0,
        "stock_rations_days": 14.0,
        "stock_medicines_days": 5.5,
        "critical_alert": "Fragile mountain road cut off by minor debris flow"
    },
    {
        "id": "node_siliguri",
        "name": "Siliguri Gateway (Chicken's Neck Corridor)",
        "state": "West Bengal / NER Gateway",
        "coordinates": [26.7271, 88.3953],
        "status": "connected",
        "hospitals": 10,
        "population": 750000,
        "stock_oxygen_days": 25.0,
        "stock_rations_days": 60.0,
        "stock_medicines_days": 40.0,
        "critical_alert": None
    }
]

# Strategic Bridges in NER with River sensor metrics
NER_BRIDGES: List[Dict[str, Any]] = [
    {
        "id": "bridge_saraighat",
        "name": "Saraighat Bridge & Rail-cum-Road Setu",
        "river": "Brahmaputra",
        "state": "Assam",
        "coordinates": [26.1772, 91.6811],
        "status": "operational",
        "structural_health": 94.5,
        "water_level_m": 4.8,
        "danger_mark_m": 8.5,
        "vulnerability_score": 18.0
    },
    {
        "id": "bridge_bogibeel",
        "name": "Bogibeel Bridge (Longest Rail-cum-Road)",
        "river": "Brahmaputra",
        "state": "Assam",
        "coordinates": [27.4042, 94.7570],
        "status": "operational",
        "structural_health": 99.0,
        "water_level_m": 5.2,
        "danger_mark_m": 9.2,
        "vulnerability_score": 8.5
    },
    {
        "id": "bridge_dhola_sadiya",
        "name": "Bhupen Hazarika Setu (Dhola-Sadiya)",
        "river": "Lohit",
        "state": "Assam / Arunachal",
        "coordinates": [27.7963, 95.6622],
        "status": "operational",
        "structural_health": 98.2,
        "water_level_m": 3.9,
        "danger_mark_m": 8.0,
        "vulnerability_score": 11.0
    },
    {
        "id": "bridge_kolia_bhomora",
        "name": "Kolia Bhomora Setu (Tezpur)",
        "river": "Brahmaputra",
        "state": "Assam",
        "coordinates": [26.6025, 92.8617],
        "status": "operational",
        "structural_health": 91.0,
        "water_level_m": 5.4,
        "danger_mark_m": 8.8,
        "vulnerability_score": 22.0
    },
    {
        "id": "bridge_naranarayan",
        "name": "Naranarayan Setu (Jogighopa-Pancharatna)",
        "river": "Brahmaputra",
        "state": "Assam",
        "coordinates": [26.2167, 90.5833],
        "status": "operational",
        "structural_health": 93.0,
        "water_level_m": 4.6,
        "danger_mark_m": 8.2,
        "vulnerability_score": 15.0
    },
    {
        "id": "bridge_jadukata",
        "name": "Jadukata Cantilever Bridge",
        "river": "Kynshi / Jadukata",
        "state": "Meghalaya",
        "coordinates": [25.2289, 91.2405],
        "status": "operational",
        "structural_health": 95.5,
        "water_level_m": 3.1,
        "danger_mark_m": 6.8,
        "vulnerability_score": 14.0
    },
    {
        "id": "bridge_sela_viaduct",
        "name": "Sela Pass High Altitude Viaduct",
        "river": "Mountain Pass Gorge",
        "state": "Arunachal Pradesh",
        "coordinates": [27.5055, 92.1037],
        "status": "operational",
        "structural_health": 97.0,
        "water_level_m": 0.0,
        "danger_mark_m": 0.0,
        "vulnerability_score": 38.0
    },
    {
        "id": "bridge_barak",
        "name": "Barak River Bridge (Silchar Bypass)",
        "river": "Barak",
        "state": "Assam",
        "coordinates": [24.8211, 92.7915],
        "status": "operational",
        "structural_health": 88.0,
        "water_level_m": 6.1,
        "danger_mark_m": 8.0,
        "vulnerability_score": 32.0
    },
    {
        "id": "bridge_irang",
        "name": "Irang River Bridge (NH-37 Lifeline)",
        "river": "Irang",
        "state": "Manipur",
        "coordinates": [24.7833, 93.5167],
        "status": "operational",
        "structural_health": 86.5,
        "water_level_m": 4.5,
        "danger_mark_m": 7.0,
        "vulnerability_score": 42.0
    }
]

# Highway Edges Interconnecting the Logistics Network
NER_ROAD_EDGES: List[Dict[str, Any]] = [
    # Gateway to Guwahati
    {
        "id": "edge_siliguri_guwahati",
        "highway_code": "NH-27 (East-West Corridor)",
        "source": "node_siliguri",
        "target": "node_guwahati",
        "distance_km": 470.0,
        "avg_speed_kmh": 65.0,
        "elevation_gain_m": 120.0,
        "slope_deg": 4.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 8.0,
        "flood_risk": 15.0,
        "rainfall_mm": 18.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [26.7271, 88.3953],
            [26.5400, 89.2000],
            [26.1806, 90.6247],
            [26.1445, 91.7362]
        ]
    },
    # Guwahati to Shillong
    {
        "id": "edge_guwahati_shillong",
        "highway_code": "NH-06 (Guwahati-Shillong Expressway)",
        "source": "node_guwahati",
        "target": "node_shillong",
        "distance_km": 100.0,
        "avg_speed_kmh": 50.0,
        "elevation_gain_m": 1400.0,
        "slope_deg": 14.0,
        "terrain_type": "hilly",
        "status": "open",
        "landslide_risk": 22.0,
        "flood_risk": 5.0,
        "rainfall_mm": 35.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [26.1445, 91.7362],
            [25.8900, 91.8200],
            [25.6800, 91.8800],
            [25.5788, 91.8933]
        ]
    },
    # Shillong to Jowai
    {
        "id": "edge_shillong_jowai",
        "highway_code": "NH-06",
        "source": "node_shillong",
        "target": "node_jowai",
        "distance_km": 65.0,
        "avg_speed_kmh": 45.0,
        "elevation_gain_m": 250.0,
        "slope_deg": 12.0,
        "terrain_type": "hilly",
        "status": "open",
        "landslide_risk": 28.0,
        "flood_risk": 10.0,
        "rainfall_mm": 45.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [25.5788, 91.8933],
            [25.5100, 92.0500],
            [25.4526, 92.2038]
        ]
    },
    # Jowai to Silchar (Southern Meghalaya Bypass)
    {
        "id": "edge_jowai_silchar",
        "highway_code": "NH-06 (Jaintia Hills-Barak Corridor)",
        "source": "node_jowai",
        "target": "node_silchar",
        "distance_km": 145.0,
        "avg_speed_kmh": 40.0,
        "elevation_gain_m": 600.0,
        "slope_deg": 18.0,
        "terrain_type": "hilly",
        "status": "open",
        "landslide_risk": 45.0,
        "flood_risk": 25.0,
        "rainfall_mm": 68.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [25.4526, 92.2038],
            [25.1800, 92.3800],
            [24.9500, 92.5500],
            [24.8333, 92.7789]
        ]
    },
    # Guwahati to Nagaon
    {
        "id": "edge_guwahati_nagaon",
        "highway_code": "NH-27 4-Lane",
        "source": "node_guwahati",
        "target": "node_nagaon",
        "distance_km": 120.0,
        "avg_speed_kmh": 70.0,
        "elevation_gain_m": 50.0,
        "slope_deg": 2.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 4.0,
        "flood_risk": 18.0,
        "rainfall_mm": 20.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [26.1445, 91.7362],
            [26.2100, 92.2000],
            [26.3452, 92.6841]
        ]
    },
    # Nagaon to Tezpur
    {
        "id": "edge_nagaon_tezpur",
        "highway_code": "NH-715 via Kolia Bhomora Setu",
        "source": "node_nagaon",
        "target": "node_tezpur",
        "distance_km": 55.0,
        "avg_speed_kmh": 55.0,
        "elevation_gain_m": 40.0,
        "slope_deg": 2.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 3.0,
        "flood_risk": 30.0,
        "rainfall_mm": 25.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [26.3452, 92.6841],
            [26.5200, 92.7500],
            [26.6528, 92.7926]
        ]
    },
    # Tezpur to Bomdila
    {
        "id": "edge_tezpur_bomdila",
        "highway_code": "NH-13 (Trans-Arunachal Highway)",
        "source": "node_tezpur",
        "target": "node_bomdila",
        "distance_km": 155.0,
        "avg_speed_kmh": 38.0,
        "elevation_gain_m": 2100.0,
        "slope_deg": 24.0,
        "terrain_type": "steep_gorge",
        "status": "open",
        "landslide_risk": 48.0,
        "flood_risk": 12.0,
        "rainfall_mm": 55.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [26.6528, 92.7926],
            [26.9800, 92.6200],
            [27.1500, 92.5100],
            [27.2645, 92.4159]
        ]
    },
    # Bomdila to Tawang (Via Sela Pass)
    {
        "id": "edge_bomdila_tawang",
        "highway_code": "NH-13 (Sela Pass Highway)",
        "source": "node_bomdila",
        "target": "node_tawang",
        "distance_km": 170.0,
        "avg_speed_kmh": 32.0,
        "elevation_gain_m": 2400.0,
        "slope_deg": 28.0,
        "terrain_type": "steep_gorge",
        "status": "warning",
        "landslide_risk": 78.0,
        "flood_risk": 8.0,
        "rainfall_mm": 72.0,
        "closure_reason": "High landslide vulnerability on Sela hairpin ascents",
        "coordinates_polyline": [
            [27.2645, 92.4159],
            [27.3900, 92.2200],
            [27.5055, 92.1037],
            [27.5861, 91.8594]
        ]
    },
    # Tezpur to Itanagar
    {
        "id": "edge_tezpur_itanagar",
        "highway_code": "NH-15 / NH-415",
        "source": "node_tezpur",
        "target": "node_itanagar",
        "distance_km": 160.0,
        "avg_speed_kmh": 50.0,
        "elevation_gain_m": 650.0,
        "slope_deg": 10.0,
        "terrain_type": "hilly",
        "status": "open",
        "landslide_risk": 35.0,
        "flood_risk": 20.0,
        "rainfall_mm": 40.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [26.6528, 92.7926],
            [26.8500, 93.1800],
            [27.0200, 93.4500],
            [27.0844, 93.6053]
        ]
    },
    # Nagaon to Jorhat
    {
        "id": "edge_nagaon_jorhat",
        "highway_code": "NH-715 (Kaziranga Corridor)",
        "source": "node_nagaon",
        "target": "node_jorhat",
        "distance_km": 185.0,
        "avg_speed_kmh": 55.0,
        "elevation_gain_m": 60.0,
        "slope_deg": 2.0,
        "terrain_type": "floodplain",
        "status": "open",
        "landslide_risk": 5.0,
        "flood_risk": 42.0,
        "rainfall_mm": 38.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [26.3452, 92.6841],
            [26.5800, 93.3500],
            [26.6200, 93.8500],
            [26.7509, 94.2037]
        ]
    },
    # Jorhat to Dibrugarh
    {
        "id": "edge_jorhat_dibrugarh",
        "highway_code": "NH-2",
        "source": "node_jorhat",
        "target": "node_dibrugarh",
        "distance_km": 130.0,
        "avg_speed_kmh": 60.0,
        "elevation_gain_m": 40.0,
        "slope_deg": 2.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 2.0,
        "flood_risk": 25.0,
        "rainfall_mm": 28.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [26.7509, 94.2037],
            [27.0200, 94.5500],
            [27.4728, 94.9120]
        ]
    },
    # Dibrugarh to Tinsukia
    {
        "id": "edge_dibrugarh_tinsukia",
        "highway_code": "NH-37",
        "source": "node_dibrugarh",
        "target": "node_tinsukia",
        "distance_km": 48.0,
        "avg_speed_kmh": 65.0,
        "elevation_gain_m": 20.0,
        "slope_deg": 1.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 2.0,
        "flood_risk": 15.0,
        "rainfall_mm": 22.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [27.4728, 94.9120],
            [27.4922, 95.3468]
        ]
    },
    # Dibrugarh to Pasighat (Via Bogibeel Bridge)
    {
        "id": "edge_dibrugarh_pasighat",
        "highway_code": "NH-515 via Bogibeel Bridge",
        "source": "node_dibrugarh",
        "target": "node_pasighat",
        "distance_km": 140.0,
        "avg_speed_kmh": 50.0,
        "elevation_gain_m": 350.0,
        "slope_deg": 8.0,
        "terrain_type": "hilly",
        "status": "open",
        "landslide_risk": 18.0,
        "flood_risk": 32.0,
        "rainfall_mm": 35.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [27.4728, 94.9120],
            [27.4042, 94.7570],
            [27.7500, 95.0500],
            [28.0668, 95.3263]
        ]
    },
    # Nagaon to Haflong (Dima Hasao Corridor)
    {
        "id": "edge_nagaon_haflong",
        "highway_code": "NH-27 Hill Section",
        "source": "node_nagaon",
        "target": "node_haflong",
        "distance_km": 170.0,
        "avg_speed_kmh": 40.0,
        "elevation_gain_m": 850.0,
        "slope_deg": 22.0,
        "terrain_type": "hilly",
        "status": "warning",
        "landslide_risk": 68.0,
        "flood_risk": 15.0,
        "rainfall_mm": 60.0,
        "closure_reason": "Mudflow accumulation near Jatinga valley",
        "coordinates_polyline": [
            [26.3452, 92.6841],
            [25.8500, 92.9500],
            [25.4500, 93.0000],
            [25.1764, 93.0189]
        ]
    },
    # Haflong to Silchar
    {
        "id": "edge_haflong_silchar",
        "highway_code": "NH-27 (Silchar Ghat)",
        "source": "node_haflong",
        "target": "node_silchar",
        "distance_km": 95.0,
        "avg_speed_kmh": 35.0,
        "elevation_gain_m": -600.0,
        "slope_deg": 26.0,
        "terrain_type": "steep_gorge",
        "status": "warning",
        "landslide_risk": 75.0,
        "flood_risk": 20.0,
        "rainfall_mm": 75.0,
        "closure_reason": "High active slope failure vulnerability",
        "coordinates_polyline": [
            [25.1764, 93.0189],
            [25.0200, 92.9100],
            [24.8333, 92.7789]
        ]
    },
    # Silchar to Karimganj
    {
        "id": "edge_silchar_karimganj",
        "highway_code": "NH-37",
        "source": "node_silchar",
        "target": "node_karimganj",
        "distance_km": 52.0,
        "avg_speed_kmh": 50.0,
        "elevation_gain_m": 15.0,
        "slope_deg": 2.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 5.0,
        "flood_risk": 38.0,
        "rainfall_mm": 35.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [24.8333, 92.7789],
            [24.8649, 92.3590]
        ]
    },
    # Karimganj to Dharmanagar (Tripura Entry)
    {
        "id": "edge_karimganj_dharmanagar",
        "highway_code": "NH-8",
        "source": "node_karimganj",
        "target": "node_dharmanagar",
        "distance_km": 60.0,
        "avg_speed_kmh": 48.0,
        "elevation_gain_m": 45.0,
        "slope_deg": 3.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 8.0,
        "flood_risk": 22.0,
        "rainfall_mm": 30.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [24.8649, 92.3590],
            [24.5800, 92.2200],
            [24.3756, 92.1627]
        ]
    },
    # Dharmanagar to Agartala
    {
        "id": "edge_dharmanagar_agartala",
        "highway_code": "NH-8 (Tripura Lifeline)",
        "source": "node_dharmanagar",
        "target": "node_agartala",
        "distance_km": 175.0,
        "avg_speed_kmh": 55.0,
        "elevation_gain_m": 90.0,
        "slope_deg": 5.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 12.0,
        "flood_risk": 20.0,
        "rainfall_mm": 32.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [24.3756, 92.1627],
            [24.1200, 91.8000],
            [23.9500, 91.5000],
            [23.8315, 91.2868]
        ]
    },
    # Silchar to Aizawl
    {
        "id": "edge_silchar_aizawl",
        "highway_code": "NH-306 / NH-54 (Mizoram Lifeline)",
        "source": "node_silchar",
        "target": "node_aizawl",
        "distance_km": 175.0,
        "avg_speed_kmh": 36.0,
        "elevation_gain_m": 1200.0,
        "slope_deg": 20.0,
        "terrain_type": "hilly",
        "status": "open",
        "landslide_risk": 52.0,
        "flood_risk": 10.0,
        "rainfall_mm": 58.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [24.8333, 92.7789],
            [24.4500, 92.6800],
            [24.0500, 92.7100],
            [23.7271, 92.7176]
        ]
    },
    # Aizawl to Lunglei
    {
        "id": "edge_aizawl_lunglei",
        "highway_code": "NH-54 South",
        "source": "node_aizawl",
        "target": "node_lunglei",
        "distance_km": 165.0,
        "avg_speed_kmh": 34.0,
        "elevation_gain_m": 400.0,
        "slope_deg": 18.0,
        "terrain_type": "hilly",
        "status": "open",
        "landslide_risk": 42.0,
        "flood_risk": 8.0,
        "rainfall_mm": 45.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [23.7271, 92.7176],
            [23.3000, 92.7800],
            [22.8671, 92.7655]
        ]
    },
    # Nagaon to Dimapur
    {
        "id": "edge_nagaon_dimapur",
        "highway_code": "NH-29",
        "source": "node_nagaon",
        "target": "node_dimapur",
        "distance_km": 150.0,
        "avg_speed_kmh": 58.0,
        "elevation_gain_m": 150.0,
        "slope_deg": 4.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 10.0,
        "flood_risk": 18.0,
        "rainfall_mm": 24.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [26.3452, 92.6841],
            [26.1200, 93.1800],
            [25.9068, 93.7273]
        ]
    },
    # Dimapur to Kohima
    {
        "id": "edge_dimapur_kohima",
        "highway_code": "NH-29 4-Lane Hill Section",
        "source": "node_dimapur",
        "target": "node_kohima",
        "distance_km": 72.0,
        "avg_speed_kmh": 38.0,
        "elevation_gain_m": 1250.0,
        "slope_deg": 21.0,
        "terrain_type": "hilly",
        "status": "open",
        "landslide_risk": 55.0,
        "flood_risk": 5.0,
        "rainfall_mm": 50.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [25.9068, 93.7273],
            [25.7900, 93.9200],
            [25.6751, 94.1086]
        ]
    },
    # Kohima to Senapati
    {
        "id": "edge_kohima_senapati",
        "highway_code": "NH-2",
        "source": "node_kohima",
        "target": "node_senapati",
        "distance_km": 68.0,
        "avg_speed_kmh": 40.0,
        "elevation_gain_m": 200.0,
        "slope_deg": 14.0,
        "terrain_type": "hilly",
        "status": "open",
        "landslide_risk": 38.0,
        "flood_risk": 6.0,
        "rainfall_mm": 42.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [25.6751, 94.1086],
            [25.4800, 94.0800],
            [25.2678, 94.0201]
        ]
    },
    # Senapati to Imphal
    {
        "id": "edge_senapati_imphal",
        "highway_code": "NH-2 (Manipur Northern Highway)",
        "source": "node_senapati",
        "target": "node_imphal",
        "distance_km": 60.0,
        "avg_speed_kmh": 48.0,
        "elevation_gain_m": -400.0,
        "slope_deg": 8.0,
        "terrain_type": "hilly",
        "status": "open",
        "landslide_risk": 25.0,
        "flood_risk": 15.0,
        "rainfall_mm": 35.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [25.2678, 94.0201],
            [25.0100, 93.9700],
            [24.8170, 93.9368]
        ]
    },
    # Silchar to Imphal (NH-37 Western Lifeline via Jiribam)
    {
        "id": "edge_silchar_imphal",
        "highway_code": "NH-37 (Jiribam-Imphal Highway)",
        "source": "node_silchar",
        "target": "node_imphal",
        "distance_km": 240.0,
        "avg_speed_kmh": 36.0,
        "elevation_gain_m": 900.0,
        "slope_deg": 23.0,
        "terrain_type": "steep_gorge",
        "status": "open",
        "landslide_risk": 62.0,
        "flood_risk": 18.0,
        "rainfall_mm": 65.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [24.8333, 92.7789],
            [24.8000, 93.1200],
            [24.7833, 93.5167],
            [24.8170, 93.9368]
        ]
    },
    # Imphal to Churachandpur
    {
        "id": "edge_imphal_churachandpur",
        "highway_code": "NH-102B",
        "source": "node_imphal",
        "target": "node_churachandpur",
        "distance_km": 65.0,
        "avg_speed_kmh": 52.0,
        "elevation_gain_m": 120.0,
        "slope_deg": 5.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 12.0,
        "flood_risk": 20.0,
        "rainfall_mm": 30.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [24.8170, 93.9368],
            [24.5800, 93.7900],
            [24.3333, 93.6833]
        ]
    },
    # Siliguri to Gangtok (NH-10 Teesta Lifeline)
    {
        "id": "edge_siliguri_gangtok",
        "highway_code": "NH-10 (Sikkim Lifeline)",
        "source": "node_siliguri",
        "target": "node_gangtok",
        "distance_km": 115.0,
        "avg_speed_kmh": 35.0,
        "elevation_gain_m": 1600.0,
        "slope_deg": 27.0,
        "terrain_type": "steep_gorge",
        "status": "warning",
        "landslide_risk": 74.0,
        "flood_risk": 35.0,
        "rainfall_mm": 82.0,
        "closure_reason": "High Teesta river swell & continuous boulder slips near 29th Mile",
        "coordinates_polyline": [
            [26.7271, 88.3953],
            [26.9500, 88.4800],
            [27.1800, 88.5200],
            [27.3389, 88.6065]
        ]
    },
    # Gangtok to Mangan
    {
        "id": "edge_gangtok_mangan",
        "highway_code": "North Sikkim Highway",
        "source": "node_gangtok",
        "target": "node_mangan",
        "distance_km": 65.0,
        "avg_speed_kmh": 28.0,
        "elevation_gain_m": 900.0,
        "slope_deg": 30.0,
        "terrain_type": "steep_gorge",
        "status": "warning",
        "landslide_risk": 82.0,
        "flood_risk": 15.0,
        "rainfall_mm": 90.0,
        "closure_reason": "Active debris flow on fragile hillside cuts",
        "coordinates_polyline": [
            [27.3389, 88.6065],
            [27.4200, 88.5800],
            [27.5054, 88.5298]
        ]
    }
]

# Active Simulated Vehicles with Live Telemetry
INITIAL_FLEET_DATA: List[Dict[str, Any]] = [
    {
        "id": "trk_v101",
        "vehicle_number": "AS-01-GC-9281",
        "driver_name": "Biraj Borah",
        "driver_phone": "+91 94350 11234",
        "vehicle_type": "Cryogenic Tanker (Oxygen)",
        "cargo_type": "Liquid Medical Oxygen (16,000 L)",
        "cargo_priority": "CRITICAL_LIFE_SAVING",
        "cargo_weight_tons": 18.5,
        "source": "Guwahati (AIIMS Logistics Depot)",
        "destination": "Silchar Medical College Hospital (SMCH)",
        "current_coordinates": [25.4500, 93.0000],
        "speed_kmh": 36.0,
        "heading_deg": 145.0,
        "status": "delayed",
        "delay_minutes": 45,
        "assigned_route_id": "edge_nagaon_haflong",
        "eta_timestamp": "3.5 Hours"
    },
    {
        "id": "trk_v102",
        "vehicle_number": "AS-12-BC-4492",
        "driver_name": "Tsering Norbu",
        "driver_phone": "+91 98620 44512",
        "vehicle_type": "Heavy 4x4 Army Logistic Carrier",
        "cargo_type": "Insulin, Antibiotics & Cold-Chain Vaccines",
        "cargo_priority": "CRITICAL_LIFE_SAVING",
        "cargo_weight_tons": 8.2,
        "source": "Tezpur Military Base",
        "destination": "Tawang District Civil Hospital",
        "current_coordinates": [27.3900, 92.2200],
        "speed_kmh": 28.0,
        "heading_deg": 310.0,
        "status": "delayed",
        "delay_minutes": 80,
        "assigned_route_id": "edge_bomdila_tawang",
        "eta_timestamp": "4.2 Hours"
    },
    {
        "id": "trk_v103",
        "vehicle_number": "NL-07-A-8819",
        "driver_name": "Kevichusa Angami",
        "driver_phone": "+91 94028 99120",
        "vehicle_type": "Heavy Multi-Axle Truck",
        "cargo_type": "FCI Rice & Wheat Essential Rations (24 Tons)",
        "cargo_priority": "HIGH",
        "cargo_weight_tons": 24.0,
        "source": "Dimapur Central Godown",
        "destination": "Imphal Relief Supply Depot",
        "current_coordinates": [25.7900, 93.9200],
        "speed_kmh": 42.0,
        "heading_deg": 160.0,
        "status": "moving",
        "delay_minutes": 0,
        "assigned_route_id": "edge_dimapur_kohima",
        "eta_timestamp": "2.8 Hours"
    },
    {
        "id": "trk_v104",
        "vehicle_number": "TR-01-T-5510",
        "driver_name": "Subir Debbarma",
        "driver_phone": "+91 94361 77319",
        "vehicle_type": "Fuel Tanker (Indian Oil)",
        "cargo_type": "High-Speed Diesel & Aviation Turbine Fuel",
        "cargo_priority": "HIGH",
        "cargo_weight_tons": 20.0,
        "source": "Guwahati Refinery (IOCL)",
        "destination": "Agartala Airport Storage Hub",
        "current_coordinates": [25.5100, 92.0500],
        "speed_kmh": 44.0,
        "heading_deg": 120.0,
        "status": "moving",
        "delay_minutes": 15,
        "assigned_route_id": "edge_shillong_jowai",
        "eta_timestamp": "6.0 Hours"
    },
    {
        "id": "trk_v105",
        "vehicle_number": "SK-01-D-3104",
        "driver_name": "Pemba Bhutia",
        "driver_phone": "+91 97330 22891",
        "vehicle_type": "Refrigerated Medical Van",
        "cargo_type": "Blood Plasma & Dialysis Concentrates",
        "cargo_priority": "CRITICAL_LIFE_SAVING",
        "cargo_weight_tons": 4.5,
        "source": "Siliguri Medical Hub",
        "destination": "STNM Multispeciality Hospital, Gangtok",
        "current_coordinates": [26.9500, 88.4800],
        "speed_kmh": 32.0,
        "heading_deg": 45.0,
        "status": "delayed",
        "delay_minutes": 60,
        "assigned_route_id": "edge_siliguri_gangtok",
        "eta_timestamp": "2.1 Hours"
    },
    {
        "id": "trk_v106",
        "vehicle_number": "MZ-01-K-1944",
        "driver_name": "Lalremruata Sailo",
        "driver_phone": "+91 98625 66011",
        "vehicle_type": "Heavy Cargo Truck",
        "cargo_type": "Baby Food, Milk Powder & Emergency Rations",
        "cargo_priority": "HIGH",
        "cargo_weight_tons": 14.0,
        "source": "Silchar Logistics Terminal",
        "destination": "Aizawl Civil Supply Depot",
        "current_coordinates": [24.4500, 92.6800],
        "speed_kmh": 38.0,
        "heading_deg": 175.0,
        "status": "moving",
        "delay_minutes": 10,
        "assigned_route_id": "edge_silchar_aizawl",
        "eta_timestamp": "4.5 Hours"
    },
    {
        "id": "trk_v107",
        "vehicle_number": "ML-05-H-7023",
        "driver_name": "Daphishi Marwein",
        "driver_phone": "+91 94363 44812",
        "vehicle_type": "Heavy Earthmover / PWD Recovery Crane",
        "cargo_type": "Road Clearance Equipment & Bailey Bridge Parts",
        "cargo_priority": "HIGH",
        "cargo_weight_tons": 26.0,
        "source": "Shillong PWD HQ",
        "destination": "Jadukata River Sector",
        "current_coordinates": [25.5788, 91.8933],
        "speed_kmh": 30.0,
        "heading_deg": 220.0,
        "status": "moving",
        "delay_minutes": 0,
        "assigned_route_id": "edge_guwahati_shillong",
        "eta_timestamp": "3.0 Hours"
    }
]

# Initial Emergency Alerts in multiple languages
INITIAL_ALERTS: List[Dict[str, Any]] = [
    {
        "id": "alt_01",
        "timestamp": "10 Mins Ago",
        "severity": "CRITICAL_DANGER",
        "category": "LANDSLIDE",
        "location_tag": "Sela Pass Corridor (NH-13, Arunachal)",
        "message_en": "RED ALERT: Massive boulder fall and soil liquefaction reported near Sela Tunnel ascent. Route hazardous for heavy commercial vehicles. AI suggests bypass via Rupa-Kalaktang.",
        "message_as": "ৰঙা সতৰ্কবাৰ্তা: চেলা পাছ অঞ্চলত ডাঙৰ শিল খহি পৰা আৰু ভূমিষ্খলনৰ ঘটনা। গধুৰ যান-বাহনৰ বাবে পথ বিপদজনক।",
        "message_hi": "रेड अलर्ट: सेला पास के पास भारी भूस्खलन और चट्टान गिरने की सूचना। भारी वाहनों के लिए मार्ग अत्यंत जोखिम भरा।",
        "message_bn": "লাল সতর্কতা: সেলা পাসের কাছে ভারী ভূমিধস ও পাথর পড়ার ঘটনা। ভারী পণ্যবাহী গাড়ির জন্য পথ বিপজ্জনক।",
        "affected_routes": ["NH-13"],
        "affected_districts": ["Tawang", "West Kameng"]
    },
    {
        "id": "alt_02",
        "timestamp": "25 Mins Ago",
        "severity": "WARNING",
        "category": "FLOOD",
        "location_tag": "Brahmaputra River - Kolia Bhomora / Tezpur",
        "message_en": "ORANGE ALERT: Brahmaputra water level rising 0.8m above normal at Tezpur ghat. PWD monitoring bridge pier vibration. Heavy 16-wheelers restricted.",
        "message_as": "কমলা সতৰ্কবাৰ্তা: তেজপুৰ ঘাটত ব্ৰহ্মপুত্ৰৰ জলপৃষ্ঠ বিপদসীমাৰ ওচৰ চাপিছে। দলঙৰ ওপৰেৰে গধুৰ বাহন চলাচলত নিয়ন্ত্ৰণ।",
        "message_hi": "ऑरेंज अलर्ट: तेजपुर में ब्रह्मपुत्र का जलस्तर खतरे के निशान के पास। भारी ट्रकों की आवाजाही नियंत्रित की गई।",
        "message_bn": "কমলা সতর্কতা: তেজপুরে ব্রহ্মপুত্র নদের জলস্তর বিপদসীমার কাছে। ভারী যান চলাচলে সতর্কতা জারি।",
        "affected_routes": ["NH-715"],
        "affected_districts": ["Sonitpur", "Nagaon"]
    },
    {
        "id": "alt_03",
        "timestamp": "40 Mins Ago",
        "severity": "WARNING",
        "category": "LANDSLIDE",
        "location_tag": "NH-10 Teesta Gorge (Siliguri - Gangtok)",
        "message_en": "YELLOW ALERT: Continuous debris sliding at 29th Mile corridor. Intermittent single-lane traffic open. Expect 60+ minutes delays.",
        "message_as": "হালধীয়া সতৰ্কবাৰ্তা: ২৯ মাইল অঞ্চলত অহৰহ মাটি খহি থকাৰ বাবে চিকিম সংযোগী পথত বিলম্ব ঘটিব পাৰে।",
        "message_hi": "येलो अलर्ट: 29th Mile के पास लगातार मलबा गिरने से एनएच-10 पर यातायात धीमा, 1 घंटे की देरी संभावित।",
        "message_bn": "হলুদ সতর্কতা: ২৯ মাইলের কাছে ক্রমাগত ভূমিধসের কারণে এনএইচ-১০ এ যান চলাচল বিঘ্নিত।",
        "affected_routes": ["NH-10"],
        "affected_districts": ["Gangtok", "Kalimpong"]
    }
]

# Initial PWD / Crowd Field Reports
INITIAL_FIELD_REPORTS: List[Dict[str, Any]] = [
    {
        "id": "rpt_901",
        "officer_name": "Pranjal Saikia (AE, PWD Roads)",
        "department": "PWD Engineer",
        "incident_type": "Landslide",
        "severity": "HIGH",
        "latitude": 25.1764,
        "longitude": 93.0189,
        "location_name": "Jatinga Hill Section, NH-27 (Dima Hasao)",
        "nearest_highway": "NH-27",
        "photo_base64": None,
        "photo_url": "https://images.unsplash.com/photo-1547683905-f686c993aae5?auto=format&fit=crop&w=600&q=80",
        "description": "Hill cutting caved in covering approx 45 meters of roadway. 2 JCB excavators deployed on site. Clearance underway.",
        "estimated_clearance_hrs": 4.5,
        "reported_at": "1 Hour Ago",
        "verification_status": "PWD_CONFIRMED"
    },
    {
        "id": "rpt_902",
        "officer_name": "Inspector Dorjee Khandu",
        "department": "Traffic Police",
        "incident_type": "Bridge Damaged",
        "severity": "MEDIUM",
        "latitude": 27.5055,
        "longitude": 92.1037,
        "location_name": "Sela Approach Culvert #4",
        "nearest_highway": "NH-13",
        "photo_base64": None,
        "photo_url": "https://images.unsplash.com/photo-1517649763962-0c623266ddc0?auto=format&fit=crop&w=600&q=80",
        "description": "Culvert abutment showing erosion after flash runoff. Light vehicles permitted; heavy trucks advised alternative pass.",
        "estimated_clearance_hrs": 6.0,
        "reported_at": "2 Hours Ago",
        "verification_status": "VERIFIED_AI"
    }
]
