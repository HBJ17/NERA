"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Module 16: Regional Meteorological & Doppler Radar Telemetry Engine
"""
from typing import Dict, List, Any
from app.services.digital_twin_data import NER_DISTRICT_NODES

NER_WEATHER_STATIONS: Dict[str, Dict[str, Any]] = {
    "node_guwahati": {
        "district_id": "node_guwahati",
        "station_name": "Guwahati Borjhar Met Center (Kamrup)",
        "state": "Assam",
        "coordinates": [26.1445, 91.7362],
        "temperature_c": 28.5,
        "humidity_pct": 82,
        "rainfall_mm_hr": 14.2,
        "rainfall_24h_mm": 48.0,
        "wind_kmh": 18.5,
        "condition": "Heavy Monsoon Showers",
        "warning_level": "YELLOW_ADVISORY",
        "radar_intensity_dbz": 42
    },
    "node_shillong": {
        "district_id": "node_shillong",
        "station_name": "Shillong Peak Weather Observatory (East Khasi Hills)",
        "state": "Meghalaya",
        "coordinates": [25.5788, 91.8933],
        "temperature_c": 19.2,
        "humidity_pct": 94,
        "rainfall_mm_hr": 28.5,
        "rainfall_24h_mm": 110.0,
        "wind_kmh": 24.0,
        "condition": "Severe Torrential Rain & Dense Mist",
        "warning_level": "ORANGE_WARNING",
        "radar_intensity_dbz": 54
    },
    "node_kohima": {
        "district_id": "node_kohima",
        "station_name": "Kohima Ridge Met Station",
        "state": "Nagaland",
        "coordinates": [25.6751, 94.1086],
        "temperature_c": 21.0,
        "humidity_pct": 88,
        "rainfall_mm_hr": 18.0,
        "rainfall_24h_mm": 65.0,
        "wind_kmh": 15.0,
        "condition": "Hill Slope Downpours",
        "warning_level": "ORANGE_WARNING",
        "radar_intensity_dbz": 48
    },
    "node_imphal": {
        "district_id": "node_imphal",
        "station_name": "Imphal Tulihal Met Center",
        "state": "Manipur",
        "coordinates": [24.8170, 93.9368],
        "temperature_c": 26.0,
        "humidity_pct": 84,
        "rainfall_mm_hr": 12.0,
        "rainfall_24h_mm": 42.0,
        "wind_kmh": 12.0,
        "condition": "Scattered Rain Showers",
        "warning_level": "YELLOW_ADVISORY",
        "radar_intensity_dbz": 38
    },
    "node_aizawl": {
        "district_id": "node_aizawl",
        "station_name": "Aizawl Lengpui Weather Radar",
        "state": "Mizoram",
        "coordinates": [23.7271, 92.7176],
        "temperature_c": 23.5,
        "humidity_pct": 90,
        "rainfall_mm_hr": 16.5,
        "rainfall_24h_mm": 58.0,
        "wind_kmh": 16.0,
        "condition": "Monsoon Clouds & Mist",
        "warning_level": "YELLOW_ADVISORY",
        "radar_intensity_dbz": 44
    },
    "node_tawang": {
        "district_id": "node_tawang",
        "station_name": "Tawang High Altitude Met Outpost (10,000 ft)",
        "state": "Arunachal Pradesh",
        "coordinates": [27.5861, 91.8594],
        "temperature_c": 9.5,
        "humidity_pct": 96,
        "rainfall_mm_hr": 32.0,
        "rainfall_24h_mm": 135.0,
        "wind_kmh": 35.0,
        "condition": "Freezing Rain & Slope Fog",
        "warning_level": "RED_ALERT",
        "radar_intensity_dbz": 58
    },
    "node_pasighat": {
        "district_id": "node_pasighat",
        "station_name": "Pasighat Siang River Doppler Station",
        "state": "Arunachal Pradesh",
        "coordinates": [28.0668, 95.3263],
        "temperature_c": 25.0,
        "humidity_pct": 91,
        "rainfall_mm_hr": 22.0,
        "rainfall_24h_mm": 88.0,
        "wind_kmh": 20.0,
        "condition": "Heavy Riverine Precipitation",
        "warning_level": "ORANGE_WARNING",
        "radar_intensity_dbz": 50
    },
    "node_gangtok": {
        "district_id": "node_gangtok",
        "station_name": "Gangtok Teesta Basin Met Station",
        "state": "Sikkim",
        "coordinates": [27.3314, 88.6138],
        "temperature_c": 17.5,
        "humidity_pct": 95,
        "rainfall_mm_hr": 26.0,
        "rainfall_24h_mm": 95.0,
        "wind_kmh": 22.0,
        "condition": "Continuous Gorge Downpour",
        "warning_level": "RED_ALERT",
        "radar_intensity_dbz": 55
    },
    "node_agartala": {
        "district_id": "node_agartala",
        "station_name": "Agartala Singerbhil Met Center",
        "state": "Tripura",
        "coordinates": [23.8315, 91.2868],
        "temperature_c": 29.0,
        "humidity_pct": 78,
        "rainfall_mm_hr": 8.0,
        "rainfall_24h_mm": 24.0,
        "wind_kmh": 14.0,
        "condition": "Partly Cloudy with Light Showers",
        "warning_level": "GREEN_CLEAR",
        "radar_intensity_dbz": 28
    },
    "node_haflong": {
        "district_id": "node_haflong",
        "station_name": "Dima Hasao Hill Sector Met Post",
        "state": "Assam",
        "coordinates": [25.1764, 93.0189],
        "temperature_c": 22.5,
        "humidity_pct": 93,
        "rainfall_mm_hr": 30.0,
        "rainfall_24h_mm": 125.0,
        "wind_kmh": 26.0,
        "condition": "Saturated Slope Torrential Storm",
        "warning_level": "RED_ALERT",
        "radar_intensity_dbz": 56
    }
}

class WeatherEngine:
    def __init__(self):
        self.stations = dict(NER_WEATHER_STATIONS)
        # Populate rest from NER_DISTRICT_NODES
        for node in NER_DISTRICT_NODES:
            n_id = node["id"]
            if n_id not in self.stations:
                self.stations[n_id] = {
                    "district_id": n_id,
                    "station_name": f"{node['name'].split(' (')[0]} Met Post",
                    "state": node["state"],
                    "coordinates": node["coordinates"],
                    "temperature_c": 26.0,
                    "humidity_pct": 82,
                    "rainfall_mm_hr": 10.0,
                    "rainfall_24h_mm": 35.0,
                    "wind_kmh": 15.0,
                    "condition": "Passing Monsoon Cloud Cover",
                    "warning_level": "YELLOW_ADVISORY",
                    "radar_intensity_dbz": 35
                }

    def get_all_stations(self) -> List[Dict[str, Any]]:
        return list(self.stations.values())

    def get_district_weather(self, district_id: str) -> Dict[str, Any]:
        return self.stations.get(district_id, self.stations.get("node_guwahati"))

    def get_radar_overlays(self) -> List[Dict[str, Any]]:
        """Returns radar precipitation intensity zones for Leaflet overlay"""
        overlays = []
        for s in self.stations.values():
            if s["rainfall_mm_hr"] > 15.0:
                color = "#ff3366" if s["rainfall_mm_hr"] > 25.0 else "#ffb800"
                overlays.append({
                    "station_id": s["district_id"],
                    "coordinates": s["coordinates"],
                    "radius_meters": 18000 + int(s["rainfall_mm_hr"] * 500),
                    "color": color,
                    "condition": s["condition"],
                    "rainfall_mm_hr": s["rainfall_mm_hr"],
                    "dbz": s["radar_intensity_dbz"]
                })
        return overlays

weather_engine = WeatherEngine()
