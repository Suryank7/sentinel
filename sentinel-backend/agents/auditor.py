import uuid
from datetime import datetime, timezone

async def auditor_node(state: dict) -> dict:
    """
    AUDITOR: The Compliance Watchdog
    Checks for permit conflicts and regulatory deviations.
    """
    permits = state.get("active_permits", [])
    zones = {z["id"]: z for z in state.get("zones", [])}
    
    flags = []
    deviations = []
    
    # 1. Check for permit spatial conflicts
    # Group permits by zone
    permits_by_zone = {}
    for p in permits:
        permits_by_zone.setdefault(p["zone_id"], []).append(p)
        
    for zone_id, zone_permits in permits_by_zone.items():
        if len(zone_permits) > 1:
            types = [p["type"] for p in zone_permits]
            if "HOT_WORK" in types and "CONFINED_SPACE" in types:
                flags.append({
                    "id": f"flag-{uuid.uuid4().hex[:8]}",
                    "type": "PERMIT_CONFLICT",
                    "severity": "CRITICAL",
                    "description": "Hot Work and Confined Space permits active simultaneously in same zone.",
                    "permit_ids": [p["id"] for p in zone_permits],
                    "zone_ids": [zone_id],
                    "regulation_reference": "IS 17893:2023 Section 5.4",
                    "detected_at": datetime.now(timezone.utc).isoformat()
                })
                deviations.append({"severity": "CRITICAL"})
                
    # 2. Cross-reference permits with WATCHER anomalies
    anomalies = state.get("watcher_anomalies", [])
    anomaly_zones = {a["zone_id"]: a for a in anomalies}
    
    for p in permits:
        if p["type"] == "HOT_WORK" and p["zone_id"] in anomaly_zones:
            anomaly = anomaly_zones[p["zone_id"]]
            if anomaly["type"] == "SUB_THRESHOLD_ELEVATED" or anomaly["type"] == "THRESHOLD_BREACH":
                flags.append({
                    "id": f"flag-{uuid.uuid4().hex[:8]}",
                    "type": "PERMIT_CONFLICT",
                    "severity": "CRITICAL",
                    "description": f"Hot Work Permit {p['id']} active near elevated gas readings.",
                    "permit_ids": [p["id"]],
                    "zone_ids": [p["zone_id"]],
                    "regulation_reference": "OISD-STD-105 Section 4.3",
                    "detected_at": datetime.now(timezone.utc).isoformat()
                })
                deviations.append({"severity": "CRITICAL"})

    # Calculate mock compliance score
    total_checks = 45
    num_deviations = len(deviations) + 5 # adding some mock minor ones
    score = int((total_checks - num_deviations) / total_checks * 100)
    
    state["auditor_flags"] = flags
    state["compliance_status"] = {
        "overall_score": score,
        "total_checks": total_checks,
        "deviations": num_deviations,
        "critical_deviations": len([d for d in deviations if d["severity"] == "CRITICAL"])
    }
    state["auditor_status"] = "COMPLETED"
    state["auditor_summary"] = f"Checked {len(permits)} permits. Found {len(flags)} conflicts."
    
    return state
