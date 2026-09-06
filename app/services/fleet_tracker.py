"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Module 3, 4, 5, 6, 8 & 19: Fleet Telemetry, Field Incident Ingestion, Verification Lifecycle & Alert State Manager

Maintains:
- Live GPS vehicle telemetry with micro-kinetic updates
- Ingests Crowdsourced (65% confidence, Pending Verification) & Govt Employee (92% confidence, Emergency Flag) reports
- Closed-Loop Lifecycle: SUBMITTED -> PENDING_VERIFICATION -> VERIFIED / REJECTED -> ACTIVE_INCIDENT
- Propagates verified disruptions immediately into road graph status, alert tickers, and routing engine
- Batch Synchronization from Offline IndexedDB queue
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
    FieldReportVerifyRequest,
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

    def get_pending_reports(self) -> List[Dict[str, Any]]:
        return [r for r in self.field_reports if r.get("verification_status") == "PENDING_VERIFICATION"]

    def get_alerts(self) -> List[Dict[str, Any]]:
        return self.alerts

    def add_field_report(self, report: FieldReportCreate) -> FieldReportRecord:
        report_id = f"rpt_{uuid.uuid4().hex[:6]}"
        now_str = datetime.now().strftime("%I:%M %p, Today")

        is_gov = report.reporter_role in ("gov_employee", "admin") or any(k in report.department.upper() for k in ["PWD", "NDRF", "POLICE", "SDMA", "ENGINEER"])
        
        confidence = report.confidence_score or (92.0 if is_gov else 65.0)
        initial_status = "ACTIVE_INCIDENT" if (is_gov and report.emergency_flag) else ("PWD_CONFIRMED" if is_gov else "PENDING_VERIFICATION")

        record = FieldReportRecord(
            id=report_id,
            officer_name=report.officer_name,
            department=report.department,
            reporter_role=report.reporter_role,
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
            emergency_flag=report.emergency_flag,
            confidence_score=confidence,
            reported_at=now_str,
            verification_status=initial_status,
            verified_by=report.officer_name if is_gov else None,
            verified_at=now_str if is_gov else None
        )

        self.field_reports.insert(0, record.model_dump())

        # If verified / high severity, propagate into Digital Twin network immediately
        if initial_status in ("ACTIVE_INCIDENT", "PWD_CONFIRMED") or report.severity in ("HIGH", "BLOCKING"):
            self._propagate_field_report_to_twin(record)

        return record

    def verify_field_report(self, report_id: str, req: FieldReportVerifyRequest) -> Optional[Dict[str, Any]]:
        """Employee / Admin reviews and verifies or rejects a field report"""
        report = next((r for r in self.field_reports if r["id"] == report_id), None)
        if not report:
            return None

        now_str = datetime.now().strftime("%I:%M %p, Today")
        if req.action.upper() == "CONFIRM":
            report["verification_status"] = "ACTIVE_INCIDENT"
            report["confidence_score"] = max(report.get("confidence_score", 65.0), 95.0)
            report["verified_by"] = f"{req.verifier_name} ({req.verifier_department})"
            report["verified_at"] = now_str
            
            # Closed-Loop Promotion: Propagate into Twin road network & trigger Alert
            rec_obj = FieldReportRecord(**report)
            self._propagate_field_report_to_twin(rec_obj)
        else:
            report["verification_status"] = "REJECTED"
            report["verified_by"] = f"{req.verifier_name} ({req.verifier_department})"
            report["verified_at"] = now_str

        return report

    def sync_batch_offline_reports(self, reports: List[FieldReportCreate]) -> List[FieldReportRecord]:
        """Processes queued reports captured offline and restores database consistency"""
        synced_records = []
        for r in reports:
            rec = self.add_field_report(r)
            synced_records.append(rec)
        return synced_records

    def _propagate_field_report_to_twin(self, record: FieldReportRecord):
        # Match nearest highway edge by code/name
        hw = record.nearest_highway.lower().replace("-", "").replace(" ", "")
        matched_edge = None
        for edge in self.edges_state:
            e_hw = edge["highway_code"].lower().replace("-", "").replace(" ", "")
            if hw and (hw in e_hw or e_hw in hw):
                matched_edge = edge
                break

        # Spatial fallback: match by geographical proximity to report coordinates
        if not matched_edge and record.latitude and record.longitude:
            node_coords = {n["id"]: n["coordinates"] for n in NER_DISTRICT_NODES}
            best_dist = float("inf")
            for edge in self.edges_state:
                c1 = node_coords.get(edge["source"])
                c2 = node_coords.get(edge["target"])
                if c1 and c2:
                    mid_lat = (c1[0] + c2[0]) / 2.0
                    mid_lng = (c1[1] + c2[1]) / 2.0
                    d = (mid_lat - record.latitude)**2 + (mid_lng - record.longitude)**2
                    if d < best_dist:
                        best_dist = d
                        matched_edge = edge

        if matched_edge:
            if record.severity in ("HIGH", "BLOCKING"):
                matched_edge["status"] = "blocked" if record.severity == "BLOCKING" else "warning"
                matched_edge["landslide_risk"] = max(matched_edge.get("landslide_risk", 10.0), 88.0)
                matched_edge["closure_reason"] = f"Verified Incident ({record.incident_type}): {record.description[:60]}..."
                
                # Check if active freight convoys are delayed
                for v in self.fleet:
                    if matched_edge["highway_code"].lower() in v.get("route_id", "").lower() or matched_edge["source"] in v.get("destination", "").lower():
                        v["status"] = "delayed"
                        v["delay_reason"] = f"Corridor severed by verified {record.incident_type}"

        # Propagate closed-loop graph update to routing engine immediately
        try:
            from app.services.routing_engine import smart_route_engine
            smart_route_engine.build_graph()
        except Exception:
            pass

        # Generate live emergency alert
        new_alert = {
            "id": f"alt_{uuid.uuid4().hex[:4]}",
            "timestamp": "Just Now",
            "severity": "CRITICAL_DANGER" if record.severity in ("HIGH", "BLOCKING") else "WARNING",
            "category": "LANDSLIDE" if "landslide" in record.incident_type.lower() else ("FLOOD" if "flood" in record.incident_type.lower() else "ROAD_CLOSURE"),
            "location_tag": f"{record.location_name} ({record.nearest_highway})",
            "message_en": f"VERIFIED DISPATCH: {record.incident_type} at {record.location_name}. {record.description}",
            "message_as": f"প্ৰমাণিত প্ৰতিবেদন: {record.location_name} ত {record.incident_type} ৰ ঘটনা। যান-বাহন চালকসকল সতৰ্ক হওক।",
            "message_hi": f"सत्यापित सूचना: {record.location_name} पर {record.incident_type}। सावधानी बरतें।",
            "message_bn": f"যাচাইকৃত রিপোর্ট: {record.location_name} এ {record.incident_type}। বিকল্প রুট ব্যবহার করুন।",
            "affected_routes": [record.nearest_highway],
            "affected_districts": [record.location_name.split(",")[0]]
        }
        self.alerts.insert(0, new_alert)

    def tick_telemetry(self):
        """Simulate micro-movement for active vehicles along their routes"""
        for v in self.fleet:
            if v["status"] == "moving":
                lat, lng = v["current_coordinates"]
                lat += 0.0008 * (1 if int(v["id"][-1]) % 2 == 0 else -0.5)
                lng += 0.0009 * (1 if int(v["id"][-1]) % 2 == 0 else -0.5)
                v["current_coordinates"] = [round(lat, 5), round(lng, 5)]

fleet_manager = FleetAndFieldManager()
