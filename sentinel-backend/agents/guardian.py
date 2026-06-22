import uuid
from datetime import datetime, timezone

async def guardian_node(state: dict) -> dict:
    """
    GUARDIAN: The Emergency Response Orchestrator
    Initiates emergency response actions based on risk severity.
    """
    risk_events = state.get("risk_events", [])
    actions = []
    
    for re in risk_events:
        severity = re["severity"]
        if severity in ["CRITICAL", "HIGH"]:
            # Auto-alert officer
            actions.append({
                "id": f"action-{uuid.uuid4().hex[:8]}",
                "risk_event_id": re["id"],
                "type": "ALERT_OFFICER",
                "description": f"Alert Safety Officer: {severity} risk in {re['zones_affected']}",
                "target": "Safety Officer",
                "urgency": "IMMEDIATE",
                "requires_confirmation": False,
                "status": "COMPLETED",
                "executed_at": datetime.now(timezone.utc).isoformat()
            })
            
            # Extract permits from risk factors
            permits = [f for f in re["risk_factors"] if f["category"] == "PERMIT"]
            
            for p in permits:
                action_status = "COMPLETED" if severity == "CRITICAL" else "PROPOSED"
                actions.append({
                    "id": f"action-{uuid.uuid4().hex[:8]}",
                    "risk_event_id": re["id"],
                    "type": "SUSPEND_PERMIT",
                    "description": f"Suspend Permit {p['name']}",
                    "target": p['name'],
                    "urgency": "IMMEDIATE",
                    "requires_confirmation": severity != "CRITICAL",
                    "status": action_status,
                    "executed_at": datetime.now(timezone.utc).isoformat() if action_status == "COMPLETED" else None
                })
                
            if severity == "CRITICAL":
                actions.append({
                    "id": f"action-{uuid.uuid4().hex[:8]}",
                    "risk_event_id": re["id"],
                    "type": "EVACUATE_ZONE",
                    "description": f"Evacuate {re['workers_at_risk']} workers from {re['zones_affected']}",
                    "target": str(re['zones_affected']),
                    "urgency": "IMMEDIATE",
                    "requires_confirmation": False,
                    "status": "EXECUTING",
                    "executed_at": datetime.now(timezone.utc).isoformat()
                })
                
    state["emergency_actions"] = actions
    state["guardian_status"] = "COMPLETED"
    state["guardian_summary"] = f"Generated {len(actions)} emergency actions."
    
    return state
