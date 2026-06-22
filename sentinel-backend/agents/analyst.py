import uuid
import os
from datetime import datetime, timezone
import google.generativeai as genai
from services.crs_engine import assemble_crs, calculate_regulatory_violation_score

genai.configure(api_key=os.getenv("GOOGLE_API_KEY", ""))

async def analyst_node(state: dict) -> dict:
    """
    ANALYST: The Risk Calculator
    Runs the Compound Risk Score engine.
    """
    anomalies = state.get("watcher_anomalies", [])
    flags = state.get("auditor_flags", [])
    zones = {z["id"]: z for z in state.get("zones", [])}
    
    # Simple hackathon logic: if we have both anomalies and flags in the same zone, it's a compound risk
    risk_events = []
    
    # Group by zone
    zone_risks = {}
    for a in anomalies:
        zone_risks.setdefault(a["zone_id"], {"sensors": [], "permits": []})
        zone_risks[a["zone_id"]]["sensors"].append({
            "name": a["sensor_name"],
            "value": a["normalized_risk"],
            "type": a["sensor_name"].split()[0].replace("₂", "2").replace("₄", "4"), # Hack to get type
            "proximity": 1.0
        })
        
    for f in flags:
        for z_id in f["zone_ids"]:
            zone_risks.setdefault(z_id, {"sensors": [], "permits": []})
            zone_risks[z_id]["permits"].append({
                "name": f"Permit {f['permit_ids'][0]}",
                "value": 0.8 if "CRITICAL" in f["severity"] else 0.5,
                "type": "HOT_WORK" if "Hot Work" in f["description"] else "GENERAL",
                "proximity": 0.85 # Assume adjacent
            })
            
    # Calculate CRS per zone
    for z_id, risks in zone_risks.items():
        if not risks["sensors"] and not risks["permits"]:
            continue
            
        # Add operational risk (Shift changeover simulation)
        op_risks = [
            {"name": "Shift Changeover", "value": 0.5, "category": "OPERATIONAL", "type": "SHIFT"}
        ]
        
        reg_score = calculate_regulatory_violation_score([{"severity": "CRITICAL"}]) if risks["permits"] else 0.0
        
        crs_result = assemble_crs(
            sensor_risks=risks["sensors"],
            permit_risks=risks["permits"],
            operational_risks=op_risks,
            cascade_factor=1.0,
            cascade_reason="",
            regulatory_violation_score=reg_score
        )
        
        if crs_result.score > 0.15:
            # Generate description with Gemini (simulated here for speed if no API key)
            if os.getenv("GOOGLE_API_KEY"):
                model = genai.GenerativeModel("gemini-2.5-flash")
                prompt = f"Write a 2 sentence compound risk analysis for a steel plant. Zone: {zones.get(z_id, {}).get('name', 'Unknown')}. Risk score: {crs_result.score} ({crs_result.severity}). Factors: {len(risks['sensors'])} sensors anomalous, {len(risks['permits'])} permit conflicts."
                try:
                    desc = model.generate_content(prompt).text
                except:
                    desc = f"Compound risk detected in {zones.get(z_id, {}).get('name', 'Unknown')} with score {crs_result.score}."
            else:
                desc = f"Compound risk detected in {zones.get(z_id, {}).get('name', 'Unknown')} with score {crs_result.score}."
                
            risk_factors = []
            for r in risks["sensors"]: risk_factors.append({"name": r["name"], "value": r["value"], "category": "GAS"})
            for r in risks["permits"]: risk_factors.append({"name": r["name"], "value": r["value"], "category": "PERMIT"})
            for r in op_risks: risk_factors.append({"name": r["name"], "value": r["value"], "category": "OPERATIONAL"})

            risk_events.append({
                "id": f"risk-{uuid.uuid4().hex[:8]}",
                "crs_score": crs_result.score,
                "severity": crs_result.severity,
                "title": f"Compound Risk in {zones.get(z_id, {}).get('name', 'Unknown')}",
                "description": desc,
                "zones_affected": [z_id],
                "workers_at_risk": 15, # Hardcoded for demo
                "risk_factors": risk_factors,
                "cascade_factor": crs_result.breakdown["cascade_factor"],
                "cascade_reason": crs_result.breakdown["cascade_reason"],
                "regulatory_violations": ["OISD-STD-105 Section 4.3"] if risks["permits"] else [],
                "crs_breakdown": crs_result.breakdown,
                "detected_at": datetime.now(timezone.utc).isoformat()
            })
            
    state["risk_events"] = risk_events
    state["analyst_status"] = "COMPLETED"
    state["analyst_summary"] = f"Calculated CRS for {len(zone_risks)} zones. Found {len(risk_events)} risk events."
    
    return state
