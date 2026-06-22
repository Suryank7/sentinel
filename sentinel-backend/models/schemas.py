from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class SensorReading(BaseModel):
    sensor_id: str
    value: float
    unit: str
    timestamp: str

class Anomaly(BaseModel):
    id: str
    sensor_id: str
    sensor_name: str
    zone_id: str
    zone_name: str
    type: str
    reading: float
    threshold_alarm: float
    normalized_risk: float
    trend: str
    description: str
    confidence: float
    detected_at: str

class PermitFlag(BaseModel):
    id: str
    type: str
    severity: str
    description: str
    permit_ids: List[str]
    zone_ids: List[str]
    regulation_reference: Optional[str] = None
    detected_at: str

class RiskEvent(BaseModel):
    id: str
    crs_score: float
    severity: str
    title: str
    description: str
    zones_affected: List[str]
    workers_at_risk: int
    risk_factors: List[Dict]
    cascade_factor: float
    cascade_reason: Optional[str] = None
    regulatory_violations: List[str]
    crs_breakdown: Dict
    detected_at: str

class IncidentPrediction(BaseModel):
    risk_event_id: str
    incident_probability: Dict[str, float]
    trend: str
    trend_acceleration: float
    confidence: float
    similar_incidents: List[Dict]
    intervention_window: str
    predicted_at: str

class SafetyReport(BaseModel):
    risk_event_id: str
    headline: str
    report_text: str
    regulatory_citations: List[str]
    similar_incidents_referenced: List[str]
    generated_at: str

class EmergencyAction(BaseModel):
    id: str
    risk_event_id: str
    type: str
    description: str
    target: str
    urgency: str
    requires_confirmation: bool
    status: str
    executed_at: Optional[str] = None

class DashboardMetrics(BaseModel):
    active_risks: int
    critical_risks: int
    workers_on_site: int
    workers_safe: int
    overall_crs: float
    compliance_score: int
    active_permits: int
    sensors_online: int
    sensors_anomaly: int
    last_updated: str
