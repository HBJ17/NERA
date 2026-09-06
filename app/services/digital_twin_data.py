"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Digital Twin Geospatial Infrastructure & Topology Store

Expanded Models:
- 84 Strategic Logistics Hubs across all 8 North Eastern States + Siliguri Gateway Corridor
- 14 Vital River Bridges & Structural Health Monitors
- 119 Interconnected National Highway & Frontier Lifeline Corridors
- Active Real-Time Emergency & Commercial Convoy Telemetry
"""
from typing import Dict, List, Any

NER_DISTRICT_NODES: List[Dict[str, Any]] = [
    {
        "id": "node_guwahati",
        "name": "Guwahati (Kamrup Metro)",
        "state": "Assam",
        "coordinates": [
            26.1445,
            91.7362
        ],
        "status": "connected",
        "hospitals": 16,
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
        "coordinates": [
            26.6528,
            92.7926
        ],
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
        "coordinates": [
            26.3452,
            92.6841
        ],
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
        "coordinates": [
            26.7509,
            94.2037
        ],
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
        "coordinates": [
            27.4728,
            94.912
        ],
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
        "coordinates": [
            27.4922,
            95.3468
        ],
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
        "coordinates": [
            24.8333,
            92.7789
        ],
        "status": "limited",
        "hospitals": 6,
        "population": 480000,
        "stock_oxygen_days": 4.5,
        "stock_rations_days": 14.0,
        "stock_medicines_days": 6.5,
        "critical_alert": "Barak river embankment alert. Convoy priority: HIGH."
    },
    {
        "id": "node_bongaigaon",
        "name": "Bongaigaon",
        "state": "Assam",
        "coordinates": [
            26.5019,
            90.5594
        ],
        "status": "connected",
        "hospitals": 5,
        "population": 310000,
        "stock_oxygen_days": 13.0,
        "stock_rations_days": 30.0,
        "stock_medicines_days": 21.0,
        "critical_alert": None
    },
    {
        "id": "node_dhubri",
        "name": "Dhubri (Brahmaputra Gate)",
        "state": "Assam",
        "coordinates": [
            26.0207,
            89.974
        ],
        "status": "connected",
        "hospitals": 4,
        "population": 350000,
        "stock_oxygen_days": 7.8,
        "stock_rations_days": 22.0,
        "stock_medicines_days": 14.0,
        "critical_alert": None
    },
    {
        "id": "node_haflong",
        "name": "Haflong (Dima Hasao Hill Sector)",
        "state": "Assam",
        "coordinates": [
            25.1764,
            93.0189
        ],
        "status": "limited",
        "hospitals": 3,
        "population": 190000,
        "stock_oxygen_days": 3.0,
        "stock_rations_days": 8.0,
        "stock_medicines_days": 5.0,
        "critical_alert": "Jatinga hill cutting prone to debris sliding."
    },
    {
        "id": "node_north_lakhimpur",
        "name": "North Lakhimpur",
        "state": "Assam",
        "coordinates": [
            27.2346,
            94.1037
        ],
        "status": "connected",
        "hospitals": 4,
        "population": 280000,
        "stock_oxygen_days": 8.2,
        "stock_rations_days": 20.0,
        "stock_medicines_days": 15.0,
        "critical_alert": None
    },
    {
        "id": "node_goalpara",
        "name": "Goalpara",
        "state": "Assam",
        "coordinates": [
            26.1754,
            90.6247
        ],
        "status": "connected",
        "hospitals": 4,
        "population": 290000,
        "stock_oxygen_days": 9.0,
        "stock_rations_days": 24.0,
        "stock_medicines_days": 17.0,
        "critical_alert": None
    },
    {
        "id": "node_barpeta",
        "name": "Barpeta",
        "state": "Assam",
        "coordinates": [
            26.3216,
            91.0048
        ],
        "status": "connected",
        "hospitals": 4,
        "population": 320000,
        "stock_oxygen_days": 8.5,
        "stock_rations_days": 22.0,
        "stock_medicines_days": 16.0,
        "critical_alert": None
    },
    {
        "id": "node_karimganj",
        "name": "Karimganj",
        "state": "Assam",
        "coordinates": [
            24.8693,
            92.3592
        ],
        "status": "limited",
        "hospitals": 4,
        "population": 330000,
        "stock_oxygen_days": 5.2,
        "stock_rations_days": 16.0,
        "stock_medicines_days": 8.0,
        "critical_alert": None
    },
    {
        "id": "node_hailakandi",
        "name": "Hailakandi",
        "state": "Assam",
        "coordinates": [
            24.6833,
            92.5667
        ],
        "status": "limited",
        "hospitals": 3,
        "population": 270000,
        "stock_oxygen_days": 4.8,
        "stock_rations_days": 15.0,
        "stock_medicines_days": 7.5,
        "critical_alert": None
    },
    {
        "id": "node_golaghat",
        "name": "Golaghat",
        "state": "Assam",
        "coordinates": [
            26.5167,
            93.9667
        ],
        "status": "connected",
        "hospitals": 4,
        "population": 260000,
        "stock_oxygen_days": 10.0,
        "stock_rations_days": 26.0,
        "stock_medicines_days": 18.0,
        "critical_alert": None
    },
    {
        "id": "node_sivasagar",
        "name": "Sivasagar",
        "state": "Assam",
        "coordinates": [
            26.9826,
            94.6425
        ],
        "status": "connected",
        "hospitals": 5,
        "population": 310000,
        "stock_oxygen_days": 11.0,
        "stock_rations_days": 28.0,
        "stock_medicines_days": 19.0,
        "critical_alert": None
    },
    {
        "id": "node_diphu",
        "name": "Diphu (Karbi Anglong)",
        "state": "Assam",
        "coordinates": [
            25.8456,
            93.4319
        ],
        "status": "connected",
        "hospitals": 4,
        "population": 220000,
        "stock_oxygen_days": 6.8,
        "stock_rations_days": 18.0,
        "stock_medicines_days": 11.0,
        "critical_alert": None
    },
    {
        "id": "node_kokrajhar",
        "name": "Kokrajhar (BTR)",
        "state": "Assam",
        "coordinates": [
            26.4014,
            90.2714
        ],
        "status": "connected",
        "hospitals": 4,
        "population": 270000,
        "stock_oxygen_days": 10.5,
        "stock_rations_days": 26.0,
        "stock_medicines_days": 18.0,
        "critical_alert": None
    },
    {
        "id": "node_majuli",
        "name": "Majuli Island (River District)",
        "state": "Assam",
        "coordinates": [
            26.95,
            94.2167
        ],
        "status": "limited",
        "hospitals": 2,
        "population": 170000,
        "stock_oxygen_days": 5.0,
        "stock_rations_days": 12.0,
        "stock_medicines_days": 7.0,
        "critical_alert": "Brahmaputra water cut off risk during monsoon."
    },
    {
        "id": "node_dhemaji",
        "name": "Dhemaji",
        "state": "Assam",
        "coordinates": [
            27.4833,
            94.5833
        ],
        "status": "limited",
        "hospitals": 3,
        "population": 240000,
        "stock_oxygen_days": 6.5,
        "stock_rations_days": 15.0,
        "stock_medicines_days": 9.5,
        "critical_alert": None
    },
    {
        "id": "node_mangaldai",
        "name": "Mangaldai (Darrang)",
        "state": "Assam",
        "coordinates": [
            26.4388,
            92.0336
        ],
        "status": "connected",
        "hospitals": 4,
        "population": 260000,
        "stock_oxygen_days": 9.2,
        "stock_rations_days": 24.0,
        "stock_medicines_days": 16.0,
        "critical_alert": None
    },
    {
        "id": "node_itanagar",
        "name": "Itanagar (State Capital)",
        "state": "Arunachal Pradesh",
        "coordinates": [
            27.0844,
            93.6053
        ],
        "status": "connected",
        "hospitals": 5,
        "population": 210000,
        "stock_oxygen_days": 11.0,
        "stock_rations_days": 28.0,
        "stock_medicines_days": 20.0,
        "critical_alert": None
    },
    {
        "id": "node_naharlagun",
        "name": "Naharlagun (Rail Terminal)",
        "state": "Arunachal Pradesh",
        "coordinates": [
            27.1044,
            93.6934
        ],
        "status": "connected",
        "hospitals": 4,
        "population": 140000,
        "stock_oxygen_days": 10.5,
        "stock_rations_days": 26.0,
        "stock_medicines_days": 19.0,
        "critical_alert": None
    },
    {
        "id": "node_tawang",
        "name": "Tawang (High-Altitude Strategic Hub)",
        "state": "Arunachal Pradesh",
        "coordinates": [
            27.5861,
            91.8594
        ],
        "status": "limited",
        "hospitals": 3,
        "population": 95000,
        "stock_oxygen_days": 3.8,
        "stock_rations_days": 18.0,
        "stock_medicines_days": 7.0,
        "critical_alert": "Sela Tunnel pass ice caution. Oxygen resupply critical."
    },
    {
        "id": "node_pasighat",
        "name": "Pasighat (East Siang Hub)",
        "state": "Arunachal Pradesh",
        "coordinates": [
            28.0667,
            95.3333
        ],
        "status": "connected",
        "hospitals": 4,
        "population": 130000,
        "stock_oxygen_days": 8.5,
        "stock_rations_days": 22.0,
        "stock_medicines_days": 15.0,
        "critical_alert": None
    },
    {
        "id": "node_bomdila",
        "name": "Bomdila (West Kameng)",
        "state": "Arunachal Pradesh",
        "coordinates": [
            27.2644,
            92.4222
        ],
        "status": "connected",
        "hospitals": 3,
        "population": 85000,
        "stock_oxygen_days": 6.2,
        "stock_rations_days": 20.0,
        "stock_medicines_days": 12.0,
        "critical_alert": None
    },
    {
        "id": "node_dirang",
        "name": "Dirang Valley",
        "state": "Arunachal Pradesh",
        "coordinates": [
            27.3575,
            92.2403
        ],
        "status": "connected",
        "hospitals": 2,
        "population": 60000,
        "stock_oxygen_days": 5.5,
        "stock_rations_days": 18.0,
        "stock_medicines_days": 10.0,
        "critical_alert": None
    },
    {
        "id": "node_bhalukpong",
        "name": "Bhalukpong (Kameng Gate)",
        "state": "Arunachal Pradesh",
        "coordinates": [
            27.0139,
            92.6458
        ],
        "status": "connected",
        "hospitals": 2,
        "population": 50000,
        "stock_oxygen_days": 8.0,
        "stock_rations_days": 22.0,
        "stock_medicines_days": 14.0,
        "critical_alert": None
    },
    {
        "id": "node_ziro",
        "name": "Ziro (Lower Subansiri)",
        "state": "Arunachal Pradesh",
        "coordinates": [
            27.5949,
            93.8344
        ],
        "status": "connected",
        "hospitals": 3,
        "population": 75000,
        "stock_oxygen_days": 6.0,
        "stock_rations_days": 19.0,
        "stock_medicines_days": 11.0,
        "critical_alert": None
    },
    {
        "id": "node_tezu",
        "name": "Tezu (Lohit Valley)",
        "state": "Arunachal Pradesh",
        "coordinates": [
            27.9167,
            96.1667
        ],
        "status": "connected",
        "hospitals": 3,
        "population": 80000,
        "stock_oxygen_days": 7.0,
        "stock_rations_days": 20.0,
        "stock_medicines_days": 13.0,
        "critical_alert": None
    },
    {
        "id": "node_roing",
        "name": "Roing (Dibang Valley)",
        "state": "Arunachal Pradesh",
        "coordinates": [
            28.1394,
            95.8361
        ],
        "status": "connected",
        "hospitals": 2,
        "population": 65000,
        "stock_oxygen_days": 6.5,
        "stock_rations_days": 18.0,
        "stock_medicines_days": 12.0,
        "critical_alert": None
    },
    {
        "id": "node_along",
        "name": "Along / Aalo (West Siang)",
        "state": "Arunachal Pradesh",
        "coordinates": [
            28.1706,
            94.8028
        ],
        "status": "connected",
        "hospitals": 3,
        "population": 70000,
        "stock_oxygen_days": 5.8,
        "stock_rations_days": 17.0,
        "stock_medicines_days": 10.5,
        "critical_alert": None
    },
    {
        "id": "node_namsai",
        "name": "Namsai (Golden Pagoda Hub)",
        "state": "Arunachal Pradesh",
        "coordinates": [
            27.6667,
            95.8667
        ],
        "status": "connected",
        "hospitals": 3,
        "population": 90000,
        "stock_oxygen_days": 8.0,
        "stock_rations_days": 22.0,
        "stock_medicines_days": 15.0,
        "critical_alert": None
    },
    {
        "id": "node_shillong",
        "name": "Shillong (East Khasi Hills)",
        "state": "Meghalaya",
        "coordinates": [
            25.5788,
            91.8933
        ],
        "status": "connected",
        "hospitals": 8,
        "population": 360000,
        "stock_oxygen_days": 14.5,
        "stock_rations_days": 32.0,
        "stock_medicines_days": 25.0,
        "critical_alert": None
    },
    {
        "id": "node_tura",
        "name": "Tura (Garo Hills Central)",
        "state": "Meghalaya",
        "coordinates": [
            25.5144,
            90.2025
        ],
        "status": "connected",
        "hospitals": 4,
        "population": 220000,
        "stock_oxygen_days": 7.5,
        "stock_rations_days": 20.0,
        "stock_medicines_days": 14.0,
        "critical_alert": None
    },
    {
        "id": "node_jowai",
        "name": "Jowai (West Jaintia Hills)",
        "state": "Meghalaya",
        "coordinates": [
            25.45,
            92.2
        ],
        "status": "connected",
        "hospitals": 4,
        "population": 160000,
        "stock_oxygen_days": 8.0,
        "stock_rations_days": 22.0,
        "stock_medicines_days": 15.0,
        "critical_alert": None
    },
    {
        "id": "node_nongpoh",
        "name": "Nongpoh (Ri-Bhoi NH-06 Gateway)",
        "state": "Meghalaya",
        "coordinates": [
            25.9036,
            91.8806
        ],
        "status": "connected",
        "hospitals": 3,
        "population": 120000,
        "stock_oxygen_days": 10.0,
        "stock_rations_days": 26.0,
        "stock_medicines_days": 18.0,
        "critical_alert": None
    },
    {
        "id": "node_cherrapunji",
        "name": "Cherrapunji / Sohra",
        "state": "Meghalaya",
        "coordinates": [
            25.27,
            91.73
        ],
        "status": "connected",
        "hospitals": 2,
        "population": 65000,
        "stock_oxygen_days": 6.0,
        "stock_rations_days": 18.0,
        "stock_medicines_days": 11.0,
        "critical_alert": "Extreme rainfall sector. Slopes saturated."
    },
    {
        "id": "node_dawki",
        "name": "Dawki (Border Trade Gate)",
        "state": "Meghalaya",
        "coordinates": [
            25.195,
            92.019
        ],
        "status": "connected",
        "hospitals": 2,
        "population": 45000,
        "stock_oxygen_days": 6.8,
        "stock_rations_days": 19.0,
        "stock_medicines_days": 12.0,
        "critical_alert": None
    },
    {
        "id": "node_williamnagar",
        "name": "Williamnagar (East Garo)",
        "state": "Meghalaya",
        "coordinates": [
            25.4944,
            90.6208
        ],
        "status": "connected",
        "hospitals": 3,
        "population": 95000,
        "stock_oxygen_days": 6.2,
        "stock_rations_days": 17.0,
        "stock_medicines_days": 11.5,
        "critical_alert": None
    },
    {
        "id": "node_baghmara",
        "name": "Baghmara (South Garo)",
        "state": "Meghalaya",
        "coordinates": [
            25.2,
            90.6333
        ],
        "status": "limited",
        "hospitals": 2,
        "population": 70000,
        "stock_oxygen_days": 4.6,
        "stock_rations_days": 14.0,
        "stock_medicines_days": 8.0,
        "critical_alert": None
    },
    {
        "id": "node_mairang",
        "name": "Mairang (West Khasi)",
        "state": "Meghalaya",
        "coordinates": [
            25.56,
            91.64
        ],
        "status": "connected",
        "hospitals": 2,
        "population": 80000,
        "stock_oxygen_days": 7.0,
        "stock_rations_days": 20.0,
        "stock_medicines_days": 13.0,
        "critical_alert": None
    },
    {
        "id": "node_kohima",
        "name": "Kohima (State Capital)",
        "state": "Nagaland",
        "coordinates": [
            25.6751,
            94.1086
        ],
        "status": "connected",
        "hospitals": 5,
        "population": 270000,
        "stock_oxygen_days": 8.5,
        "stock_rations_days": 22.0,
        "stock_medicines_days": 15.0,
        "critical_alert": None
    },
    {
        "id": "node_dimapur",
        "name": "Dimapur (Rail & Air Logistics Hub)",
        "state": "Nagaland",
        "coordinates": [
            25.906,
            93.727
        ],
        "status": "connected",
        "hospitals": 6,
        "population": 380000,
        "stock_oxygen_days": 15.0,
        "stock_rations_days": 38.0,
        "stock_medicines_days": 26.0,
        "critical_alert": None
    },
    {
        "id": "node_mokokchung",
        "name": "Mokokchung (Ao Sector)",
        "state": "Nagaland",
        "coordinates": [
            26.3249,
            94.5165
        ],
        "status": "connected",
        "hospitals": 4,
        "population": 170000,
        "stock_oxygen_days": 7.2,
        "stock_rations_days": 20.0,
        "stock_medicines_days": 13.0,
        "critical_alert": None
    },
    {
        "id": "node_tuensang",
        "name": "Tuensang (Eastern Hub)",
        "state": "Nagaland",
        "coordinates": [
            26.28,
            94.83
        ],
        "status": "limited",
        "hospitals": 3,
        "population": 150000,
        "stock_oxygen_days": 4.2,
        "stock_rations_days": 13.0,
        "stock_medicines_days": 7.5,
        "critical_alert": "Eastern mountain single lane sector."
    },
    {
        "id": "node_mon",
        "name": "Mon (Konyak Hill Sector)",
        "state": "Nagaland",
        "coordinates": [
            26.74,
            95.06
        ],
        "status": "limited",
        "hospitals": 3,
        "population": 160000,
        "stock_oxygen_days": 4.0,
        "stock_rations_days": 12.0,
        "stock_medicines_days": 7.0,
        "critical_alert": None
    },
    {
        "id": "node_wokha",
        "name": "Wokha (Lotha Sector)",
        "state": "Nagaland",
        "coordinates": [
            26.1,
            94.26
        ],
        "status": "connected",
        "hospitals": 3,
        "population": 110000,
        "stock_oxygen_days": 6.8,
        "stock_rations_days": 19.0,
        "stock_medicines_days": 12.0,
        "critical_alert": None
    },
    {
        "id": "node_zunheboto",
        "name": "Zunheboto (Sumi Ridge Hub)",
        "state": "Nagaland",
        "coordinates": [
            25.97,
            94.52
        ],
        "status": "limited",
        "hospitals": 3,
        "population": 120000,
        "stock_oxygen_days": 4.5,
        "stock_rations_days": 14.0,
        "stock_medicines_days": 8.0,
        "critical_alert": None
    },
    {
        "id": "node_phek",
        "name": "Phek (Chakhesang Sector)",
        "state": "Nagaland",
        "coordinates": [
            25.68,
            94.5
        ],
        "status": "limited",
        "hospitals": 3,
        "population": 130000,
        "stock_oxygen_days": 4.8,
        "stock_rations_days": 15.0,
        "stock_medicines_days": 8.5,
        "critical_alert": None
    },
    {
        "id": "node_kiphire",
        "name": "Kiphire (Saramati Sector)",
        "state": "Nagaland",
        "coordinates": [
            25.87,
            94.78
        ],
        "status": "limited",
        "hospitals": 2,
        "population": 85000,
        "stock_oxygen_days": 3.6,
        "stock_rations_days": 11.0,
        "stock_medicines_days": 6.0,
        "critical_alert": "High altitude isolated terrain."
    },
    {
        "id": "node_peren",
        "name": "Peren (Jalukie Sector)",
        "state": "Nagaland",
        "coordinates": [
            25.52,
            93.74
        ],
        "status": "connected",
        "hospitals": 2,
        "population": 95000,
        "stock_oxygen_days": 6.5,
        "stock_rations_days": 18.0,
        "stock_medicines_days": 12.0,
        "critical_alert": None
    },
    {
        "id": "node_imphal",
        "name": "Imphal (Manipur Valley Central)",
        "state": "Manipur",
        "coordinates": [
            24.817,
            93.9368
        ],
        "status": "connected",
        "hospitals": 7,
        "population": 490000,
        "stock_oxygen_days": 9.0,
        "stock_rations_days": 24.0,
        "stock_medicines_days": 17.0,
        "critical_alert": None
    },
    {
        "id": "node_churachandpur",
        "name": "Churachandpur (Lamka Hub)",
        "state": "Manipur",
        "coordinates": [
            24.3333,
            93.6833
        ],
        "status": "limited",
        "hospitals": 4,
        "population": 280000,
        "stock_oxygen_days": 4.8,
        "stock_rations_days": 14.0,
        "stock_medicines_days": 8.0,
        "critical_alert": None
    },
    {
        "id": "node_thoubal",
        "name": "Thoubal",
        "state": "Manipur",
        "coordinates": [
            24.6333,
            93.9833
        ],
        "status": "connected",
        "hospitals": 4,
        "population": 220000,
        "stock_oxygen_days": 8.0,
        "stock_rations_days": 20.0,
        "stock_medicines_days": 14.0,
        "critical_alert": None
    },
    {
        "id": "node_bishnupur",
        "name": "Bishnupur (Loktak Lake)",
        "state": "Manipur",
        "coordinates": [
            24.63,
            93.76
        ],
        "status": "connected",
        "hospitals": 3,
        "population": 180000,
        "stock_oxygen_days": 7.5,
        "stock_rations_days": 19.0,
        "stock_medicines_days": 13.5,
        "critical_alert": None
    },
    {
        "id": "node_ukhrul",
        "name": "Ukhrul (Shiroi Hills)",
        "state": "Manipur",
        "coordinates": [
            25.1167,
            94.3667
        ],
        "status": "limited",
        "hospitals": 3,
        "population": 140000,
        "stock_oxygen_days": 4.4,
        "stock_rations_days": 13.0,
        "stock_medicines_days": 7.5,
        "critical_alert": None
    },
    {
        "id": "node_senapati",
        "name": "Senapati (NH-02 Gateway)",
        "state": "Manipur",
        "coordinates": [
            25.27,
            94.02
        ],
        "status": "connected",
        "hospitals": 3,
        "population": 160000,
        "stock_oxygen_days": 6.5,
        "stock_rations_days": 18.0,
        "stock_medicines_days": 12.0,
        "critical_alert": None
    },
    {
        "id": "node_tamenglong",
        "name": "Tamenglong (Western Hills)",
        "state": "Manipur",
        "coordinates": [
            24.9833,
            93.4833
        ],
        "status": "limited",
        "hospitals": 2,
        "population": 110000,
        "stock_oxygen_days": 3.8,
        "stock_rations_days": 10.0,
        "stock_medicines_days": 6.5,
        "critical_alert": "Barak tributary cut-off prone."
    },
    {
        "id": "node_jiribam",
        "name": "Jiribam (Assam Border Railhead)",
        "state": "Manipur",
        "coordinates": [
            24.8,
            93.12
        ],
        "status": "connected",
        "hospitals": 3,
        "population": 65000,
        "stock_oxygen_days": 9.5,
        "stock_rations_days": 25.0,
        "stock_medicines_days": 16.0,
        "critical_alert": None
    },
    {
        "id": "node_moreh",
        "name": "Moreh (AH-1 Myanmar Border Gate)",
        "state": "Manipur",
        "coordinates": [
            24.25,
            94.3
        ],
        "status": "limited",
        "hospitals": 2,
        "population": 55000,
        "stock_oxygen_days": 5.0,
        "stock_rations_days": 15.0,
        "stock_medicines_days": 9.0,
        "critical_alert": "International border trade corridor."
    },
    {
        "id": "node_aizawl",
        "name": "Aizawl (State Capital Ridge)",
        "state": "Mizoram",
        "coordinates": [
            23.7271,
            92.7176
        ],
        "status": "connected",
        "hospitals": 6,
        "population": 340000,
        "stock_oxygen_days": 7.2,
        "stock_rations_days": 22.0,
        "stock_medicines_days": 14.0,
        "critical_alert": None
    },
    {
        "id": "node_lunglei",
        "name": "Lunglei (South Mizoram Central)",
        "state": "Mizoram",
        "coordinates": [
            22.88,
            92.73
        ],
        "status": "limited",
        "hospitals": 4,
        "population": 160000,
        "stock_oxygen_days": 4.5,
        "stock_rations_days": 15.0,
        "stock_medicines_days": 8.0,
        "critical_alert": None
    },
    {
        "id": "node_champhai",
        "name": "Champhai (Zokhawthar Border)",
        "state": "Mizoram",
        "coordinates": [
            23.47,
            93.33
        ],
        "status": "limited",
        "hospitals": 3,
        "population": 120000,
        "stock_oxygen_days": 4.0,
        "stock_rations_days": 14.0,
        "stock_medicines_days": 7.5,
        "critical_alert": None
    },
    {
        "id": "node_kolasib",
        "name": "Kolasib (NH-306 Lifeline)",
        "state": "Mizoram",
        "coordinates": [
            24.22,
            92.68
        ],
        "status": "connected",
        "hospitals": 3,
        "population": 90000,
        "stock_oxygen_days": 7.0,
        "stock_rations_days": 20.0,
        "stock_medicines_days": 13.0,
        "critical_alert": None
    },
    {
        "id": "node_serchhip",
        "name": "Serchhip",
        "state": "Mizoram",
        "coordinates": [
            23.31,
            92.85
        ],
        "status": "connected",
        "hospitals": 2,
        "population": 75000,
        "stock_oxygen_days": 5.8,
        "stock_rations_days": 18.0,
        "stock_medicines_days": 11.0,
        "critical_alert": None
    },
    {
        "id": "node_lawngtlai",
        "name": "Lawngtlai (Kaladan Corridor)",
        "state": "Mizoram",
        "coordinates": [
            22.52,
            92.89
        ],
        "status": "limited",
        "hospitals": 2,
        "population": 85000,
        "stock_oxygen_days": 3.8,
        "stock_rations_days": 12.0,
        "stock_medicines_days": 6.8,
        "critical_alert": None
    },
    {
        "id": "node_mamit",
        "name": "Mamit (Western Sector)",
        "state": "Mizoram",
        "coordinates": [
            23.93,
            92.49
        ],
        "status": "limited",
        "hospitals": 2,
        "population": 70000,
        "stock_oxygen_days": 4.2,
        "stock_rations_days": 13.0,
        "stock_medicines_days": 7.0,
        "critical_alert": None
    },
    {
        "id": "node_vairengte",
        "name": "Vairengte (Assam Entry Gate)",
        "state": "Mizoram",
        "coordinates": [
            24.51,
            92.76
        ],
        "status": "connected",
        "hospitals": 2,
        "population": 50000,
        "stock_oxygen_days": 9.0,
        "stock_rations_days": 25.0,
        "stock_medicines_days": 16.0,
        "critical_alert": None
    },
    {
        "id": "node_agartala",
        "name": "Agartala (State Capital)",
        "state": "Tripura",
        "coordinates": [
            23.8315,
            91.2868
        ],
        "status": "connected",
        "hospitals": 7,
        "population": 530000,
        "stock_oxygen_days": 16.0,
        "stock_rations_days": 40.0,
        "stock_medicines_days": 28.0,
        "critical_alert": None
    },
    {
        "id": "node_udaipur",
        "name": "Udaipur (Gomati Hub)",
        "state": "Tripura",
        "coordinates": [
            23.5333,
            91.4833
        ],
        "status": "connected",
        "hospitals": 4,
        "population": 210000,
        "stock_oxygen_days": 11.5,
        "stock_rations_days": 28.0,
        "stock_medicines_days": 20.0,
        "critical_alert": None
    },
    {
        "id": "node_dharmanagar",
        "name": "Dharmanagar (North Tripura Railhead)",
        "state": "Tripura",
        "coordinates": [
            24.3833,
            92.1667
        ],
        "status": "connected",
        "hospitals": 4,
        "population": 180000,
        "stock_oxygen_days": 10.0,
        "stock_rations_days": 26.0,
        "stock_medicines_days": 18.0,
        "critical_alert": None
    },
    {
        "id": "node_kailashahar",
        "name": "Kailashahar (Unakoti Hub)",
        "state": "Tripura",
        "coordinates": [
            24.3333,
            92.0
        ],
        "status": "connected",
        "hospitals": 3,
        "population": 140000,
        "stock_oxygen_days": 8.0,
        "stock_rations_days": 22.0,
        "stock_medicines_days": 15.0,
        "critical_alert": None
    },
    {
        "id": "node_ambassa",
        "name": "Ambassa (Dhalai Central)",
        "state": "Tripura",
        "coordinates": [
            23.92,
            91.85
        ],
        "status": "connected",
        "hospitals": 3,
        "population": 130000,
        "stock_oxygen_days": 7.5,
        "stock_rations_days": 20.0,
        "stock_medicines_days": 14.0,
        "critical_alert": None
    },
    {
        "id": "node_belonia",
        "name": "Belonia (South Border Gate)",
        "state": "Tripura",
        "coordinates": [
            23.25,
            91.45
        ],
        "status": "connected",
        "hospitals": 3,
        "population": 120000,
        "stock_oxygen_days": 8.5,
        "stock_rations_days": 23.0,
        "stock_medicines_days": 16.0,
        "critical_alert": None
    },
    {
        "id": "node_sabroom",
        "name": "Sabroom (Maitri Setu Port Gate)",
        "state": "Tripura",
        "coordinates": [
            23.0,
            91.73
        ],
        "status": "connected",
        "hospitals": 2,
        "population": 75000,
        "stock_oxygen_days": 7.0,
        "stock_rations_days": 20.0,
        "stock_medicines_days": 13.5,
        "critical_alert": "Multimodal link to Chittagong Port."
    },
    {
        "id": "node_gangtok",
        "name": "Gangtok (State Capital)",
        "state": "Sikkim",
        "coordinates": [
            27.3389,
            88.6065
        ],
        "status": "connected",
        "hospitals": 5,
        "population": 180000,
        "stock_oxygen_days": 6.2,
        "stock_rations_days": 22.0,
        "stock_medicines_days": 12.0,
        "critical_alert": "Teesta Gorge NH-10 vulnerability."
    },
    {
        "id": "node_namchi",
        "name": "Namchi (South Sikkim)",
        "state": "Sikkim",
        "coordinates": [
            27.17,
            88.35
        ],
        "status": "connected",
        "hospitals": 3,
        "population": 90000,
        "stock_oxygen_days": 7.0,
        "stock_rations_days": 24.0,
        "stock_medicines_days": 14.0,
        "critical_alert": None
    },
    {
        "id": "node_geyzing",
        "name": "Geyzing / Pelling (West Sikkim)",
        "state": "Sikkim",
        "coordinates": [
            27.28,
            88.25
        ],
        "status": "connected",
        "hospitals": 3,
        "population": 80000,
        "stock_oxygen_days": 5.5,
        "stock_rations_days": 20.0,
        "stock_medicines_days": 11.0,
        "critical_alert": None
    },
    {
        "id": "node_mangan",
        "name": "Mangan (North Sikkim Gorge)",
        "state": "Sikkim",
        "coordinates": [
            27.52,
            88.53
        ],
        "status": "limited",
        "hospitals": 2,
        "population": 55000,
        "stock_oxygen_days": 3.5,
        "stock_rations_days": 14.0,
        "stock_medicines_days": 6.5,
        "critical_alert": "Glacial lake / flash flood zone."
    },
    {
        "id": "node_rangpo",
        "name": "Rangpo (NH-10 Entry Gateway)",
        "state": "Sikkim",
        "coordinates": [
            27.18,
            88.53
        ],
        "status": "connected",
        "hospitals": 3,
        "population": 70000,
        "stock_oxygen_days": 9.0,
        "stock_rations_days": 26.0,
        "stock_medicines_days": 17.0,
        "critical_alert": None
    },
    {
        "id": "node_nathula",
        "name": "Nathu La Pass (Old Silk Route)",
        "state": "Sikkim",
        "coordinates": [
            27.3865,
            88.831
        ],
        "status": "limited",
        "hospitals": 1,
        "population": 15000,
        "stock_oxygen_days": 3.0,
        "stock_rations_days": 10.0,
        "stock_medicines_days": 5.0,
        "critical_alert": "High altitude pass (14,140 ft)."
    },
    {
        "id": "node_siliguri",
        "name": "Siliguri (Chicken's Neck Tri-Junction)",
        "state": "West Bengal Gateway",
        "coordinates": [
            26.7271,
            88.3953
        ],
        "status": "connected",
        "hospitals": 12,
        "population": 950000,
        "stock_oxygen_days": 22.0,
        "stock_rations_days": 50.0,
        "stock_medicines_days": 35.0,
        "critical_alert": None
    }
]

NER_BRIDGES: List[Dict[str, Any]] = [
    {
        "id": "bridge_saraighat",
        "name": "Saraighat Bridge (Brahmaputra South-North Trunk)",
        "river": "Brahmaputra",
        "state": "Assam",
        "coordinates": [
            26.1283,
            91.6811
        ],
        "structural_health": 88.0,
        "water_level_m": 48.5,
        "danger_mark_m": 50.0,
        "vulnerability_score": 38.0,
        "status": "operational"
    },
    {
        "id": "bridge_kolia_bhomora",
        "name": "Kolia Bhomora Setu (Tezpur-Nagaon)",
        "river": "Brahmaputra",
        "state": "Assam",
        "coordinates": [
            26.6111,
            92.8639
        ],
        "structural_health": 82.0,
        "water_level_m": 66.8,
        "danger_mark_m": 68.0,
        "vulnerability_score": 45.0,
        "status": "operational"
    },
    {
        "id": "bridge_bogibeel",
        "name": "Bogibeel Rail-Road Bridge (Dibrugarh-Dhemaji)",
        "river": "Brahmaputra",
        "state": "Assam",
        "coordinates": [
            27.4,
            94.75
        ],
        "structural_health": 96.0,
        "water_level_m": 102.0,
        "danger_mark_m": 106.0,
        "vulnerability_score": 25.0,
        "status": "operational"
    },
    {
        "id": "bridge_dhola_sadiya",
        "name": "Bhupen Hazarika Setu (Dhola-Sadiya 9.15km)",
        "river": "Lohit",
        "state": "Assam / Arunachal Border",
        "coordinates": [
            27.7944,
            95.6694
        ],
        "structural_health": 94.0,
        "water_level_m": 128.0,
        "danger_mark_m": 133.0,
        "vulnerability_score": 30.0,
        "status": "operational"
    },
    {
        "id": "bridge_naranarayan",
        "name": "Naranarayan Setu (Jogighopa-Pancharatna)",
        "river": "Brahmaputra",
        "state": "Assam",
        "coordinates": [
            26.2083,
            90.625
        ],
        "structural_health": 79.0,
        "water_level_m": 29.2,
        "danger_mark_m": 31.5,
        "vulnerability_score": 52.0,
        "status": "warning"
    },
    {
        "id": "bridge_sadarghat",
        "name": "Sadarghat Bridge (Silchar Urban Link)",
        "river": "Barak",
        "state": "Assam",
        "coordinates": [
            24.8361,
            92.7889
        ],
        "structural_health": 65.0,
        "water_level_m": 19.8,
        "danger_mark_m": 20.0,
        "vulnerability_score": 75.0,
        "status": "warning"
    },
    {
        "id": "bridge_coronation",
        "name": "Sevoke Coronation Bridge (Teesta River Gorge)",
        "river": "Teesta",
        "state": "West Bengal / Sikkim Gateway",
        "coordinates": [
            26.8833,
            88.45
        ],
        "structural_health": 71.0,
        "water_level_m": 142.0,
        "danger_mark_m": 146.0,
        "vulnerability_score": 68.0,
        "status": "warning"
    },
    {
        "id": "bridge_maitri_setu",
        "name": "Maitri Setu (Sabroom Feni River International Gateway)",
        "river": "Feni",
        "state": "Tripura / Bangladesh Border",
        "coordinates": [
            23.0111,
            91.7333
        ],
        "structural_health": 98.0,
        "water_level_m": 18.2,
        "danger_mark_m": 22.0,
        "vulnerability_score": 15.0,
        "status": "operational"
    },
    {
        "id": "bridge_umiam",
        "name": "Umiam Dam Viaduct (NH-06 Shillong Expressway)",
        "river": "Umiam Lake",
        "state": "Meghalaya",
        "coordinates": [
            25.6583,
            91.8972
        ],
        "structural_health": 89.0,
        "water_level_m": 980.0,
        "danger_mark_m": 995.0,
        "vulnerability_score": 28.0,
        "status": "operational"
    },
    {
        "id": "bridge_dawki",
        "name": "Dawki Suspension Bridge (Umngot River)",
        "river": "Umngot",
        "state": "Meghalaya",
        "coordinates": [
            25.196,
            92.0195
        ],
        "structural_health": 74.0,
        "water_level_m": 24.5,
        "danger_mark_m": 28.0,
        "vulnerability_score": 62.0,
        "status": "operational"
    },
    {
        "id": "bridge_rangpo",
        "name": "Rangpo Gateway Bridge (Teesta Confluence)",
        "river": "Teesta / Rangpo",
        "state": "Sikkim",
        "coordinates": [
            27.178,
            88.529
        ],
        "structural_health": 85.0,
        "water_level_m": 310.0,
        "danger_mark_m": 325.0,
        "vulnerability_score": 45.0,
        "status": "operational"
    },
    {
        "id": "bridge_pasighat_siang",
        "name": "Ranaghat Siang Bridge (Pasighat)",
        "river": "Siang / Brahmaputra",
        "state": "Arunachal Pradesh",
        "coordinates": [
            28.0833,
            95.35
        ],
        "structural_health": 91.0,
        "water_level_m": 152.0,
        "danger_mark_m": 158.0,
        "vulnerability_score": 35.0,
        "status": "operational"
    },
    {
        "id": "bridge_jiribam",
        "name": "Barak River Jiribam Bridge",
        "river": "Barak",
        "state": "Manipur / Assam Border",
        "coordinates": [
            24.795,
            93.118
        ],
        "structural_health": 84.0,
        "water_level_m": 38.0,
        "danger_mark_m": 42.0,
        "vulnerability_score": 40.0,
        "status": "operational"
    },
    {
        "id": "bridge_loktak",
        "name": "Loktak Lake Causeway Bridge",
        "river": "Loktak Lake",
        "state": "Manipur",
        "coordinates": [
            24.52,
            93.79
        ],
        "structural_health": 92.0,
        "water_level_m": 768.0,
        "danger_mark_m": 772.0,
        "vulnerability_score": 25.0,
        "status": "operational"
    }
]

NER_ROAD_EDGES: List[Dict[str, Any]] = [
    {
        "id": "edge_siliguri_bongaigaon",
        "highway_code": "NH-27 (East-West Corridor Gateway)",
        "source": "node_siliguri",
        "target": "node_bongaigaon",
        "distance_km": 230.0,
        "avg_speed_kmh": 65.0,
        "elevation_gain_m": 40.0,
        "slope_deg": 2.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 6.0,
        "flood_risk": 14.0,
        "rainfall_mm": 18.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.7271,
                88.3953
            ],
            [
                26.6708,
                88.9363
            ],
            [
                26.6145,
                89.4774
            ],
            [
                26.5582,
                90.0184
            ],
            [
                26.5019,
                90.5594
            ]
        ]
    },
    {
        "id": "edge_siliguri_dhubri",
        "highway_code": "NH-17 (Gateway South Bank Trunk)",
        "source": "node_siliguri",
        "target": "node_dhubri",
        "distance_km": 210.0,
        "avg_speed_kmh": 60.0,
        "elevation_gain_m": 40.0,
        "slope_deg": 2.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 4.0,
        "flood_risk": 22.0,
        "rainfall_mm": 20.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.7271,
                88.3953
            ],
            [
                26.5857,
                88.8057
            ],
            [
                26.4161,
                89.2035
            ],
            [
                26.2254,
                89.5919
            ],
            [
                26.0207,
                89.974
            ]
        ]
    },
    {
        "id": "edge_siliguri_rangpo",
        "highway_code": "NH-10 (Sikkim Lifeline Teesta Gorge)",
        "source": "node_siliguri",
        "target": "node_rangpo",
        "distance_km": 75.0,
        "avg_speed_kmh": 40.0,
        "elevation_gain_m": 620.0,
        "slope_deg": 18.0,
        "terrain_type": "gorge",
        "status": "open",
        "landslide_risk": 32.0,
        "flood_risk": 35.0,
        "rainfall_mm": 52.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.7271,
                88.3953
            ],
            [
                26.8462,
                88.4092
            ],
            [
                26.9606,
                88.4389
            ],
            [
                27.0715,
                88.4805
            ],
            [
                27.18,
                88.53
            ]
        ]
    },
    {
        "id": "edge_dhubri_goalpara",
        "highway_code": "NH-17 (Lower Assam South Bank)",
        "source": "node_dhubri",
        "target": "node_goalpara",
        "distance_km": 78.0,
        "avg_speed_kmh": 55.0,
        "elevation_gain_m": 30.0,
        "slope_deg": 2.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 5.0,
        "flood_risk": 28.0,
        "rainfall_mm": 25.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.0207,
                89.974
            ],
            [
                26.0326,
                90.143
            ],
            [
                26.0659,
                90.307
            ],
            [
                26.1153,
                90.4671
            ],
            [
                26.1754,
                90.6247
            ]
        ]
    },
    {
        "id": "edge_bongaigaon_kokrajhar",
        "highway_code": "NH-27 (BTR Industrial Trunk)",
        "source": "node_bongaigaon",
        "target": "node_kokrajhar",
        "distance_km": 45.0,
        "avg_speed_kmh": 65.0,
        "elevation_gain_m": 20.0,
        "slope_deg": 1.5,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 3.0,
        "flood_risk": 12.0,
        "rainfall_mm": 15.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.5019,
                90.5594
            ],
            [
                26.5101,
                90.4758
            ],
            [
                26.4917,
                90.4014
            ],
            [
                26.4532,
                90.3341
            ],
            [
                26.4014,
                90.2714
            ]
        ]
    },
    {
        "id": "edge_kokrajhar_barpeta",
        "highway_code": "NH-27 (Lower Assam Expressway)",
        "source": "node_kokrajhar",
        "target": "node_barpeta",
        "distance_km": 95.0,
        "avg_speed_kmh": 65.0,
        "elevation_gain_m": 30.0,
        "slope_deg": 2.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 4.0,
        "flood_risk": 16.0,
        "rainfall_mm": 18.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.4014,
                90.2714
            ],
            [
                26.39,
                90.4557
            ],
            [
                26.3718,
                90.6392
            ],
            [
                26.3484,
                90.8222
            ],
            [
                26.3216,
                91.0048
            ]
        ]
    },
    {
        "id": "edge_bongaigaon_barpeta",
        "highway_code": "NH-27 (Bongaigaon-Barpeta Express)",
        "source": "node_bongaigaon",
        "target": "node_barpeta",
        "distance_km": 75.0,
        "avg_speed_kmh": 68.0,
        "elevation_gain_m": 25.0,
        "slope_deg": 1.8,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 4.0,
        "flood_risk": 15.0,
        "rainfall_mm": 16.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.5019,
                90.5594
            ],
            [
                26.4938,
                90.6857
            ],
            [
                26.4562,
                90.8001
            ],
            [
                26.3963,
                90.9054
            ],
            [
                26.3216,
                91.0048
            ]
        ]
    },
    {
        "id": "edge_goalpara_guwahati",
        "highway_code": "NH-17 (South Bank Guwahati Trunk)",
        "source": "node_goalpara",
        "target": "node_guwahati",
        "distance_km": 135.0,
        "avg_speed_kmh": 60.0,
        "elevation_gain_m": 45.0,
        "slope_deg": 2.5,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 5.0,
        "flood_risk": 20.0,
        "rainfall_mm": 22.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.1754,
                90.6247
            ],
            [
                26.1804,
                90.9029
            ],
            [
                26.1753,
                91.1809
            ],
            [
                26.1624,
                91.4586
            ],
            [
                26.1445,
                91.7362
            ]
        ]
    },
    {
        "id": "edge_goalpara_bongaigaon",
        "highway_code": "NH-117 (Naranarayan Setu Brahmaputra Link)",
        "source": "node_goalpara",
        "target": "node_bongaigaon",
        "distance_km": 48.0,
        "avg_speed_kmh": 55.0,
        "elevation_gain_m": 20.0,
        "slope_deg": 2.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 4.0,
        "flood_risk": 25.0,
        "rainfall_mm": 20.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.1754,
                90.6247
            ],
            [
                26.2635,
                90.6408
            ],
            [
                26.3464,
                90.631
            ],
            [
                26.4255,
                90.6017
            ],
            [
                26.5019,
                90.5594
            ]
        ]
    },
    {
        "id": "edge_barpeta_guwahati",
        "highway_code": "NH-27 (North Bank Highway)",
        "source": "node_barpeta",
        "target": "node_guwahati",
        "distance_km": 98.0,
        "avg_speed_kmh": 65.0,
        "elevation_gain_m": 35.0,
        "slope_deg": 2.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 6.0,
        "flood_risk": 18.0,
        "rainfall_mm": 19.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.3216,
                91.0048
            ],
            [
                26.2477,
                91.1805
            ],
            [
                26.1975,
                91.3619
            ],
            [
                26.1651,
                91.5476
            ],
            [
                26.1445,
                91.7362
            ]
        ]
    },
    {
        "id": "edge_guwahati_mangaldai",
        "highway_code": "NH-15 (North Bank Darrang Trunk)",
        "source": "node_guwahati",
        "target": "node_mangaldai",
        "distance_km": 68.0,
        "avg_speed_kmh": 58.0,
        "elevation_gain_m": 30.0,
        "slope_deg": 2.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 5.0,
        "flood_risk": 20.0,
        "rainfall_mm": 22.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.1445,
                91.7362
            ],
            [
                26.23,
                91.7987
            ],
            [
                26.306,
                91.8707
            ],
            [
                26.3748,
                91.9498
            ],
            [
                26.4388,
                92.0336
            ]
        ]
    },
    {
        "id": "edge_mangaldai_tezpur",
        "highway_code": "NH-15 (Darrang-Sonitpur Corridor)",
        "source": "node_mangaldai",
        "target": "node_tezpur",
        "distance_km": 90.0,
        "avg_speed_kmh": 62.0,
        "elevation_gain_m": 40.0,
        "slope_deg": 2.5,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 6.0,
        "flood_risk": 19.0,
        "rainfall_mm": 24.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.4388,
                92.0336
            ],
            [
                26.5303,
                92.2126
            ],
            [
                26.5914,
                92.4002
            ],
            [
                26.6297,
                92.5943
            ],
            [
                26.6528,
                92.7926
            ]
        ]
    },
    {
        "id": "edge_guwahati_nagaon",
        "highway_code": "NH-27 (Guwahati-Nagaon 4-Lane Corridor)",
        "source": "node_guwahati",
        "target": "node_nagaon",
        "distance_km": 122.0,
        "avg_speed_kmh": 70.0,
        "elevation_gain_m": 50.0,
        "slope_deg": 2.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 8.0,
        "flood_risk": 16.0,
        "rainfall_mm": 21.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.1445,
                91.7362
            ],
            [
                26.1989,
                91.9723
            ],
            [
                26.2499,
                92.2091
            ],
            [
                26.2984,
                92.4464
            ],
            [
                26.3452,
                92.6841
            ]
        ]
    },
    {
        "id": "edge_tezpur_nagaon",
        "highway_code": "NH-715 (Kolia Bhomora Setu Link)",
        "source": "node_tezpur",
        "target": "node_nagaon",
        "distance_km": 45.0,
        "avg_speed_kmh": 55.0,
        "elevation_gain_m": 35.0,
        "slope_deg": 2.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 6.0,
        "flood_risk": 28.0,
        "rainfall_mm": 26.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.6528,
                92.7926
            ],
            [
                26.5883,
                92.7304
            ],
            [
                26.5138,
                92.6963
            ],
            [
                26.432,
                92.6832
            ],
            [
                26.3452,
                92.6841
            ]
        ]
    },
    {
        "id": "edge_nagaon_golaghat",
        "highway_code": "NH-715 (Kaziranga Southern Bypass)",
        "source": "node_nagaon",
        "target": "node_golaghat",
        "distance_km": 145.0,
        "avg_speed_kmh": 58.0,
        "elevation_gain_m": 45.0,
        "slope_deg": 2.2,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 12.0,
        "flood_risk": 32.0,
        "rainfall_mm": 28.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.3452,
                92.6841
            ],
            [
                26.3641,
                93.008
            ],
            [
                26.4022,
                93.3292
            ],
            [
                26.4546,
                93.6486
            ],
            [
                26.5167,
                93.9667
            ]
        ]
    },
    {
        "id": "edge_golaghat_jorhat",
        "highway_code": "NH-715 (Upper Assam Trunk)",
        "source": "node_golaghat",
        "target": "node_jorhat",
        "distance_km": 48.0,
        "avg_speed_kmh": 60.0,
        "elevation_gain_m": 30.0,
        "slope_deg": 1.8,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 5.0,
        "flood_risk": 18.0,
        "rainfall_mm": 20.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.5167,
                93.9667
            ],
            [
                26.5925,
                94.0089
            ],
            [
                26.6545,
                94.0648
            ],
            [
                26.7061,
                94.1308
            ],
            [
                26.7509,
                94.2037
            ]
        ]
    },
    {
        "id": "edge_jorhat_sivasagar",
        "highway_code": "NH-02 (Ahom Heritage Corridor)",
        "source": "node_jorhat",
        "target": "node_sivasagar",
        "distance_km": 55.0,
        "avg_speed_kmh": 62.0,
        "elevation_gain_m": 35.0,
        "slope_deg": 1.5,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 4.0,
        "flood_risk": 16.0,
        "rainfall_mm": 22.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.7509,
                94.2037
            ],
            [
                26.8417,
                94.2961
            ],
            [
                26.9062,
                94.4023
            ],
            [
                26.951,
                94.5189
            ],
            [
                26.9826,
                94.6425
            ]
        ]
    },
    {
        "id": "edge_sivasagar_dibrugarh",
        "highway_code": "NH-02 (Upper Assam Expressway)",
        "source": "node_sivasagar",
        "target": "node_dibrugarh",
        "distance_km": 82.0,
        "avg_speed_kmh": 65.0,
        "elevation_gain_m": 40.0,
        "slope_deg": 1.8,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 5.0,
        "flood_risk": 20.0,
        "rainfall_mm": 25.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.9826,
                94.6425
            ],
            [
                27.1031,
                94.7137
            ],
            [
                27.2252,
                94.7818
            ],
            [
                27.3486,
                94.8477
            ],
            [
                27.4728,
                94.912
            ]
        ]
    },
    {
        "id": "edge_dibrugarh_tinsukia",
        "highway_code": "NH-37 (Dibrugarh-Tinsukia 4-Lane)",
        "source": "node_dibrugarh",
        "target": "node_tinsukia",
        "distance_km": 48.0,
        "avg_speed_kmh": 68.0,
        "elevation_gain_m": 25.0,
        "slope_deg": 1.5,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 4.0,
        "flood_risk": 18.0,
        "rainfall_mm": 20.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                27.4728,
                94.912
            ],
            [
                27.4382,
                95.0225
            ],
            [
                27.4352,
                95.1315
            ],
            [
                27.4558,
                95.2395
            ],
            [
                27.4922,
                95.3468
            ]
        ]
    },
    {
        "id": "edge_jorhat_majuli",
        "highway_code": "Brahmaputra Majuli Riverway / Bridge",
        "source": "node_jorhat",
        "target": "node_majuli",
        "distance_km": 28.0,
        "avg_speed_kmh": 35.0,
        "elevation_gain_m": 15.0,
        "slope_deg": 1.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 2.0,
        "flood_risk": 65.0,
        "rainfall_mm": 38.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.7509,
                94.2037
            ],
            [
                26.7996,
                94.2237
            ],
            [
                26.8491,
                94.2303
            ],
            [
                26.8994,
                94.2268
            ],
            [
                26.95,
                94.2167
            ]
        ]
    },
    {
        "id": "edge_north_lakhimpur_majuli",
        "highway_code": "NH-715A (Lakhimpur-Majuli Viaduct)",
        "source": "node_north_lakhimpur",
        "target": "node_majuli",
        "distance_km": 42.0,
        "avg_speed_kmh": 45.0,
        "elevation_gain_m": 20.0,
        "slope_deg": 1.2,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 3.0,
        "flood_risk": 55.0,
        "rainfall_mm": 34.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                27.2346,
                94.1037
            ],
            [
                27.1747,
                94.1603
            ],
            [
                27.1058,
                94.1942
            ],
            [
                27.0302,
                94.2111
            ],
            [
                26.95,
                94.2167
            ]
        ]
    },
    {
        "id": "edge_tezpur_north_lakhimpur",
        "highway_code": "NH-15 (Biswanath-Lakhimpur Highway)",
        "source": "node_tezpur",
        "target": "node_north_lakhimpur",
        "distance_km": 165.0,
        "avg_speed_kmh": 58.0,
        "elevation_gain_m": 55.0,
        "slope_deg": 2.2,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 8.0,
        "flood_risk": 25.0,
        "rainfall_mm": 30.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.6528,
                92.7926
            ],
            [
                26.8285,
                93.107
            ],
            [
                26.98,
                93.432
            ],
            [
                27.1133,
                93.7652
            ],
            [
                27.2346,
                94.1037
            ]
        ]
    },
    {
        "id": "edge_north_lakhimpur_dhemaji",
        "highway_code": "NH-15 (Subansiri Flood Basin Trunk)",
        "source": "node_north_lakhimpur",
        "target": "node_dhemaji",
        "distance_km": 65.0,
        "avg_speed_kmh": 55.0,
        "elevation_gain_m": 30.0,
        "slope_deg": 1.8,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 7.0,
        "flood_risk": 48.0,
        "rainfall_mm": 35.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                27.2346,
                94.1037
            ],
            [
                27.2854,
                94.2295
            ],
            [
                27.3453,
                94.3506
            ],
            [
                27.412,
                94.4681
            ],
            [
                27.4833,
                94.5833
            ]
        ]
    },
    {
        "id": "edge_dhemaji_dibrugarh",
        "highway_code": "NH-15 (Bogibeel Brahmaputra Bridge)",
        "source": "node_dhemaji",
        "target": "node_dibrugarh",
        "distance_km": 52.0,
        "avg_speed_kmh": 65.0,
        "elevation_gain_m": 35.0,
        "slope_deg": 1.5,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 4.0,
        "flood_risk": 35.0,
        "rainfall_mm": 28.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                27.4833,
                94.5833
            ],
            [
                27.4408,
                94.6642
            ],
            [
                27.4301,
                94.7461
            ],
            [
                27.4435,
                94.8288
            ],
            [
                27.4728,
                94.912
            ]
        ]
    },
    {
        "id": "edge_dhemaji_pasighat",
        "highway_code": "NH-515 (Jonai-Pasighat Border Highway)",
        "source": "node_dhemaji",
        "target": "node_pasighat",
        "distance_km": 95.0,
        "avg_speed_kmh": 55.0,
        "elevation_gain_m": 110.0,
        "slope_deg": 4.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 18.0,
        "flood_risk": 28.0,
        "rainfall_mm": 38.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                27.4833,
                94.5833
            ],
            [
                27.6224,
                94.7761
            ],
            [
                27.7669,
                94.9646
            ],
            [
                27.9154,
                95.15
            ],
            [
                28.0667,
                95.3333
            ]
        ]
    },
    {
        "id": "edge_tinsukia_tezu",
        "highway_code": "NH-115 (Bhupen Hazarika Setu Dhola-Sadiya)",
        "source": "node_tinsukia",
        "target": "node_tezu",
        "distance_km": 115.0,
        "avg_speed_kmh": 60.0,
        "elevation_gain_m": 140.0,
        "slope_deg": 3.5,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 14.0,
        "flood_risk": 30.0,
        "rainfall_mm": 32.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                27.4922,
                95.3468
            ],
            [
                27.6297,
                95.5355
            ],
            [
                27.7421,
                95.7372
            ],
            [
                27.8357,
                95.9487
            ],
            [
                27.9167,
                96.1667
            ]
        ]
    },
    {
        "id": "edge_tinsukia_namsai",
        "highway_code": "NH-15 (Doomdooma-Namsai Gateway)",
        "source": "node_tinsukia",
        "target": "node_namsai",
        "distance_km": 75.0,
        "avg_speed_kmh": 58.0,
        "elevation_gain_m": 80.0,
        "slope_deg": 2.5,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 8.0,
        "flood_risk": 22.0,
        "rainfall_mm": 28.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                27.4922,
                95.3468
            ],
            [
                27.5619,
                95.468
            ],
            [
                27.6107,
                95.5963
            ],
            [
                27.6439,
                95.7297
            ],
            [
                27.6667,
                95.8667
            ]
        ]
    },
    {
        "id": "edge_namsai_tezu",
        "highway_code": "NH-15 (Golden Pagoda-Lohit Trunk)",
        "source": "node_namsai",
        "target": "node_tezu",
        "distance_km": 48.0,
        "avg_speed_kmh": 55.0,
        "elevation_gain_m": 95.0,
        "slope_deg": 3.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 12.0,
        "flood_risk": 20.0,
        "rainfall_mm": 30.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                27.6667,
                95.8667
            ],
            [
                27.7133,
                95.9549
            ],
            [
                27.7727,
                96.0326
            ],
            [
                27.8415,
                96.1023
            ],
            [
                27.9167,
                96.1667
            ]
        ]
    },
    {
        "id": "edge_namsai_roing",
        "highway_code": "NH-13 (Namsai-Chowkham-Roing Corridor)",
        "source": "node_namsai",
        "target": "node_roing",
        "distance_km": 82.0,
        "avg_speed_kmh": 52.0,
        "elevation_gain_m": 130.0,
        "slope_deg": 4.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 16.0,
        "flood_risk": 24.0,
        "rainfall_mm": 34.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                27.6667,
                95.8667
            ],
            [
                27.7874,
                95.8975
            ],
            [
                27.906,
                95.8975
            ],
            [
                28.0232,
                95.8745
            ],
            [
                28.1394,
                95.8361
            ]
        ]
    },
    {
        "id": "edge_tezu_roing",
        "highway_code": "NH-13 (Trans-Arunachal Lohit-Dibang Trunk)",
        "source": "node_tezu",
        "target": "node_roing",
        "distance_km": 65.0,
        "avg_speed_kmh": 50.0,
        "elevation_gain_m": 140.0,
        "slope_deg": 4.5,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 19.0,
        "flood_risk": 26.0,
        "rainfall_mm": 36.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                27.9167,
                96.1667
            ],
            [
                27.9723,
                96.084
            ],
            [
                28.028,
                96.0014
            ],
            [
                28.0837,
                95.9187
            ],
            [
                28.1394,
                95.8361
            ]
        ]
    },
    {
        "id": "edge_roing_pasighat",
        "highway_code": "NH-13 (Dibang-Siang River Highway)",
        "source": "node_roing",
        "target": "node_pasighat",
        "distance_km": 58.0,
        "avg_speed_kmh": 50.0,
        "elevation_gain_m": 120.0,
        "slope_deg": 3.8,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 15.0,
        "flood_risk": 32.0,
        "rainfall_mm": 35.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                28.1394,
                95.8361
            ],
            [
                28.0831,
                95.7159
            ],
            [
                28.0573,
                95.5913
            ],
            [
                28.0544,
                95.4634
            ],
            [
                28.0667,
                95.3333
            ]
        ]
    },
    {
        "id": "edge_pasighat_along",
        "highway_code": "NH-13 (Siang Gorge Mountain Corridor)",
        "source": "node_pasighat",
        "target": "node_along",
        "distance_km": 102.0,
        "avg_speed_kmh": 42.0,
        "elevation_gain_m": 540.0,
        "slope_deg": 14.0,
        "terrain_type": "gorge",
        "status": "open",
        "landslide_risk": 45.0,
        "flood_risk": 28.0,
        "rainfall_mm": 48.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                28.0667,
                95.3333
            ],
            [
                28.0725,
                95.1967
            ],
            [
                28.0944,
                95.0633
            ],
            [
                28.1285,
                94.9323
            ],
            [
                28.1706,
                94.8028
            ]
        ]
    },
    {
        "id": "edge_along_ziro",
        "highway_code": "NH-13 (Daporijo-Ziro Central Hill Highway)",
        "source": "node_along",
        "target": "node_ziro",
        "distance_km": 185.0,
        "avg_speed_kmh": 38.0,
        "elevation_gain_m": 850.0,
        "slope_deg": 16.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 28.0,
        "flood_risk": 22.0,
        "rainfall_mm": 45.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                28.1706,
                94.8028
            ],
            [
                28.0503,
                94.5466
            ],
            [
                27.9112,
                94.3017
            ],
            [
                27.7578,
                94.0652
            ],
            [
                27.5949,
                93.8344
            ]
        ]
    },
    {
        "id": "edge_ziro_north_lakhimpur",
        "highway_code": "NH-229 (Raga-Potin Foothill Bypass)",
        "source": "node_ziro",
        "target": "node_north_lakhimpur",
        "distance_km": 98.0,
        "avg_speed_kmh": 45.0,
        "elevation_gain_m": 720.0,
        "slope_deg": 15.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 42.0,
        "flood_risk": 25.0,
        "rainfall_mm": 40.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                27.5949,
                93.8344
            ],
            [
                27.4837,
                93.8734
            ],
            [
                27.3894,
                93.9351
            ],
            [
                27.3078,
                94.0137
            ],
            [
                27.2346,
                94.1037
            ]
        ]
    },
    {
        "id": "edge_ziro_naharlagun",
        "highway_code": "NH-13 (Yachuli-Potin-Naharlagun)",
        "source": "node_ziro",
        "target": "node_naharlagun",
        "distance_km": 110.0,
        "avg_speed_kmh": 44.0,
        "elevation_gain_m": 680.0,
        "slope_deg": 14.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 38.0,
        "flood_risk": 24.0,
        "rainfall_mm": 38.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                27.5949,
                93.8344
            ],
            [
                27.4699,
                93.8075
            ],
            [
                27.3468,
                93.7739
            ],
            [
                27.2251,
                93.7353
            ],
            [
                27.1044,
                93.6934
            ]
        ]
    },
    {
        "id": "edge_naharlagun_itanagar",
        "highway_code": "NH-415 (Twin Capital Express Highway)",
        "source": "node_naharlagun",
        "target": "node_itanagar",
        "distance_km": 15.0,
        "avg_speed_kmh": 50.0,
        "elevation_gain_m": 120.0,
        "slope_deg": 5.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 12.0,
        "flood_risk": 15.0,
        "rainfall_mm": 25.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                27.1044,
                93.6934
            ],
            [
                27.0604,
                93.6802
            ],
            [
                27.0477,
                93.66
            ],
            [
                27.0582,
                93.6344
            ],
            [
                27.0844,
                93.6053
            ]
        ]
    },
    {
        "id": "edge_naharlagun_tezpur",
        "highway_code": "NH-15 (Banderdewa Gateway)",
        "source": "node_naharlagun",
        "target": "node_tezpur",
        "distance_km": 145.0,
        "avg_speed_kmh": 60.0,
        "elevation_gain_m": 180.0,
        "slope_deg": 3.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 10.0,
        "flood_risk": 22.0,
        "rainfall_mm": 28.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                27.1044,
                93.6934
            ],
            [
                26.9801,
                93.4739
            ],
            [
                26.8649,
                93.2498
            ],
            [
                26.7566,
                93.0224
            ],
            [
                26.6528,
                92.7926
            ]
        ]
    },
    {
        "id": "edge_tezpur_bhalukpong",
        "highway_code": "NH-13 (Arunachal Western Entry Gateway)",
        "source": "node_tezpur",
        "target": "node_bhalukpong",
        "distance_km": 62.0,
        "avg_speed_kmh": 52.0,
        "elevation_gain_m": 180.0,
        "slope_deg": 4.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 14.0,
        "flood_risk": 18.0,
        "rainfall_mm": 32.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.6528,
                92.7926
            ],
            [
                26.7556,
                92.7866
            ],
            [
                26.8483,
                92.756
            ],
            [
                26.9336,
                92.7071
            ],
            [
                27.0139,
                92.6458
            ]
        ]
    },
    {
        "id": "edge_bhalukpong_bomdila",
        "highway_code": "NH-13 (Tenga Valley Hill Highway)",
        "source": "node_bhalukpong",
        "target": "node_bomdila",
        "distance_km": 98.0,
        "avg_speed_kmh": 38.0,
        "elevation_gain_m": 1450.0,
        "slope_deg": 22.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 48.0,
        "flood_risk": 16.0,
        "rainfall_mm": 42.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                27.0139,
                92.6458
            ],
            [
                27.0968,
                92.6126
            ],
            [
                27.1635,
                92.5613
            ],
            [
                27.218,
                92.4963
            ],
            [
                27.2644,
                92.4222
            ]
        ]
    },
    {
        "id": "edge_bomdila_dirang",
        "highway_code": "NH-13 (Bomdila-Dirang River Corridor)",
        "source": "node_bomdila",
        "target": "node_dirang",
        "distance_km": 42.0,
        "avg_speed_kmh": 40.0,
        "elevation_gain_m": 420.0,
        "slope_deg": 12.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 35.0,
        "flood_risk": 14.0,
        "rainfall_mm": 36.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                27.2644,
                92.4222
            ],
            [
                27.2727,
                92.3691
            ],
            [
                27.293,
                92.322
            ],
            [
                27.3222,
                92.2796
            ],
            [
                27.3575,
                92.2403
            ]
        ]
    },
    {
        "id": "edge_dirang_tawang",
        "highway_code": "NH-13 (Sela Tunnel High Altitude Corridor)",
        "source": "node_dirang",
        "target": "node_tawang",
        "distance_km": 135.0,
        "avg_speed_kmh": 35.0,
        "elevation_gain_m": 2100.0,
        "slope_deg": 26.0,
        "terrain_type": "gorge",
        "status": "open",
        "landslide_risk": 28.0,
        "flood_risk": 12.0,
        "rainfall_mm": 48.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                27.3575,
                92.2403
            ],
            [
                27.3808,
                92.1248
            ],
            [
                27.4312,
                92.0255
            ],
            [
                27.5019,
                91.9384
            ],
            [
                27.5861,
                91.8594
            ]
        ]
    },
    {
        "id": "edge_nagaon_diphu",
        "highway_code": "NH-329 (Karbi Hills Access Highway)",
        "source": "node_nagaon",
        "target": "node_diphu",
        "distance_km": 115.0,
        "avg_speed_kmh": 52.0,
        "elevation_gain_m": 220.0,
        "slope_deg": 6.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 22.0,
        "flood_risk": 18.0,
        "rainfall_mm": 26.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.3452,
                92.6841
            ],
            [
                26.2239,
                92.8734
            ],
            [
                26.0997,
                93.0608
            ],
            [
                25.9733,
                93.2468
            ],
            [
                25.8456,
                93.4319
            ]
        ]
    },
    {
        "id": "edge_diphu_dimapur",
        "highway_code": "NH-39 (Diphu-Dimapur Inter-State Link)",
        "source": "node_diphu",
        "target": "node_dimapur",
        "distance_km": 48.0,
        "avg_speed_kmh": 58.0,
        "elevation_gain_m": 90.0,
        "slope_deg": 3.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 8.0,
        "flood_risk": 15.0,
        "rainfall_mm": 22.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.8456,
                93.4319
            ],
            [
                25.8243,
                93.5131
            ],
            [
                25.8321,
                93.5884
            ],
            [
                25.8618,
                93.6592
            ],
            [
                25.906,
                93.727
            ]
        ]
    },
    {
        "id": "edge_nagaon_haflong",
        "highway_code": "NH-27 (Lumding-Haflong Mountain Sector)",
        "source": "node_nagaon",
        "target": "node_haflong",
        "distance_km": 175.0,
        "avg_speed_kmh": 45.0,
        "elevation_gain_m": 680.0,
        "slope_deg": 14.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 45.0,
        "flood_risk": 22.0,
        "rainfall_mm": 44.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.3452,
                92.6841
            ],
            [
                26.0463,
                92.7446
            ],
            [
                25.7528,
                92.8236
            ],
            [
                25.4633,
                92.9166
            ],
            [
                25.1764,
                93.0189
            ]
        ]
    },
    {
        "id": "edge_diphu_haflong",
        "highway_code": "SH-20 (Lumding Forest Corridor)",
        "source": "node_diphu",
        "target": "node_haflong",
        "distance_km": 112.0,
        "avg_speed_kmh": 42.0,
        "elevation_gain_m": 520.0,
        "slope_deg": 12.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 38.0,
        "flood_risk": 20.0,
        "rainfall_mm": 35.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.8456,
                93.4319
            ],
            [
                25.6656,
                93.3493
            ],
            [
                25.4957,
                93.2502
            ],
            [
                25.3335,
                93.1387
            ],
            [
                25.1764,
                93.0189
            ]
        ]
    },
    {
        "id": "edge_haflong_silchar",
        "highway_code": "NH-27 (Jatinga Valley Debris Sector)",
        "source": "node_haflong",
        "target": "node_silchar",
        "distance_km": 102.0,
        "avg_speed_kmh": 38.0,
        "elevation_gain_m": 480.0,
        "slope_deg": 18.0,
        "terrain_type": "gorge",
        "status": "open",
        "landslide_risk": 32.0,
        "flood_risk": 32.0,
        "rainfall_mm": 65.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.1764,
                93.0189
            ],
            [
                25.0693,
                92.9893
            ],
            [
                24.9793,
                92.9354
            ],
            [
                24.902,
                92.8632
            ],
            [
                24.8333,
                92.7789
            ]
        ]
    },
    {
        "id": "edge_silchar_karimganj",
        "highway_code": "NH-37 (Cachar-Karimganj Trunk)",
        "source": "node_silchar",
        "target": "node_karimganj",
        "distance_km": 55.0,
        "avg_speed_kmh": 55.0,
        "elevation_gain_m": 40.0,
        "slope_deg": 2.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 6.0,
        "flood_risk": 35.0,
        "rainfall_mm": 32.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                24.8333,
                92.7789
            ],
            [
                24.8467,
                92.6743
            ],
            [
                24.8565,
                92.5695
            ],
            [
                24.8638,
                92.4644
            ],
            [
                24.8693,
                92.3592
            ]
        ]
    },
    {
        "id": "edge_karimganj_hailakandi",
        "highway_code": "NH-154 (Barak Valley Inter-District Link)",
        "source": "node_karimganj",
        "target": "node_hailakandi",
        "distance_km": 38.0,
        "avg_speed_kmh": 52.0,
        "elevation_gain_m": 35.0,
        "slope_deg": 1.8,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 5.0,
        "flood_risk": 32.0,
        "rainfall_mm": 28.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                24.8693,
                92.3592
            ],
            [
                24.7934,
                92.3847
            ],
            [
                24.741,
                92.4313
            ],
            [
                24.7063,
                92.4937
            ],
            [
                24.6833,
                92.5667
            ]
        ]
    },
    {
        "id": "edge_hailakandi_silchar",
        "highway_code": "SH-33 (Hailakandi Direct Corridor)",
        "source": "node_hailakandi",
        "target": "node_silchar",
        "distance_km": 42.0,
        "avg_speed_kmh": 52.0,
        "elevation_gain_m": 30.0,
        "slope_deg": 1.5,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 5.0,
        "flood_risk": 34.0,
        "rainfall_mm": 30.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                24.6833,
                92.5667
            ],
            [
                24.7071,
                92.6294
            ],
            [
                24.7419,
                92.6844
            ],
            [
                24.7849,
                92.7336
            ],
            [
                24.8333,
                92.7789
            ]
        ]
    },
    {
        "id": "edge_silchar_jiribam",
        "highway_code": "NH-37 (Barak-Manipur Western Lifeline)",
        "source": "node_silchar",
        "target": "node_jiribam",
        "distance_km": 52.0,
        "avg_speed_kmh": 50.0,
        "elevation_gain_m": 120.0,
        "slope_deg": 5.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 22.0,
        "flood_risk": 35.0,
        "rainfall_mm": 36.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                24.8333,
                92.7789
            ],
            [
                24.8554,
                92.8671
            ],
            [
                24.8531,
                92.953
            ],
            [
                24.8326,
                93.0371
            ],
            [
                24.8,
                93.12
            ]
        ]
    },
    {
        "id": "edge_guwahati_nongpoh",
        "highway_code": "NH-06 (Guwahati-Shillong 4-Lane Expressway)",
        "source": "node_guwahati",
        "target": "node_nongpoh",
        "distance_km": 52.0,
        "avg_speed_kmh": 65.0,
        "elevation_gain_m": 380.0,
        "slope_deg": 8.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 18.0,
        "flood_risk": 10.0,
        "rainfall_mm": 30.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.1445,
                91.7362
            ],
            [
                26.1013,
                91.8007
            ],
            [
                26.0445,
                91.8424
            ],
            [
                25.9774,
                91.8672
            ],
            [
                25.9036,
                91.8806
            ]
        ]
    },
    {
        "id": "edge_nongpoh_shillong",
        "highway_code": "NH-06 (Umiam Viaduct Mountain Corridor)",
        "source": "node_nongpoh",
        "target": "node_shillong",
        "distance_km": 48.0,
        "avg_speed_kmh": 55.0,
        "elevation_gain_m": 850.0,
        "slope_deg": 16.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 32.0,
        "flood_risk": 8.0,
        "rainfall_mm": 38.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.9036,
                91.8806
            ],
            [
                25.8219,
                91.871
            ],
            [
                25.7406,
                91.8716
            ],
            [
                25.6596,
                91.8799
            ],
            [
                25.5788,
                91.8933
            ]
        ]
    },
    {
        "id": "edge_shillong_cherrapunji",
        "highway_code": "SH-05 (Sohra Plateau Scenic Highway)",
        "source": "node_shillong",
        "target": "node_cherrapunji",
        "distance_km": 54.0,
        "avg_speed_kmh": 48.0,
        "elevation_gain_m": 420.0,
        "slope_deg": 10.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 28.0,
        "flood_risk": 12.0,
        "rainfall_mm": 85.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.5788,
                91.8933
            ],
            [
                25.5203,
                91.8172
            ],
            [
                25.4468,
                91.7693
            ],
            [
                25.3621,
                91.7426
            ],
            [
                25.27,
                91.73
            ]
        ]
    },
    {
        "id": "edge_shillong_dawki",
        "highway_code": "NH-206 (Pynursla-Dawki Border Highway)",
        "source": "node_shillong",
        "target": "node_dawki",
        "distance_km": 82.0,
        "avg_speed_kmh": 45.0,
        "elevation_gain_m": 680.0,
        "slope_deg": 14.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 42.0,
        "flood_risk": 15.0,
        "rainfall_mm": 62.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.5788,
                91.8933
            ],
            [
                25.4802,
                91.9166
            ],
            [
                25.3837,
                91.9464
            ],
            [
                25.2888,
                91.9811
            ],
            [
                25.195,
                92.019
            ]
        ]
    },
    {
        "id": "edge_dawki_jowai",
        "highway_code": "NH-206 (Amlarem-Jowai Ridge Highway)",
        "source": "node_dawki",
        "target": "node_jowai",
        "distance_km": 58.0,
        "avg_speed_kmh": 45.0,
        "elevation_gain_m": 720.0,
        "slope_deg": 15.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 35.0,
        "flood_risk": 18.0,
        "rainfall_mm": 55.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.195,
                92.019
            ],
            [
                25.2792,
                92.0354
            ],
            [
                25.3471,
                92.0749
            ],
            [
                25.4026,
                92.1317
            ],
            [
                25.45,
                92.2
            ]
        ]
    },
    {
        "id": "edge_shillong_jowai",
        "highway_code": "NH-06 (East-West Khasi-Jaintia Trunk)",
        "source": "node_shillong",
        "target": "node_jowai",
        "distance_km": 65.0,
        "avg_speed_kmh": 55.0,
        "elevation_gain_m": 350.0,
        "slope_deg": 8.0,
        "terrain_type": "plateau",
        "status": "open",
        "landslide_risk": 15.0,
        "flood_risk": 12.0,
        "rainfall_mm": 35.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.5788,
                91.8933
            ],
            [
                25.5719,
                91.9806
            ],
            [
                25.5448,
                92.0594
            ],
            [
                25.5025,
                92.1318
            ],
            [
                25.45,
                92.2
            ]
        ]
    },
    {
        "id": "edge_shillong_mairang",
        "highway_code": "NH-106 (Central Khasi Hill Corridor)",
        "source": "node_shillong",
        "target": "node_mairang",
        "distance_km": 45.0,
        "avg_speed_kmh": 50.0,
        "elevation_gain_m": 480.0,
        "slope_deg": 9.0,
        "terrain_type": "plateau",
        "status": "open",
        "landslide_risk": 18.0,
        "flood_risk": 10.0,
        "rainfall_mm": 32.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.5788,
                91.8933
            ],
            [
                25.5947,
                91.8284
            ],
            [
                25.5941,
                91.7648
            ],
            [
                25.5812,
                91.7021
            ],
            [
                25.56,
                91.64
            ]
        ]
    },
    {
        "id": "edge_mairang_tura",
        "highway_code": "NH-127B (West Khasi to Garo Hills Arterial)",
        "source": "node_mairang",
        "target": "node_tura",
        "distance_km": 175.0,
        "avg_speed_kmh": 45.0,
        "elevation_gain_m": 650.0,
        "slope_deg": 12.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 38.0,
        "flood_risk": 16.0,
        "rainfall_mm": 42.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.56,
                91.64
            ],
            [
                25.5871,
                91.2794
            ],
            [
                25.5834,
                90.9198
            ],
            [
                25.5566,
                90.5609
            ],
            [
                25.5144,
                90.2025
            ]
        ]
    },
    {
        "id": "edge_goalpara_tura",
        "highway_code": "NH-217 (Phulbari-Tura Western Foothill)",
        "source": "node_goalpara",
        "target": "node_tura",
        "distance_km": 98.0,
        "avg_speed_kmh": 55.0,
        "elevation_gain_m": 180.0,
        "slope_deg": 4.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 14.0,
        "flood_risk": 22.0,
        "rainfall_mm": 28.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.1754,
                90.6247
            ],
            [
                26.0101,
                90.5192
            ],
            [
                25.8449,
                90.4137
            ],
            [
                25.6796,
                90.3081
            ],
            [
                25.5144,
                90.2025
            ]
        ]
    },
    {
        "id": "edge_tura_williamnagar",
        "highway_code": "SH-12 (Central Garo Hills Corridor)",
        "source": "node_tura",
        "target": "node_williamnagar",
        "distance_km": 75.0,
        "avg_speed_kmh": 48.0,
        "elevation_gain_m": 240.0,
        "slope_deg": 6.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 18.0,
        "flood_risk": 18.0,
        "rainfall_mm": 32.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.5144,
                90.2025
            ],
            [
                25.5479,
                90.3089
            ],
            [
                25.5506,
                90.4139
            ],
            [
                25.5302,
                90.5177
            ],
            [
                25.4944,
                90.6208
            ]
        ]
    },
    {
        "id": "edge_williamnagar_baghmara",
        "highway_code": "SH-04 (Simsang River Gorge Highway)",
        "source": "node_williamnagar",
        "target": "node_baghmara",
        "distance_km": 82.0,
        "avg_speed_kmh": 42.0,
        "elevation_gain_m": 350.0,
        "slope_deg": 9.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 28.0,
        "flood_risk": 24.0,
        "rainfall_mm": 38.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.4944,
                90.6208
            ],
            [
                25.4217,
                90.6445
            ],
            [
                25.3482,
                90.6517
            ],
            [
                25.2743,
                90.6466
            ],
            [
                25.2,
                90.6333
            ]
        ]
    },
    {
        "id": "edge_tura_baghmara",
        "highway_code": "NH-62 (South Garo Border Highway)",
        "source": "node_tura",
        "target": "node_baghmara",
        "distance_km": 115.0,
        "avg_speed_kmh": 44.0,
        "elevation_gain_m": 280.0,
        "slope_deg": 7.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 22.0,
        "flood_risk": 26.0,
        "rainfall_mm": 35.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.5144,
                90.2025
            ],
            [
                25.4135,
                90.294
            ],
            [
                25.3305,
                90.3984
            ],
            [
                25.2608,
                90.5126
            ],
            [
                25.2,
                90.6333
            ]
        ]
    },
    {
        "id": "edge_jowai_silchar",
        "highway_code": "NH-06 (Khliehriat-Malidor Lifeline)",
        "source": "node_jowai",
        "target": "node_silchar",
        "distance_km": 135.0,
        "avg_speed_kmh": 42.0,
        "elevation_gain_m": 620.0,
        "slope_deg": 16.0,
        "terrain_type": "gorge",
        "status": "open",
        "landslide_risk": 30.0,
        "flood_risk": 25.0,
        "rainfall_mm": 58.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.45,
                92.2
            ],
            [
                25.2717,
                92.319
            ],
            [
                25.1127,
                92.4586
            ],
            [
                24.9681,
                92.6136
            ],
            [
                24.8333,
                92.7789
            ]
        ]
    },
    {
        "id": "edge_jowai_haflong",
        "highway_code": "Umrangso Hill Bypass Corridor",
        "source": "node_jowai",
        "target": "node_haflong",
        "distance_km": 125.0,
        "avg_speed_kmh": 40.0,
        "elevation_gain_m": 580.0,
        "slope_deg": 14.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 45.0,
        "flood_risk": 20.0,
        "rainfall_mm": 45.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.45,
                92.2
            ],
            [
                25.3898,
                92.4075
            ],
            [
                25.3231,
                92.6127
            ],
            [
                25.2514,
                92.8164
            ],
            [
                25.1764,
                93.0189
            ]
        ]
    },
    {
        "id": "edge_dimapur_kohima",
        "highway_code": "NH-29 (Nagaland 4-Lane Mountain Lifeline)",
        "source": "node_dimapur",
        "target": "node_kohima",
        "distance_km": 74.0,
        "avg_speed_kmh": 48.0,
        "elevation_gain_m": 1150.0,
        "slope_deg": 22.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 26.0,
        "flood_risk": 14.0,
        "rainfall_mm": 42.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.906,
                93.727
            ],
            [
                25.8825,
                93.8431
            ],
            [
                25.8316,
                93.9426
            ],
            [
                25.7602,
                94.0297
            ],
            [
                25.6751,
                94.1086
            ]
        ]
    },
    {
        "id": "edge_golaghat_dimapur",
        "highway_code": "NH-39 (Assam-Nagaland Industrial Gateway)",
        "source": "node_golaghat",
        "target": "node_dimapur",
        "distance_km": 78.0,
        "avg_speed_kmh": 60.0,
        "elevation_gain_m": 80.0,
        "slope_deg": 2.5,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 8.0,
        "flood_risk": 18.0,
        "rainfall_mm": 22.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.5167,
                93.9667
            ],
            [
                26.3594,
                93.9186
            ],
            [
                26.2058,
                93.861
            ],
            [
                26.055,
                93.7964
            ],
            [
                25.906,
                93.727
            ]
        ]
    },
    {
        "id": "edge_jorhat_mokokchung",
        "highway_code": "NH-702 (Mariani-Mokokchung Hill Cut)",
        "source": "node_jorhat",
        "target": "node_mokokchung",
        "distance_km": 85.0,
        "avg_speed_kmh": 42.0,
        "elevation_gain_m": 980.0,
        "slope_deg": 18.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 48.0,
        "flood_risk": 12.0,
        "rainfall_mm": 38.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.7509,
                94.2037
            ],
            [
                26.6248,
                94.2552
            ],
            [
                26.5144,
                94.328
            ],
            [
                26.4157,
                94.4169
            ],
            [
                26.3249,
                94.5165
            ]
        ]
    },
    {
        "id": "edge_dimapur_peren",
        "highway_code": "NH-129A (Jalukie Agricultural Valley)",
        "source": "node_dimapur",
        "target": "node_peren",
        "distance_km": 68.0,
        "avg_speed_kmh": 50.0,
        "elevation_gain_m": 420.0,
        "slope_deg": 9.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 22.0,
        "flood_risk": 15.0,
        "rainfall_mm": 28.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.906,
                93.727
            ],
            [
                25.8085,
                93.6998
            ],
            [
                25.7118,
                93.697
            ],
            [
                25.6157,
                93.7124
            ],
            [
                25.52,
                93.74
            ]
        ]
    },
    {
        "id": "edge_peren_haflong",
        "highway_code": "Inter-State Hill Pass (Mahur Link)",
        "source": "node_peren",
        "target": "node_haflong",
        "distance_km": 95.0,
        "avg_speed_kmh": 38.0,
        "elevation_gain_m": 620.0,
        "slope_deg": 15.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 42.0,
        "flood_risk": 18.0,
        "rainfall_mm": 38.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.52,
                93.74
            ],
            [
                25.4189,
                93.567
            ],
            [
                25.3299,
                93.3882
            ],
            [
                25.2501,
                93.205
            ],
            [
                25.1764,
                93.0189
            ]
        ]
    },
    {
        "id": "edge_kohima_peren",
        "highway_code": "State Highway 14 (South Nagaland Ridge)",
        "source": "node_kohima",
        "target": "node_peren",
        "distance_km": 58.0,
        "avg_speed_kmh": 42.0,
        "elevation_gain_m": 580.0,
        "slope_deg": 12.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 28.0,
        "flood_risk": 12.0,
        "rainfall_mm": 32.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.6751,
                94.1086
            ],
            [
                25.6,
                94.0318
            ],
            [
                25.5539,
                93.9427
            ],
            [
                25.5297,
                93.8444
            ],
            [
                25.52,
                93.74
            ]
        ]
    },
    {
        "id": "edge_kohima_wokha",
        "highway_code": "NH-02 (Tseminyu-Wokha Mountain Highway)",
        "source": "node_kohima",
        "target": "node_wokha",
        "distance_km": 80.0,
        "avg_speed_kmh": 44.0,
        "elevation_gain_m": 680.0,
        "slope_deg": 14.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 35.0,
        "flood_risk": 15.0,
        "rainfall_mm": 35.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.6751,
                94.1086
            ],
            [
                25.7827,
                94.1425
            ],
            [
                25.8893,
                94.1795
            ],
            [
                25.9949,
                94.219
            ],
            [
                26.1,
                94.26
            ]
        ]
    },
    {
        "id": "edge_wokha_mokokchung",
        "highway_code": "NH-02 (Lotha-Ao Mountain Trunk)",
        "source": "node_wokha",
        "target": "node_mokokchung",
        "distance_km": 72.0,
        "avg_speed_kmh": 45.0,
        "elevation_gain_m": 520.0,
        "slope_deg": 12.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 32.0,
        "flood_risk": 12.0,
        "rainfall_mm": 34.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.1,
                94.26
            ],
            [
                26.1283,
                94.3486
            ],
            [
                26.1789,
                94.4177
            ],
            [
                26.2463,
                94.472
            ],
            [
                26.3249,
                94.5165
            ]
        ]
    },
    {
        "id": "edge_mokokchung_zunheboto",
        "highway_code": "SH-12 (Central Ridge Road)",
        "source": "node_mokokchung",
        "target": "node_zunheboto",
        "distance_km": 65.0,
        "avg_speed_kmh": 38.0,
        "elevation_gain_m": 780.0,
        "slope_deg": 16.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 44.0,
        "flood_risk": 10.0,
        "rainfall_mm": 38.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.3249,
                94.5165
            ],
            [
                26.2359,
                94.4932
            ],
            [
                26.1472,
                94.4893
            ],
            [
                26.0585,
                94.4998
            ],
            [
                25.97,
                94.52
            ]
        ]
    },
    {
        "id": "edge_mokokchung_tuensang",
        "highway_code": "NH-202 (Eastern Nagaland Mountain Trunk)",
        "source": "node_mokokchung",
        "target": "node_tuensang",
        "distance_km": 88.0,
        "avg_speed_kmh": 36.0,
        "elevation_gain_m": 920.0,
        "slope_deg": 18.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 48.0,
        "flood_risk": 12.0,
        "rainfall_mm": 40.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.3249,
                94.5165
            ],
            [
                26.3377,
                94.5983
            ],
            [
                26.3313,
                94.6774
            ],
            [
                26.3105,
                94.7544
            ],
            [
                26.28,
                94.83
            ]
        ]
    },
    {
        "id": "edge_sivasagar_mon",
        "highway_code": "NH-702 (Sonari-Mon Konyak Highway)",
        "source": "node_sivasagar",
        "target": "node_mon",
        "distance_km": 78.0,
        "avg_speed_kmh": 40.0,
        "elevation_gain_m": 850.0,
        "slope_deg": 17.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 45.0,
        "flood_risk": 15.0,
        "rainfall_mm": 42.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.9826,
                94.6425
            ],
            [
                26.954,
                94.7655
            ],
            [
                26.8998,
                94.8736
            ],
            [
                26.8263,
                94.9705
            ],
            [
                26.74,
                95.06
            ]
        ]
    },
    {
        "id": "edge_mon_tuensang",
        "highway_code": "NH-202 (North-Eastern Border Ridge)",
        "source": "node_mon",
        "target": "node_tuensang",
        "distance_km": 118.0,
        "avg_speed_kmh": 35.0,
        "elevation_gain_m": 1100.0,
        "slope_deg": 20.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 28.0,
        "flood_risk": 12.0,
        "rainfall_mm": 44.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.74,
                95.06
            ],
            [
                26.627,
                94.9986
            ],
            [
                26.5124,
                94.9403
            ],
            [
                26.3966,
                94.8843
            ],
            [
                26.28,
                94.83
            ]
        ]
    },
    {
        "id": "edge_tuensang_kiphire",
        "highway_code": "NH-202 (Saramati Access Highway)",
        "source": "node_tuensang",
        "target": "node_kiphire",
        "distance_km": 92.0,
        "avg_speed_kmh": 34.0,
        "elevation_gain_m": 1050.0,
        "slope_deg": 19.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 28.0,
        "flood_risk": 14.0,
        "rainfall_mm": 45.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                26.28,
                94.83
            ],
            [
                26.1823,
                94.7783
            ],
            [
                26.0807,
                94.758
            ],
            [
                25.9763,
                94.7611
            ],
            [
                25.87,
                94.78
            ]
        ]
    },
    {
        "id": "edge_kohima_phek",
        "highway_code": "NH-29 (Chakhesang Mountain Lifeline)",
        "source": "node_kohima",
        "target": "node_phek",
        "distance_km": 85.0,
        "avg_speed_kmh": 40.0,
        "elevation_gain_m": 920.0,
        "slope_deg": 16.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 42.0,
        "flood_risk": 12.0,
        "rainfall_mm": 38.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.6751,
                94.1086
            ],
            [
                25.6596,
                94.2067
            ],
            [
                25.6575,
                94.3046
            ],
            [
                25.6654,
                94.4023
            ],
            [
                25.68,
                94.5
            ]
        ]
    },
    {
        "id": "edge_phek_kiphire",
        "highway_code": "SH-28 (Eastern Frontier Link)",
        "source": "node_phek",
        "target": "node_kiphire",
        "distance_km": 78.0,
        "avg_speed_kmh": 36.0,
        "elevation_gain_m": 880.0,
        "slope_deg": 17.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 46.0,
        "flood_risk": 12.0,
        "rainfall_mm": 40.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.68,
                94.5
            ],
            [
                25.7528,
                94.5528
            ],
            [
                25.8053,
                94.6194
            ],
            [
                25.8427,
                94.6963
            ],
            [
                25.87,
                94.78
            ]
        ]
    },
    {
        "id": "edge_zunheboto_phek",
        "highway_code": "State Highway 16 (Ridge Connector)",
        "source": "node_zunheboto",
        "target": "node_phek",
        "distance_km": 62.0,
        "avg_speed_kmh": 36.0,
        "elevation_gain_m": 720.0,
        "slope_deg": 15.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 38.0,
        "flood_risk": 10.0,
        "rainfall_mm": 35.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.97,
                94.52
            ],
            [
                25.8952,
                94.548
            ],
            [
                25.8223,
                94.5496
            ],
            [
                25.7507,
                94.5314
            ],
            [
                25.68,
                94.5
            ]
        ]
    },
    {
        "id": "edge_kohima_senapati",
        "highway_code": "NH-02 (Mao Gate Inter-State Gateway)",
        "source": "node_kohima",
        "target": "node_senapati",
        "distance_km": 58.0,
        "avg_speed_kmh": 45.0,
        "elevation_gain_m": 520.0,
        "slope_deg": 11.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 35.0,
        "flood_risk": 14.0,
        "rainfall_mm": 36.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.6751,
                94.1086
            ],
            [
                25.5766,
                94.0739
            ],
            [
                25.4758,
                94.0492
            ],
            [
                25.3735,
                94.0321
            ],
            [
                25.27,
                94.02
            ]
        ]
    },
    {
        "id": "edge_senapati_imphal",
        "highway_code": "NH-02 (Kangpokpi-Imphal Valley Expressway)",
        "source": "node_senapati",
        "target": "node_imphal",
        "distance_km": 62.0,
        "avg_speed_kmh": 55.0,
        "elevation_gain_m": 220.0,
        "slope_deg": 5.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 18.0,
        "flood_risk": 16.0,
        "rainfall_mm": 28.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.27,
                94.02
            ],
            [
                25.164,
                93.9599
            ],
            [
                25.0522,
                93.9313
            ],
            [
                24.936,
                93.9262
            ],
            [
                24.817,
                93.9368
            ]
        ]
    },
    {
        "id": "edge_jiribam_tamenglong",
        "highway_code": "NH-37 (Makru River Gorge Highway)",
        "source": "node_jiribam",
        "target": "node_tamenglong",
        "distance_km": 78.0,
        "avg_speed_kmh": 38.0,
        "elevation_gain_m": 890.0,
        "slope_deg": 18.0,
        "terrain_type": "gorge",
        "status": "open",
        "landslide_risk": 30.0,
        "flood_risk": 25.0,
        "rainfall_mm": 52.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                24.8,
                93.12
            ],
            [
                24.8382,
                93.2147
            ],
            [
                24.8825,
                93.3062
            ],
            [
                24.9314,
                93.3955
            ],
            [
                24.9833,
                93.4833
            ]
        ]
    },
    {
        "id": "edge_tamenglong_imphal",
        "highway_code": "NH-37 (Noney Viaduct Valley Highway)",
        "source": "node_tamenglong",
        "target": "node_imphal",
        "distance_km": 92.0,
        "avg_speed_kmh": 42.0,
        "elevation_gain_m": 720.0,
        "slope_deg": 15.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 48.0,
        "flood_risk": 20.0,
        "rainfall_mm": 45.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                24.9833,
                93.4833
            ],
            [
                24.9749,
                93.6089
            ],
            [
                24.94,
                93.7247
            ],
            [
                24.8852,
                93.8332
            ],
            [
                24.817,
                93.9368
            ]
        ]
    },
    {
        "id": "edge_imphal_ukhrul",
        "highway_code": "NH-202 (Shiroi Lily Mountain Highway)",
        "source": "node_imphal",
        "target": "node_ukhrul",
        "distance_km": 82.0,
        "avg_speed_kmh": 42.0,
        "elevation_gain_m": 980.0,
        "slope_deg": 16.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 44.0,
        "flood_risk": 14.0,
        "rainfall_mm": 42.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                24.817,
                93.9368
            ],
            [
                24.9144,
                94.0286
            ],
            [
                24.9939,
                94.1329
            ],
            [
                25.0598,
                94.2467
            ],
            [
                25.1167,
                94.3667
            ]
        ]
    },
    {
        "id": "edge_ukhrul_senapati",
        "highway_code": "SH-38 (Northern Ridge Bypass)",
        "source": "node_ukhrul",
        "target": "node_senapati",
        "distance_km": 75.0,
        "avg_speed_kmh": 38.0,
        "elevation_gain_m": 820.0,
        "slope_deg": 15.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 40.0,
        "flood_risk": 12.0,
        "rainfall_mm": 38.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                25.1167,
                94.3667
            ],
            [
                25.174,
                94.2884
            ],
            [
                25.2161,
                94.2034
            ],
            [
                25.2468,
                94.1134
            ],
            [
                25.27,
                94.02
            ]
        ]
    },
    {
        "id": "edge_imphal_thoubal",
        "highway_code": "NH-102 (Asian Highway 1 Valley Sector)",
        "source": "node_imphal",
        "target": "node_thoubal",
        "distance_km": 25.0,
        "avg_speed_kmh": 65.0,
        "elevation_gain_m": 30.0,
        "slope_deg": 1.5,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 5.0,
        "flood_risk": 18.0,
        "rainfall_mm": 22.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                24.817,
                93.9368
            ],
            [
                24.7616,
                93.9111
            ],
            [
                24.7138,
                93.9152
            ],
            [
                24.6717,
                93.9418
            ],
            [
                24.6333,
                93.9833
            ]
        ]
    },
    {
        "id": "edge_thoubal_moreh",
        "highway_code": "NH-102 (AH-1 Tengnoupal-Moreh Myanmar Gate)",
        "source": "node_thoubal",
        "target": "node_moreh",
        "distance_km": 85.0,
        "avg_speed_kmh": 45.0,
        "elevation_gain_m": 780.0,
        "slope_deg": 15.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 38.0,
        "flood_risk": 15.0,
        "rainfall_mm": 36.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                24.6333,
                93.9833
            ],
            [
                24.5375,
                94.0626
            ],
            [
                24.4417,
                94.1417
            ],
            [
                24.3459,
                94.2209
            ],
            [
                24.25,
                94.3
            ]
        ]
    },
    {
        "id": "edge_imphal_bishnupur",
        "highway_code": "Tiddim Road (Loktak Lake Scenic Trunk)",
        "source": "node_imphal",
        "target": "node_bishnupur",
        "distance_km": 32.0,
        "avg_speed_kmh": 60.0,
        "elevation_gain_m": 25.0,
        "slope_deg": 1.2,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 4.0,
        "flood_risk": 22.0,
        "rainfall_mm": 24.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                24.817,
                93.9368
            ],
            [
                24.7438,
                93.9206
            ],
            [
                24.6917,
                93.882
            ],
            [
                24.6556,
                93.8266
            ],
            [
                24.63,
                93.76
            ]
        ]
    },
    {
        "id": "edge_bishnupur_churachandpur",
        "highway_code": "NH-02 (Bishnupur-Lamka 4-Lane)",
        "source": "node_bishnupur",
        "target": "node_churachandpur",
        "distance_km": 35.0,
        "avg_speed_kmh": 62.0,
        "elevation_gain_m": 45.0,
        "slope_deg": 2.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 6.0,
        "flood_risk": 20.0,
        "rainfall_mm": 25.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                24.63,
                93.76
            ],
            [
                24.5507,
                93.7607
            ],
            [
                24.4755,
                93.7455
            ],
            [
                24.4034,
                93.7184
            ],
            [
                24.3333,
                93.6833
            ]
        ]
    },
    {
        "id": "edge_churachandpur_thoubal",
        "highway_code": "SH-42 (Southern Valley Bypass)",
        "source": "node_churachandpur",
        "target": "node_thoubal",
        "distance_km": 52.0,
        "avg_speed_kmh": 52.0,
        "elevation_gain_m": 80.0,
        "slope_deg": 3.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 8.0,
        "flood_risk": 22.0,
        "rainfall_mm": 26.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                24.3333,
                93.6833
            ],
            [
                24.3888,
                93.7778
            ],
            [
                24.4599,
                93.8567
            ],
            [
                24.5427,
                93.9239
            ],
            [
                24.6333,
                93.9833
            ]
        ]
    },
    {
        "id": "edge_churachandpur_aizawl",
        "highway_code": "NH-102B (Guite Road Trans-Border Highway)",
        "source": "node_churachandpur",
        "target": "node_aizawl",
        "distance_km": 215.0,
        "avg_speed_kmh": 38.0,
        "elevation_gain_m": 1450.0,
        "slope_deg": 18.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 29.0,
        "flood_risk": 16.0,
        "rainfall_mm": 48.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                24.3333,
                93.6833
            ],
            [
                24.2116,
                93.4231
            ],
            [
                24.0661,
                93.1779
            ],
            [
                23.9026,
                92.944
            ],
            [
                23.7271,
                92.7176
            ]
        ]
    },
    {
        "id": "edge_silchar_vairengte",
        "highway_code": "NH-306 (Assam-Mizoram Entry Lifeline)",
        "source": "node_silchar",
        "target": "node_vairengte",
        "distance_km": 45.0,
        "avg_speed_kmh": 52.0,
        "elevation_gain_m": 120.0,
        "slope_deg": 4.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 15.0,
        "flood_risk": 25.0,
        "rainfall_mm": 32.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                24.8333,
                92.7789
            ],
            [
                24.752,
                92.7829
            ],
            [
                24.671,
                92.7799
            ],
            [
                24.5904,
                92.7717
            ],
            [
                24.51,
                92.76
            ]
        ]
    },
    {
        "id": "edge_vairengte_kolasib",
        "highway_code": "NH-306 (Kolasib Mountain Trunk)",
        "source": "node_vairengte",
        "target": "node_kolasib",
        "distance_km": 48.0,
        "avg_speed_kmh": 45.0,
        "elevation_gain_m": 580.0,
        "slope_deg": 12.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 32.0,
        "flood_risk": 18.0,
        "rainfall_mm": 38.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                24.51,
                92.76
            ],
            [
                24.4269,
                92.7785
            ],
            [
                24.3523,
                92.7662
            ],
            [
                24.284,
                92.7308
            ],
            [
                24.22,
                92.68
            ]
        ]
    },
    {
        "id": "edge_kolasib_aizawl",
        "highway_code": "NH-306 (Ratu-Aizawl Ridge Expressway)",
        "source": "node_kolasib",
        "target": "node_aizawl",
        "distance_km": 82.0,
        "avg_speed_kmh": 45.0,
        "elevation_gain_m": 820.0,
        "slope_deg": 15.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 38.0,
        "flood_risk": 15.0,
        "rainfall_mm": 42.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                24.22,
                92.68
            ],
            [
                24.0977,
                92.702
            ],
            [
                23.9747,
                92.714
            ],
            [
                23.8511,
                92.7183
            ],
            [
                23.7271,
                92.7176
            ]
        ]
    },
    {
        "id": "edge_aizawl_mamit",
        "highway_code": "NH-108 (Western Mizoram Mountain Highway)",
        "source": "node_aizawl",
        "target": "node_mamit",
        "distance_km": 92.0,
        "avg_speed_kmh": 40.0,
        "elevation_gain_m": 750.0,
        "slope_deg": 14.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 35.0,
        "flood_risk": 14.0,
        "rainfall_mm": 38.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                23.7271,
                92.7176
            ],
            [
                23.8026,
                92.6828
            ],
            [
                23.8583,
                92.6303
            ],
            [
                23.8991,
                92.5646
            ],
            [
                23.93,
                92.49
            ]
        ]
    },
    {
        "id": "edge_mamit_kolasib",
        "highway_code": "SH-22 (North-West Ridge Connector)",
        "source": "node_mamit",
        "target": "node_kolasib",
        "distance_km": 75.0,
        "avg_speed_kmh": 42.0,
        "elevation_gain_m": 620.0,
        "slope_deg": 12.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 30.0,
        "flood_risk": 15.0,
        "rainfall_mm": 35.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                23.93,
                92.49
            ],
            [
                23.9858,
                92.5629
            ],
            [
                24.055,
                92.6155
            ],
            [
                24.1342,
                92.6528
            ],
            [
                24.22,
                92.68
            ]
        ]
    },
    {
        "id": "edge_aizawl_serchhip",
        "highway_code": "NH-54 (Central Mizoram Ridge Trunk)",
        "source": "node_aizawl",
        "target": "node_serchhip",
        "distance_km": 85.0,
        "avg_speed_kmh": 44.0,
        "elevation_gain_m": 780.0,
        "slope_deg": 14.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 36.0,
        "flood_risk": 14.0,
        "rainfall_mm": 40.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                23.7271,
                92.7176
            ],
            [
                23.6279,
                92.7668
            ],
            [
                23.5247,
                92.8031
            ],
            [
                23.4184,
                92.8298
            ],
            [
                23.31,
                92.85
            ]
        ]
    },
    {
        "id": "edge_serchhip_champhai",
        "highway_code": "NH-54 (East Ridge Border Highway)",
        "source": "node_serchhip",
        "target": "node_champhai",
        "distance_km": 98.0,
        "avg_speed_kmh": 40.0,
        "elevation_gain_m": 920.0,
        "slope_deg": 16.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 42.0,
        "flood_risk": 12.0,
        "rainfall_mm": 44.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                23.31,
                92.85
            ],
            [
                23.3874,
                92.9575
            ],
            [
                23.4349,
                93.075
            ],
            [
                23.4599,
                93.2
            ],
            [
                23.47,
                93.33
            ]
        ]
    },
    {
        "id": "edge_aizawl_champhai",
        "highway_code": "NH-06 (Seling-Champhai Trade Highway)",
        "source": "node_aizawl",
        "target": "node_champhai",
        "distance_km": 165.0,
        "avg_speed_kmh": 42.0,
        "elevation_gain_m": 1150.0,
        "slope_deg": 17.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 45.0,
        "flood_risk": 14.0,
        "rainfall_mm": 45.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                23.7271,
                92.7176
            ],
            [
                23.6667,
                92.8723
            ],
            [
                23.6032,
                93.0258
            ],
            [
                23.5374,
                93.1782
            ],
            [
                23.47,
                93.33
            ]
        ]
    },
    {
        "id": "edge_serchhip_lunglei",
        "highway_code": "NH-54 (Mat River Valley Highway)",
        "source": "node_serchhip",
        "target": "node_lunglei",
        "distance_km": 88.0,
        "avg_speed_kmh": 42.0,
        "elevation_gain_m": 850.0,
        "slope_deg": 15.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 38.0,
        "flood_risk": 15.0,
        "rainfall_mm": 42.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                23.31,
                92.85
            ],
            [
                23.2125,
                92.7842
            ],
            [
                23.107,
                92.747
            ],
            [
                22.9955,
                92.7313
            ],
            [
                22.88,
                92.73
            ]
        ]
    },
    {
        "id": "edge_lunglei_lawngtlai",
        "highway_code": "NH-54 (Kaladan Multimodal Highway)",
        "source": "node_lunglei",
        "target": "node_lawngtlai",
        "distance_km": 65.0,
        "avg_speed_kmh": 42.0,
        "elevation_gain_m": 680.0,
        "slope_deg": 14.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 42.0,
        "flood_risk": 16.0,
        "rainfall_mm": 46.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                22.88,
                92.73
            ],
            [
                22.7802,
                92.748
            ],
            [
                22.6883,
                92.7836
            ],
            [
                22.6022,
                92.8324
            ],
            [
                22.52,
                92.89
            ]
        ]
    },
    {
        "id": "edge_mamit_dharmanagar",
        "highway_code": "NH-108 (Mizoram-Tripura Inter-State Lifeline)",
        "source": "node_mamit",
        "target": "node_dharmanagar",
        "distance_km": 115.0,
        "avg_speed_kmh": 45.0,
        "elevation_gain_m": 640.0,
        "slope_deg": 12.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 32.0,
        "flood_risk": 18.0,
        "rainfall_mm": 36.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                23.93,
                92.49
            ],
            [
                24.0292,
                92.3894
            ],
            [
                24.1397,
                92.3046
            ],
            [
                24.2587,
                92.2317
            ],
            [
                24.3833,
                92.1667
            ]
        ]
    },
    {
        "id": "edge_karimganj_dharmanagar",
        "highway_code": "NH-08 (Assam-Tripura Inter-State Trunk)",
        "source": "node_karimganj",
        "target": "node_dharmanagar",
        "distance_km": 62.0,
        "avg_speed_kmh": 55.0,
        "elevation_gain_m": 80.0,
        "slope_deg": 2.5,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 8.0,
        "flood_risk": 25.0,
        "rainfall_mm": 30.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                24.8693,
                92.3592
            ],
            [
                24.7341,
                92.3456
            ],
            [
                24.6099,
                92.3044
            ],
            [
                24.4939,
                92.2424
            ],
            [
                24.3833,
                92.1667
            ]
        ]
    },
    {
        "id": "edge_dharmanagar_kailashahar",
        "highway_code": "NH-208 (Unakoti Heritage Access)",
        "source": "node_dharmanagar",
        "target": "node_kailashahar",
        "distance_km": 32.0,
        "avg_speed_kmh": 52.0,
        "elevation_gain_m": 40.0,
        "slope_deg": 2.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 6.0,
        "flood_risk": 22.0,
        "rainfall_mm": 28.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                24.3833,
                92.1667
            ],
            [
                24.3751,
                92.1237
            ],
            [
                24.3634,
                92.0818
            ],
            [
                24.3492,
                92.0407
            ],
            [
                24.3333,
                92.0
            ]
        ]
    },
    {
        "id": "edge_kailashahar_ambassa",
        "highway_code": "NH-208 (Manu Valley Forest Highway)",
        "source": "node_kailashahar",
        "target": "node_ambassa",
        "distance_km": 68.0,
        "avg_speed_kmh": 50.0,
        "elevation_gain_m": 180.0,
        "slope_deg": 4.5,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 15.0,
        "flood_risk": 20.0,
        "rainfall_mm": 32.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                24.3333,
                92.0
            ],
            [
                24.2434,
                91.9254
            ],
            [
                24.1428,
                91.8805
            ],
            [
                24.0341,
                91.8578
            ],
            [
                23.92,
                91.85
            ]
        ]
    },
    {
        "id": "edge_dharmanagar_ambassa",
        "highway_code": "NH-08 (Tripura Central Spine)",
        "source": "node_dharmanagar",
        "target": "node_ambassa",
        "distance_km": 78.0,
        "avg_speed_kmh": 54.0,
        "elevation_gain_m": 210.0,
        "slope_deg": 5.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 16.0,
        "flood_risk": 18.0,
        "rainfall_mm": 30.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                24.3833,
                92.1667
            ],
            [
                24.2769,
                92.0738
            ],
            [
                24.1629,
                91.9918
            ],
            [
                24.0434,
                91.9182
            ],
            [
                23.92,
                91.85
            ]
        ]
    },
    {
        "id": "edge_ambassa_agartala",
        "highway_code": "NH-08 (Baramura Hill Range Corridor)",
        "source": "node_ambassa",
        "target": "node_agartala",
        "distance_km": 85.0,
        "avg_speed_kmh": 55.0,
        "elevation_gain_m": 280.0,
        "slope_deg": 6.5,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 22.0,
        "flood_risk": 16.0,
        "rainfall_mm": 35.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                23.92,
                91.85
            ],
            [
                23.8677,
                91.7139
            ],
            [
                23.8395,
                91.5741
            ],
            [
                23.8295,
                91.4314
            ],
            [
                23.8315,
                91.2868
            ]
        ]
    },
    {
        "id": "edge_agartala_udaipur",
        "highway_code": "NH-08 (Agartala-Udaipur 4-Lane Trunk)",
        "source": "node_agartala",
        "target": "node_udaipur",
        "distance_km": 52.0,
        "avg_speed_kmh": 68.0,
        "elevation_gain_m": 45.0,
        "slope_deg": 1.5,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 4.0,
        "flood_risk": 15.0,
        "rainfall_mm": 22.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                23.8315,
                91.2868
            ],
            [
                23.7751,
                91.3635
            ],
            [
                23.7042,
                91.4181
            ],
            [
                23.6224,
                91.4562
            ],
            [
                23.5333,
                91.4833
            ]
        ]
    },
    {
        "id": "edge_udaipur_belonia",
        "highway_code": "NH-108A (South Border Highway)",
        "source": "node_udaipur",
        "target": "node_belonia",
        "distance_km": 45.0,
        "avg_speed_kmh": 58.0,
        "elevation_gain_m": 40.0,
        "slope_deg": 1.8,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 5.0,
        "flood_risk": 18.0,
        "rainfall_mm": 24.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                23.5333,
                91.4833
            ],
            [
                23.464,
                91.4622
            ],
            [
                23.3935,
                91.4513
            ],
            [
                23.322,
                91.4481
            ],
            [
                23.25,
                91.45
            ]
        ]
    },
    {
        "id": "edge_udaipur_sabroom",
        "highway_code": "NH-08 (Maitri Setu Feni River Corridor)",
        "source": "node_udaipur",
        "target": "node_sabroom",
        "distance_km": 72.0,
        "avg_speed_kmh": 65.0,
        "elevation_gain_m": 50.0,
        "slope_deg": 2.0,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 6.0,
        "flood_risk": 16.0,
        "rainfall_mm": 26.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                23.5333,
                91.4833
            ],
            [
                23.3832,
                91.5087
            ],
            [
                23.2465,
                91.5632
            ],
            [
                23.1199,
                91.6393
            ],
            [
                23.0,
                91.73
            ]
        ]
    },
    {
        "id": "edge_belonia_sabroom",
        "highway_code": "NH-08 (Southern Frontier Link)",
        "source": "node_belonia",
        "target": "node_sabroom",
        "distance_km": 42.0,
        "avg_speed_kmh": 55.0,
        "elevation_gain_m": 35.0,
        "slope_deg": 1.5,
        "terrain_type": "plains",
        "status": "open",
        "landslide_risk": 5.0,
        "flood_risk": 18.0,
        "rainfall_mm": 25.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                23.25,
                91.45
            ],
            [
                23.1812,
                91.5144
            ],
            [
                23.1174,
                91.5832
            ],
            [
                23.0574,
                91.6555
            ],
            [
                23.0,
                91.73
            ]
        ]
    },
    {
        "id": "edge_rangpo_gangtok",
        "highway_code": "NH-10 (Singtam-Ranipool-Gangtok Trunk)",
        "source": "node_rangpo",
        "target": "node_gangtok",
        "distance_km": 38.0,
        "avg_speed_kmh": 42.0,
        "elevation_gain_m": 880.0,
        "slope_deg": 18.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 48.0,
        "flood_risk": 15.0,
        "rainfall_mm": 48.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                27.18,
                88.53
            ],
            [
                27.2351,
                88.5172
            ],
            [
                27.2779,
                88.53
            ],
            [
                27.3115,
                88.5619
            ],
            [
                27.3389,
                88.6065
            ]
        ]
    },
    {
        "id": "edge_rangpo_namchi",
        "highway_code": "NH-710 (Melli-Jorethang-Namchi)",
        "source": "node_rangpo",
        "target": "node_namchi",
        "distance_km": 45.0,
        "avg_speed_kmh": 40.0,
        "elevation_gain_m": 720.0,
        "slope_deg": 16.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 42.0,
        "flood_risk": 14.0,
        "rainfall_mm": 42.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                27.18,
                88.53
            ],
            [
                27.1501,
                88.4865
            ],
            [
                27.1422,
                88.4418
            ],
            [
                27.1506,
                88.3962
            ],
            [
                27.17,
                88.35
            ]
        ]
    },
    {
        "id": "edge_namchi_geyzing",
        "highway_code": "SH-08 (Legship River-Pelling Highway)",
        "source": "node_namchi",
        "target": "node_geyzing",
        "distance_km": 48.0,
        "avg_speed_kmh": 38.0,
        "elevation_gain_m": 850.0,
        "slope_deg": 17.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 45.0,
        "flood_risk": 12.0,
        "rainfall_mm": 40.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                27.17,
                88.35
            ],
            [
                27.2115,
                88.3403
            ],
            [
                27.2417,
                88.3184
            ],
            [
                27.2637,
                88.2873
            ],
            [
                27.28,
                88.25
            ]
        ]
    },
    {
        "id": "edge_gangtok_namchi",
        "highway_code": "Damthang Pass Scenic Mountain Highway",
        "source": "node_gangtok",
        "target": "node_namchi",
        "distance_km": 62.0,
        "avg_speed_kmh": 38.0,
        "elevation_gain_m": 940.0,
        "slope_deg": 18.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 48.0,
        "flood_risk": 12.0,
        "rainfall_mm": 44.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                27.3389,
                88.6065
            ],
            [
                27.3288,
                88.5212
            ],
            [
                27.293,
                88.4528
            ],
            [
                27.238,
                88.3972
            ],
            [
                27.17,
                88.35
            ]
        ]
    },
    {
        "id": "edge_gangtok_mangan",
        "highway_code": "North Sikkim Highway (Teesta Gorge Sector)",
        "source": "node_gangtok",
        "target": "node_mangan",
        "distance_km": 65.0,
        "avg_speed_kmh": 35.0,
        "elevation_gain_m": 1150.0,
        "slope_deg": 22.0,
        "terrain_type": "gorge",
        "status": "open",
        "landslide_risk": 34.0,
        "flood_risk": 18.0,
        "rainfall_mm": 55.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                27.3389,
                88.6065
            ],
            [
                27.3841,
                88.5872
            ],
            [
                27.4294,
                88.5681
            ],
            [
                27.4747,
                88.549
            ],
            [
                27.52,
                88.53
            ]
        ]
    },
    {
        "id": "edge_mangan_geyzing",
        "highway_code": "Dikchu-Ravangla Mountain Bypass",
        "source": "node_mangan",
        "target": "node_geyzing",
        "distance_km": 78.0,
        "avg_speed_kmh": 32.0,
        "elevation_gain_m": 1220.0,
        "slope_deg": 21.0,
        "terrain_type": "hills",
        "status": "open",
        "landslide_risk": 28.0,
        "flood_risk": 14.0,
        "rainfall_mm": 48.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                27.52,
                88.53
            ],
            [
                27.4307,
                88.4851
            ],
            [
                27.3648,
                88.4201
            ],
            [
                27.3166,
                88.3401
            ],
            [
                27.28,
                88.25
            ]
        ]
    },
    {
        "id": "edge_gangtok_nathula",
        "highway_code": "JN Road (Nathu La High-Altitude Silk Pass)",
        "source": "node_gangtok",
        "target": "node_nathula",
        "distance_km": 54.0,
        "avg_speed_kmh": 30.0,
        "elevation_gain_m": 2450.0,
        "slope_deg": 28.0,
        "terrain_type": "gorge",
        "status": "open",
        "landslide_risk": 36.0,
        "flood_risk": 10.0,
        "rainfall_mm": 52.0,
        "closure_reason": None,
        "coordinates_polyline": [
            [
                27.3389,
                88.6065
            ],
            [
                27.3709,
                88.6584
            ],
            [
                27.3868,
                88.7136
            ],
            [
                27.3906,
                88.7715
            ],
            [
                27.3865,
                88.831
            ]
        ]
    }
]

INITIAL_FLEET_DATA: List[Dict[str, Any]] = [
    {
        "id": "trk_v101",
        "category": "logistics",
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
        "category": "logistics",
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
        "category": "logistics",
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
        "category": "logistics",
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
        "category": "logistics",
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
        "category": "logistics",
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
        "category": "logistics",
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
    },
    {
        "id": "car_v201",
        "category": "car",
        "vehicle_number": "AS-01-EB-3419",
        "driver_name": "Arun Saikia",
        "driver_phone": "+91 94351 88201",
        "vehicle_type": "Civilian Passenger SUV (Tata Safari)",
        "cargo_type": "Evacuating Family (4 Members) & Essential Bags",
        "cargo_priority": "STANDARD",
        "cargo_weight_tons": 1.9,
        "source": "Guwahati Central",
        "destination": "Shillong Police Bazar",
        "current_coordinates": [25.8200, 91.8600],
        "speed_kmh": 55.0,
        "heading_deg": 165.0,
        "status": "moving",
        "delay_minutes": 0,
        "assigned_route_id": "edge_guwahati_shillong",
        "eta_timestamp": "1.1 Hours"
    },
    {
        "id": "car_v202",
        "category": "car",
        "vehicle_number": "ML-05-C-8812",
        "driver_name": "Mary Lyngdoh",
        "driver_phone": "+91 98622 33405",
        "vehicle_type": "Civilian Hatchback (Maruti Swift)",
        "cargo_type": "Commuter Passengers (2) & First-Aid Supplies",
        "cargo_priority": "STANDARD",
        "cargo_weight_tons": 1.1,
        "source": "Shillong",
        "destination": "Cherrapunji (Sohra)",
        "current_coordinates": [25.4100, 91.7500],
        "speed_kmh": 48.0,
        "heading_deg": 190.0,
        "status": "moving",
        "delay_minutes": 5,
        "assigned_route_id": "edge_shillong_cherrapunji",
        "eta_timestamp": "0.7 Hours"
    },
    {
        "id": "car_v203",
        "category": "car",
        "vehicle_number": "NL-01-F-5520",
        "driver_name": "Imti Ao",
        "driver_phone": "+91 94020 77114",
        "vehicle_type": "Civilian 4WD (Mahindra Thar)",
        "cargo_type": "Community Volunteer Doctors (3)",
        "cargo_priority": "HIGH",
        "cargo_weight_tons": 1.7,
        "source": "Kohima",
        "destination": "Imphal West",
        "current_coordinates": [25.2500, 93.9800],
        "speed_kmh": 45.0,
        "heading_deg": 170.0,
        "status": "moving",
        "delay_minutes": 10,
        "assigned_route_id": "edge_kohima_imphal",
        "eta_timestamp": "2.0 Hours"
    },
    {
        "id": "car_v204",
        "category": "car",
        "vehicle_number": "AR-01-B-2109",
        "driver_name": "Karsang Dorjee",
        "driver_phone": "+91 94360 99450",
        "vehicle_type": "Civilian Utility Vehicle (Bolero)",
        "cargo_type": "Local Family Evacuees (5)",
        "cargo_priority": "STANDARD",
        "cargo_weight_tons": 2.1,
        "source": "Itanagar",
        "destination": "Tezpur",
        "current_coordinates": [27.0200, 93.4500],
        "speed_kmh": 50.0,
        "heading_deg": 215.0,
        "status": "delayed",
        "delay_minutes": 30,
        "assigned_route_id": "edge_itanagar_tezpur",
        "eta_timestamp": "2.4 Hours"
    },
    {
        "id": "car_v205",
        "category": "car",
        "vehicle_number": "SK-02-P-7711",
        "driver_name": "Sonam Lepcha",
        "driver_phone": "+91 97332 55198",
        "vehicle_type": "Passenger Taxi (Innova Crysta)",
        "cargo_type": "Stranded Travellers (4) & Emergency Luggage",
        "cargo_priority": "STANDARD",
        "cargo_weight_tons": 2.2,
        "source": "Gangtok",
        "destination": "Siliguri Junction",
        "current_coordinates": [27.1200, 88.5100],
        "speed_kmh": 40.0,
        "heading_deg": 210.0,
        "status": "moving",
        "delay_minutes": 0,
        "assigned_route_id": "edge_siliguri_gangtok",
        "eta_timestamp": "1.8 Hours"
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
