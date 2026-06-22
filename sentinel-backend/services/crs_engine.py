from typing import List, Dict, Tuple, Optional
from datetime import datetime, timezone

class CRSResult:
    def __init__(self, score: float, severity: str, breakdown: Dict):
        self.score = score
        self.severity = severity
        self.breakdown = breakdown

PROXIMITY_WEIGHTS = {
    "SAME_ZONE": 1.0,
    "ADJACENT_ZONE": 0.7,
    "NEARBY_ZONE": 0.3,
    "DISTANT_ZONE": 0.1,
}

CASCADE_FACTORS = {
    ("FLAMMABLE_GAS", "HOT_WORK"): 3.5,
    ("FLAMMABLE_GAS", "ELECTRICAL_WORK"): 2.8,
    ("TOXIC_GAS", "CONFINED_SPACE"): 3.0,
    ("LOW_OXYGEN", "CONFINED_SPACE"): 3.2,
    ("HIGH_PRESSURE", "MAINTENANCE"): 2.5,
    ("HIGH_TEMPERATURE", "PERSONNEL_NEARBY"): 2.0,
    ("SHIFT_CHANGEOVER", "HAZARDOUS_WORK"): 1.8,
    ("MAINTENANCE_OVERDUE", "HAZARDOUS_OPERATION"): 2.2,
}

def get_proximity_weight(zone_a: str, zone_b: str, adjacency_map: Dict[str, List[str]]) -> float:
    if zone_a == zone_b:
        return PROXIMITY_WEIGHTS["SAME_ZONE"]
    if zone_b in adjacency_map.get(zone_a, []):
        return PROXIMITY_WEIGHTS["ADJACENT_ZONE"]
    # For hackathon, assuming if it's not same or adjacent, it's distant
    return PROXIMITY_WEIGHTS["DISTANT_ZONE"]

def calculate_cascade_factor(active_risk_types: List[str]) -> float:
    max_cascade = 1.0
    for i in range(len(active_risk_types)):
        for j in range(i + 1, len(active_risk_types)):
            pair1 = (active_risk_types[i], active_risk_types[j])
            pair2 = (active_risk_types[j], active_risk_types[i])
            if pair1 in CASCADE_FACTORS:
                max_cascade = max(max_cascade, CASCADE_FACTORS[pair1])
            if pair2 in CASCADE_FACTORS:
                max_cascade = max(max_cascade, CASCADE_FACTORS[pair2])
    return max_cascade

def calculate_regulatory_violation_score(deviations: List[Dict]) -> float:
    score = 0.0
    for dev in deviations:
        if dev["severity"] == "CRITICAL":
            score += 0.25
        elif dev["severity"] == "MAJOR":
            score += 0.15
        elif dev["severity"] == "MINOR":
            score += 0.05
    return min(score, 0.5)

def assemble_crs(
    sensor_risks: List[Dict],
    permit_risks: List[Dict],
    operational_risks: List[Dict],
    cascade_factor: float,
    cascade_reason: str,
    regulatory_violation_score: float
) -> CRSResult:
    weighted_sum = 0.0
    individual_factors = []
    active_risk_types = []

    # Category Weights
    W_GAS = 0.35
    W_PERMIT = 0.25
    W_OP = 0.10
    W_EQUIP = 0.20

    for sr in sensor_risks:
        val = sr["value"] * W_GAS * sr.get("proximity", 1.0)
        weighted_sum += val
        individual_factors.append({
            "name": sr["name"],
            "value": sr["value"],
            "weight": W_GAS,
            "contribution": val
        })
        if sr["type"] in ["H2S", "CO"]:
            active_risk_types.append("TOXIC_GAS")
        elif sr["type"] == "CH4":
            active_risk_types.append("FLAMMABLE_GAS")
        elif sr["type"] == "O2" and sr.get("is_low", False):
            active_risk_types.append("LOW_OXYGEN")

    for pr in permit_risks:
        val = pr["value"] * W_PERMIT * pr.get("proximity", 1.0)
        weighted_sum += val
        individual_factors.append({
            "name": pr["name"],
            "value": pr["value"],
            "weight": W_PERMIT,
            "contribution": val
        })
        if "HOT_WORK" in pr["type"]:
            active_risk_types.append("HOT_WORK")
        elif "CONFINED" in pr["type"]:
            active_risk_types.append("CONFINED_SPACE")

    for opr in operational_risks:
        w = W_EQUIP if opr["category"] == "EQUIPMENT" else W_OP
        val = opr["value"] * w
        weighted_sum += val
        individual_factors.append({
            "name": opr["name"],
            "value": opr["value"],
            "weight": w,
            "contribution": val
        })
        if "Shift" in opr["name"]:
            active_risk_types.append("SHIFT_CHANGEOVER")
        if "Maintenance" in opr["name"]:
            active_risk_types.append("MAINTENANCE_OVERDUE")

    if cascade_factor == 1.0:
        cascade_factor = calculate_cascade_factor(active_risk_types)
        if cascade_factor > 1.0:
            cascade_reason = "Auto-detected Cascade"

    base_score = min(weighted_sum, 1.0)
    cascaded_score = base_score * cascade_factor
    final_score = cascaded_score * (1 + regulatory_violation_score)
    crs = min(final_score, 1.0)

    if crs > 0.85:
        severity = "CRITICAL"
    elif crs > 0.60:
        severity = "HIGH"
    elif crs > 0.35:
        severity = "MEDIUM"
    elif crs > 0.15:
        severity = "LOW"
    else:
        severity = "NORMAL"

    breakdown = {
        "base_score": round(base_score, 3),
        "cascade_factor": cascade_factor,
        "cascade_reason": cascade_reason,
        "regulatory_penalty": round(regulatory_violation_score, 3),
        "individual_factors": individual_factors
    }

    return CRSResult(score=round(crs, 3), severity=severity, breakdown=breakdown)
