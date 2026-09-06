"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Module 16: Regional Meteorological & Doppler Radar Telemetry Engine
"""
from typing import Dict, List, Any, Optional
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

import urllib.request
import json
import time
from datetime import datetime

class WeatherEngine:
    def __init__(self):
        self.stations = dict(NER_WEATHER_STATIONS)
        self.last_sync_timestamp: float = 0
        self.is_live_synced: bool = False
        self.sync_source: str = "Pre-calibrated Doppler Baseline"

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
                    "radar_intensity_dbz": 35,
                    "is_live": False
                }

    def get_all_stations(self) -> List[Dict[str, Any]]:
        return list(self.stations.values())

    def get_district_weather(self, district_id: str) -> Dict[str, Any]:
        return self.stations.get(district_id, self.stations.get("node_guwahati"))

    def get_sync_status(self) -> Dict[str, Any]:
        return {
            "is_live_synced": self.is_live_synced,
            "sync_source": self.sync_source,
            "last_synced_at": datetime.fromtimestamp(self.last_sync_timestamp).strftime("%Y-%m-%d %H:%M:%S IST") if self.last_sync_timestamp > 0 else "Baseline Only",
            "total_stations": len(self.stations),
            "high_warning_count": sum(1 for s in self.stations.values() if s.get("warning_level") in ("ORANGE_WARNING", "RED_ALERT"))
        }

    def sync_live_weather(self, target_districts: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Fetches live meteorological observations from Open-Meteo free API
        for high-priority or specified NER district stations.
        Falls back seamlessly without failing if offline.
        """
        targets = target_districts or [
            "node_guwahati", "node_shillong", "node_kohima", "node_imphal",
            "node_aizawl", "node_gangtok", "node_tawang", "node_silchar",
            "node_agartala", "node_pasighat", "node_haflong", "node_tura"
        ]
        
        synced_count = 0
        errors = []

        for d_id in targets:
            station = self.stations.get(d_id)
            if not station:
                continue
            coords = station["coordinates"]
            lat, lon = coords[0], coords[1]
            url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation,rain,weather_code,wind_speed_10m"
                f"&hourly=precipitation&forecast_days=1&timezone=auto"
            )
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "NERA-Logistics-Platform/2.0"})
                with urllib.request.urlopen(req, timeout=3.0) as res:
                    if res.status == 200:
                        payload = json.loads(res.read().decode("utf-8"))
                        curr = payload.get("current", {})
                        temp = float(curr.get("temperature_2m", station["temperature_c"]))
                        humidity = float(curr.get("relative_humidity_2m", station["humidity_pct"]))
                        rain_hr = float(curr.get("precipitation", station["rainfall_mm_hr"]))
                        wind = float(curr.get("wind_speed_10m", station["wind_kmh"]))
                        
                        # Hourly precipitation sum for 24h estimation
                        hourly_precip = payload.get("hourly", {}).get("precipitation", [])
                        rain_24h = sum(float(x) for x in hourly_precip[:24]) if hourly_precip else max(rain_hr * 6.0, 15.0)

                        # Determine meteorological condition & warning level
                        wcode = curr.get("weather_code", 0)
                        if rain_hr > 25.0 or rain_24h > 120.0:
                            warning = "RED_ALERT"
                            condition = "Torrential Cloudburst / Severe Inundation"
                            radar_dbz = 58
                        elif rain_hr > 15.0 or rain_24h > 65.0:
                            warning = "ORANGE_WARNING"
                            condition = "Heavy Monsoon Downpour / High Runoff"
                            radar_dbz = 48
                        elif rain_hr > 3.0:
                            warning = "YELLOW_ADVISORY"
                            condition = "Moderate Showers & Hill Slope Mist"
                            radar_dbz = 38
                        else:
                            warning = "GREEN_CLEAR"
                            condition = "Clear / Overcast High-Altitude Pass"
                            radar_dbz = 22

                        # Update station live data
                        station.update({
                            "temperature_c": round(temp, 1),
                            "humidity_pct": int(humidity),
                            "rainfall_mm_hr": round(rain_hr, 1),
                            "rainfall_24h_mm": round(rain_24h, 1),
                            "wind_kmh": round(wind, 1),
                            "condition": condition,
                            "warning_level": warning,
                            "radar_intensity_dbz": radar_dbz,
                            "is_live": True,
                            "last_synced": datetime.now().strftime("%H:%M:%S IST")
                        })
                        synced_count += 1
            except Exception as e:
                errors.append(f"{d_id}: {str(e)[:40]}")
                continue

        if synced_count > 0:
            self.last_sync_timestamp = time.time()
            self.is_live_synced = True
            self.sync_source = f"Open-Meteo Global WMO API ({synced_count} Live Met Stations Synced)"

        return {
            "status": "success" if synced_count > 0 else "fallback_retained",
            "synced_count": synced_count,
            "total_stations": len(self.stations),
            "sync_source": self.sync_source,
            "is_live_synced": self.is_live_synced,
            "errors_count": len(errors)
        }

    def get_radar_overlays(self) -> List[Dict[str, Any]]:
        """Returns radar precipitation intensity zones for Leaflet overlay"""
        overlays = []
        for s in self.stations.values():
            if s.get("rainfall_mm_hr", 0) > 10.0 or s.get("radar_intensity_dbz", 0) >= 35:
                color = "#ff3366" if s.get("rainfall_mm_hr", 0) > 25.0 else ("#ffb800" if s.get("rainfall_mm_hr", 0) > 12.0 else "#00f0ff")
                overlays.append({
                    "station_id": s["district_id"],
                    "coordinates": s["coordinates"],
                    "radius_meters": 18000 + int(s.get("rainfall_mm_hr", 10) * 500),
                    "color": color,
                    "condition": s.get("condition", "Precipitation Zone"),
                    "rainfall_mm_hr": s.get("rainfall_mm_hr", 10),
                    "dbz": s.get("radar_intensity_dbz", 35),
                    "warning_level": s.get("warning_level", "YELLOW_ADVISORY")
                })
        return overlays

weather_engine = WeatherEngine()

