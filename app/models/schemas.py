"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Pydantic v2 Request, Response, and Graph Entity Validation Schemas
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# --- Digital Twin Graph Schemas ---
class GeoPoint(BaseModel):
    lat: float
    lng: float

class DistrictNode(BaseModel):
    id: str
    name: str
    state: str
    coordinates: List[float] # [lat, lng]
    status: str = "connected" # "connected", "limited", "disconnected"
    hospitals: int = 1
    population: int
    stock_oxygen_days: float
    stock_rations_days: float
    stock_medicines_days: float
    critical_alert: Optional[str] = None

class BridgeNode(BaseModel):
    id: str
    name: str
    river: str
    state: str
    coordinates: List[float]
    status: str = "operational" # "operational", "caution", "submerged", "damaged", "closed"
    structural_health: float = 98.0 # %
    water_level_m: float = 4.2
    danger_mark_m: float = 8.5
    vulnerability_score: float = 12.0 # %

class RoadEdge(BaseModel):
    id: str
    highway_code: str
    source: str
    target: str
    distance_km: float
    avg_speed_kmh: float
    elevation_gain_m: float
    slope_deg: float
    terrain_type: str # "plains", "hilly", "steep_gorge", "floodplain"
    status: str = "open" # "open", "warning", "critical", "blocked"
    landslide_risk: float = 10.0 # 0-100%
    flood_risk: float = 5.0 # 0-100%
    rainfall_mm: float = 12.0
    closure_reason: Optional[str] = None
    coordinates_polyline: List[List[float]]

# --- Fleet & GPS Schemas ---
class VehicleTelemetry(BaseModel):
    id: str
    vehicle_number: str
    driver_name: str
    driver_phone: str
    vehicle_type: str # "Heavy Truck", "Refrigerated Van", "Tanker (Oxygen)", "Light Carrier"
    cargo_type: str # "Liquid Medical Oxygen", "Cold-Chain Vaccines", "FCI Rice & Wheat Rations", "Diesel/LPG", "Disaster Relief Kits"
    cargo_priority: str # "CRITICAL_LIFE_SAVING", "HIGH", "STANDARD"
    cargo_weight_tons: float
    source: str
    destination: str
    current_coordinates: List[float]
    speed_kmh: float
    heading_deg: float
    status: str # "moving", "delayed", "rerouted", "halted_danger"
    delay_minutes: int = 0
    assigned_route_id: Optional[str] = None
    eta_timestamp: str

# --- AI Prediction Schemas ---
class LandslidePredictionRequest(BaseModel):
    rainfall_mm: float = Field(..., ge=0, le=500, description="24h cumulative rainfall in mm")
    slope_degrees: float = Field(..., ge=0, le=90, description="Terrain slope angle in degrees")
    soil_saturation_pct: float = Field(..., ge=0, le=100, description="Soil volumetric moisture saturation %")
    historical_landslide_count: int = Field(default=3, ge=0, le=50, description="Past landslides within 5km in last 10 years")
    seismic_zone: int = Field(default=5, ge=1, le=5, description="Seismic Hazard Zone (Zone V for NER)")
    vegetation_index: float = Field(default=0.45, ge=0.0, le=1.0, description="Normalized Difference Vegetation Index (NDVI)")

class FactorWeight(BaseModel):
    name: str
    contribution_pct: float
    description: str

class LandslidePredictionResponse(BaseModel):
    landslide_risk_pct: float
    risk_level: str # "LOW", "MODERATE", "HIGH", "SEVERE", "CATASTROPHIC"
    action_protocol: str
    factor_breakdown: List[FactorWeight]
    model_confidence: float

class FloodPredictionRequest(BaseModel):
    rainfall_mm: float
    river_discharge_cumec: float
    current_gauge_m: float
    danger_mark_m: float
    catchment_elevation_m: float

class FloodPredictionResponse(BaseModel):
    flood_risk_pct: float
    risk_tier: str
    time_to_inundation_hours: float
    submergence_depth_m: float
    recommended_bypass: Optional[str]

# --- Route Optimization Schemas ---
class RouteRequest(BaseModel):
    source_id: str
    destination_id: str
    vehicle_type: str = "Heavy Truck"
    cargo_priority: str = "CRITICAL_LIFE_SAVING"
    avoid_high_risk: bool = True
    custom_avoid_nodes: List[str] = []
    custom_avoid_edges: List[str] = []

class RouteSegment(BaseModel):
    edge_id: str
    name: str
    distance_km: float
    travel_time_min: float
    landslide_risk: float
    flood_risk: float
    status: str
    instructions: str
    coordinates: List[List[float]]

class RoutePlan(BaseModel):
    route_id: str
    is_primary: bool
    title: str
    total_distance_km: float
    total_travel_time_hours: float
    aggregate_risk_score: float # 0 - 100
    landslide_exposure_km: float
    flood_exposure_km: float
    segments: List[RouteSegment]
    path_coordinates: List[List[float]]
    summary: str
    weather_advisory: str
    red_zone_count: int = 0
    ai_risk_breakdown: Optional[Dict[str, Any]] = None

class RouteOptimizationResponse(BaseModel):
    source_name: str
    destination_name: str
    recommended_route: RoutePlan
    alternative_route: Optional[RoutePlan] = None
    contingency_detour: Optional[RoutePlan] = None
    delay_delta_minutes: int
    risk_reduction_pct: float
    red_zones_avoided: int = 0
    ai_risk_breakdown: Optional[Dict[str, Any]] = None

# --- Simulation Schemas ---
class DisasterSimulationRequest(BaseModel):
    scenario_id: str # "bridge_collapse", "landslide_blockage", "monsoon_flood", "custom"
    target_node_id: Optional[str] = None
    target_edge_id: Optional[str] = None
    disaster_severity: str = "HIGH" # "MODERATE", "HIGH", "TOTAL_BREACH"
    weather_multiplier: float = 1.5

class IsolatedDistrictReport(BaseModel):
    district_id: str
    district_name: str
    state: str
    population_impacted: int
    days_oxygen_left: float
    days_food_left: float
    isolation_tier: str # "FULLY_CUT_OFF", "RESTRICTED_ACCESS", "AIR_DROP_ONLY"

class AffectedVehicleReport(BaseModel):
    vehicle_id: str
    vehicle_number: str
    cargo_type: str
    cargo_priority: str
    destination: str
    current_status: str
    estimated_delay_hrs: float
    suggested_reroute_id: Optional[str]

class DisasterSimulationResponse(BaseModel):
    scenario_title: str
    incident_location: str
    impact_timestamp: str
    isolated_districts: List[IsolatedDistrictReport]
    total_population_affected: int
    delayed_vehicles: List[AffectedVehicleReport]
    critical_supplies_at_risk: Dict[str, Any]
    ai_generated_reroutes: List[RoutePlan]
    emergency_action_recommendations: List[str]
    connectivity_matrix: Dict[str, str]

# --- Field Reports Schemas ---
class FieldReportCreate(BaseModel):
    officer_name: str
    department: str = "Local Citizen" # "PWD Engineer", "Traffic Police", "NDRF", "Commercial Driver", "Local Citizen"
    reporter_role: str = "user" # "user", "gov_employee", "admin"
    incident_type: str # "Landslide", "Flash Flood", "Road Blockage", "Accident", "Damaged Road", "Weather Hazard", "Other"
    severity: str = "HIGH" # "LOW", "MEDIUM", "HIGH", "BLOCKING"
    latitude: float
    longitude: float
    location_name: str
    nearest_highway: str
    photo_base64: Optional[str] = None
    photo_url: Optional[str] = None
    description: str
    estimated_clearance_hrs: float = 6.0
    emergency_flag: bool = False
    confidence_score: Optional[float] = 65.0

class FieldReportVerifyRequest(BaseModel):
    action: str # "CONFIRM" or "REJECT"
    verifier_name: str = "District Incident Commander"
    verifier_department: str = "SDMA / PWD"
    notes: Optional[str] = None

class FieldReportRecord(FieldReportCreate):
    id: str
    reported_at: str
    verification_status: str = "PENDING_VERIFICATION" # "SUBMITTED", "PENDING_VERIFICATION", "VERIFIED", "REJECTED", "ACTIVE_INCIDENT"
    verified_by: Optional[str] = None
    verified_at: Optional[str] = None

# --- Alert Broadcast Schemas ---
class EmergencyAlert(BaseModel):
    id: str
    timestamp: str
    severity: str # "INFO", "WARNING", "CRITICAL_DANGER"
    category: str # "LANDSLIDE", "FLOOD", "ROAD_CLOSURE", "WEATHER"
    location_tag: str
    message_en: str
    message_as: str # Assamese
    message_hi: str # Hindi
    message_bn: str # Bengali
    affected_routes: List[str]
    affected_districts: List[str]
