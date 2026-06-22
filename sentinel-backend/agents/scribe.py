import uuid
import os
from datetime import datetime, timezone
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY", ""))

async def scribe_node(state: dict) -> dict:
    """
    SCRIBE: The Safety Intelligence Reporter
    Generates human-readable safety reports with regulatory citations.
    """
    risk_events = state.get("risk_events", [])
    predictions = {p["risk_event_id"]: p for p in state.get("predictions", [])}
    
    reports = []
    
    for re in risk_events:
        if re["severity"] in ["CRITICAL", "HIGH"]:
            pred = predictions.get(re["id"], {})
            
            # Simulated RAG context for demo speed
            sim_incidents = "Visakhapatnam Steel Plant Explosion (June 2026)"
            reg_citations = re.get("regulatory_violations", [])
            
            if os.getenv("GOOGLE_API_KEY"):
                model = genai.GenerativeModel("gemini-2.5-flash")
                prompt = f"""
                You are SCRIBE, a safety intelligence reporter.
                Write a brief safety report based ONLY on this context:
                Risk: {re['title']} ({re['severity']})
                Factors: {[f['name'] for f in re['risk_factors']]}
                Prediction: {pred.get('incident_probability', {}).get('1_hour', 'N/A') * 100}% in 1hr.
                Regulations: {reg_citations}
                Historical precedent: {sim_incidents}
                
                Format as a professional 3-sentence summary.
                """
                try:
                    report_text = model.generate_content(prompt).text
                except:
                    report_text = f"CRITICAL COMPOUND RISK ALERT. Factors detected: {[f['name'] for f in re['risk_factors']]}. Prediction: {pred.get('incident_probability', {}).get('1_hour', 'N/A') * 100}% probability in 1 hour. Reference: {sim_incidents}. Ensure compliance with {reg_citations}."
            else:
                report_text = f"CRITICAL COMPOUND RISK ALERT. Factors detected: {[f['name'] for f in re['risk_factors']]}. Prediction: {pred.get('incident_probability', {}).get('1_hour', 'N/A') * 100}% probability in 1 hour. Reference: {sim_incidents}. Ensure compliance with {reg_citations}."

            reports.append({
                "risk_event_id": re["id"],
                "headline": f"{re['severity']}: {re['title']}",
                "report_text": report_text,
                "regulatory_citations": reg_citations,
                "similar_incidents_referenced": [sim_incidents],
                "generated_at": datetime.now(timezone.utc).isoformat()
            })
            
    state["safety_reports"] = reports
    state["scribe_status"] = "COMPLETED"
    
    return state
