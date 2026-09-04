"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Module 3, 6, 8 & 12: Fleet Telemetry, Field Incident Ingestion & Alert State Manager

Maintains:
- Live GPS vehicle telemetry with micro-jitter kinetic updates
- Dynamic in-memory road edge and district node statuses
- Geotagged field reports queue and topological twin graph propagation
- Multilingual alert broadcast synthesis
"""
import copy
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.services.digital_twin_data import (
    INITIAL_FLEET_DATA,
    INITIAL_FIELD_REPORTS,
    INITIAL_ALERTS,
    NER_DISTRICT_NODES,
    NER_ROAD_EDGES
)
from app.models.schemas import (
    FieldReportCreate,
    FieldReportRecord,
    EmergencyAlert
)

class FleetAndFieldManager:
    def __init__(self):
        self.fleet: List[Dict[str, Any]] = copy.deepcopy(INITIAL_FLEET_DATA)
        self.field_reports: List[Dict[str, Any]] = copy.deepcopy(INITIAL_FIELD_REPORTS)
        self.alerts: List[Dict[str, Any]] = copy.deepcopy(INITIAL_ALERTS)
        self.nodes_state: List[Dict[str, Any]] = copy.deepcopy(NER_DISTRICT_NODES)
        self.edges_state: List[Dict[str, Any]] = copy.deepcopy(NER_ROAD_EDGES)

    def get_fleet(self) -> List[Dict[str, Any]]:
        return self.fleet

    def get_field_reports(self) -> List[Dict[str, Any]]:
        return self.field_reports

    def get_alerts(self) -> List[Dict[str, Any]]:
        return self.alerts

    def add_field_report(self, report: FieldReportCreate) -> FieldReportRecord:
        report_id = f"rpt_{uuid.uuid4().hex[:6]}"
        now_str = datetime.now().strftime("%I:%M %p, Today")

        record = FieldReportRecord(
            id=report_id,
            officer_name=report.officer_name,
            department=report.department,
            incident_type=report.incident_type,
            severity=report.severity,
            latitude=report.latitude,
            longitude=report.longitude,
            location_name=report.location_name,
            nearest_highway=report.nearest_highway,
            photo_base64=report.photo_base64,
            photo_url=report.photo_url or "https://images.unsplash.com/photo-1547683905-f686c993aae5?auto=format&fit=crop&w=600&q=80",
            description=report.description,
            estimated_clearance_hrs=report.estimated_clearance_hrs,
            reported_at=now_str,
            verification_status="PWD_CONFIRMED" if "PWD" in report.department else "VERIFIED_AI"
        )

        self.field_reports.insert(0, record.model_dump())

        # Automatically propagate hazard into the Digital Twin road network!
        self._propagate_field_report_to_twin(record)

        return record

    def _propagate_field_report_to_twin(self, record: FieldReportRecord):
        # Match nearest highway edge
        hw = record.nearest_highway.lower().replace("-", "").replace(" ", "")
        for edge in self.edges_state:
            e_hw = edge["highway_code"].lower().replace("-", "").replace(" ", "")
            if hw in e_hw or e_hw in hw:
                if record.severity in ("HIGH", "BLOCKING"):
                    edge["status"] = "warning"
                    edge["landslide_risk"] = max(edge["landslide_risk"], 85.0)
                    edge["closure_reason"] = f"Field Incident ({record.incident_type}): {record.description[:60]}..."
                break

        # Generate live emergency alert
        new_alert = {
            "id": f"alt_{uuid.uuid4().hex[:4]}",
            "timestamp": "Just Now",
            "severity": "CRITICAL_DANGER" if record.severity in ("HIGH", "BLOCKING") else "WARNING",
            "category": "LANDSLIDE" if "landslide" in record.incident_type.lower() else "ROAD_CLOSURE",
            "location_tag": f"{record.location_name} ({record.nearest_highway})",
            "message_en": f"LIVE DISPATCH: {record.incident_type} reported at {record.location_name}. {record.description}",
            "message_as": f"প্ৰত্যক্ষ প্ৰতিবেদন: {record.location_name} ত {record.incident_type} ৰ ঘটনা। যান-বাহন চালকসকল সতৰ্ক হওক।",
            "message_hi": f"ताज़ा रिपोर्ट: {record.location_name} पर {record.incident_type} की सूचना। यातायात प्रभावित।",
            "message_bn": f"তাজা খবর: {record.location_name} এ {record.incident_type} এর খবর। চালকদের সতর্ক থাকার পরামর্শ।",
            "affected_routes": [record.nearest_highway],
            "affected_districts": [record.location_name.split(",")[0]]
        }
        self.alerts.insert(0, new_alert)

    def tick_telemetry(self):
        """Simulate micro-movement for active vehicles along their routes"""
        for v in self.fleet:
            if v["status"] == "moving":
                # Slight realistic jitter along route
                lat, lng = v["current_coordinates"]
                lat += 0.0008 * (1 if int(v["id"][-1]) % 2 == 0 else -0.5)
                lng += 0.0009 * (1 if int(v["id"][-1]) % 2 == 0 else -0.5)
                v["current_coordinates"] = [round(lat, 5), round(lng, 5)]

fleet_manager = FleetAndFieldManager()
