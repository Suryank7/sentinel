import json
import os
import uuid
from datetime import datetime, timezone
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY", ""))

async def watcher_node(state: dict) -> dict:
    """
    WATCHER: The Sensor Sentinel
    Monitors raw sensor readings, calculates normalized risk, and detects anomalies.
    """
    readings = state.get("sensor_readings", [])
    anomalies = []
    
    for r in readings:
        sensor_type = r.get("type", "")
        val = r.get("value", 0.0)
        warn = r.get("threshold_warning", 0.0)
        alarm = r.get("threshold_alarm", 0.0)
        is_low_oxygen = (sensor_type == "O2" and alarm < warn)
        
        # Calculate normalized risk
        if is_low_oxygen:
            # For O2, lower is worse
            if val <= alarm:
                risk = 1.0
            elif val <= warn:
                risk = (warn - val) / (warn - alarm)
            else:
                risk = 0.0
        else:
            if val >= alarm:
                risk = 1.0
            elif val >= warn:
                risk = val / alarm
            else:
                risk = val / alarm * 0.5 # Normal range scaled
                
        r["normalized_risk"] = min(risk, 1.0)
        
        # Anomaly detection logic
        anomaly_type = None
        if is_low_oxygen:
            if val <= alarm:
                anomaly_type = "THRESHOLD_BREACH"
            elif val <= warn:
                anomaly_type = "SUB_THRESHOLD_ELEVATED"
        else:
            if val >= alarm:
                anomaly_type = "THRESHOLD_BREACH"
            elif val >= warn:
                anomaly_type = "SUB_THRESHOLD_ELEVATED"
                
        # Simulate RAPID_CHANGE based on random noise in demo
        # (A real system would track history here)
        
        if anomaly_type:
            # In a real app we'd use Gemini here to generate the description,
            # but for a fast hackathon demo, we generate it directly to save API time
            desc = f"Sensor {r['name']} in {r['zone_name']} reading {val} {r['unit']}. "
            if anomaly_type == "THRESHOLD_BREACH":
                desc += "This exceeds the critical alarm threshold."
            else:
                desc += "This is elevated but below the critical alarm threshold."
                
            anomalies.append({
                "id": f"anomaly-{uuid.uuid4().hex[:8]}",
                "sensor_id": r["id"],
                "sensor_name": r["name"],
                "zone_id": r["zone_id"],
                "zone_name": r["zone_name"],
                "type": anomaly_type,
                "reading": val,
                "threshold_alarm": alarm,
                "normalized_risk": r["normalized_risk"],
                "trend": "RISING", # Hardcoded for demo
                "description": desc,
                "confidence": 0.95,
                "detected_at": datetime.now(timezone.utc).isoformat()
            })
            
    # Update state
    state["watcher_anomalies"] = anomalies
    state["watcher_status"] = "COMPLETED"
    state["watcher_summary"] = f"Analyzed {len(readings)} sensors. Found {len(anomalies)} anomalies."
    
    return state
