from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END
import asyncio

from agents.watcher import watcher_node
from agents.auditor import auditor_node
from agents.analyst import analyst_node
from agents.oracle import oracle_node
from agents.scribe import scribe_node
from agents.guardian import guardian_node

class SentinelState(TypedDict):
    sensor_readings: List[Dict]
    active_permits: List[Dict]
    workers: List[Dict]
    zones: List[Dict]
    equipment: List[Dict]
    
    watcher_anomalies: List[Dict]
    watcher_status: str
    watcher_summary: str
    
    auditor_flags: List[Dict]
    compliance_status: Dict
    auditor_status: str
    auditor_summary: str
    
    risk_events: List[Dict]
    analyst_status: str
    analyst_summary: str
    
    predictions: List[Dict]
    oracle_status: str
    oracle_summary: str
    
    safety_reports: List[Dict]
    scribe_status: str
    
    emergency_actions: List[Dict]
    guardian_status: str
    guardian_summary: str
    
    run_id: str
    timestamp: str
    demo_mode: bool
    errors: List[str]

def build_sentinel_graph():
    graph = StateGraph(SentinelState)
    
    graph.add_node("watcher", watcher_node)
    graph.add_node("auditor", auditor_node)
    graph.add_node("analyst", analyst_node)
    graph.add_node("oracle", oracle_node)
    graph.add_node("scribe", scribe_node)
    graph.add_node("guardian", guardian_node)
    
    # We run watcher and auditor sequentially to emulate parallel 
    # since we just pass the state through
    graph.set_entry_point("watcher")
    graph.add_edge("watcher", "auditor")
    graph.add_edge("auditor", "analyst")
    
    def after_analyst(state: SentinelState):
        if any(r["crs_score"] > 0.35 for r in state.get("risk_events", [])):
            return "oracle"
        return "end"
        
    graph.add_conditional_edges(
        "analyst",
        after_analyst,
        {"oracle": "oracle", "end": END}
    )
    
    graph.add_edge("oracle", "scribe")
    
    def after_scribe(state: SentinelState):
        if any(r["severity"] == "CRITICAL" for r in state.get("risk_events", [])):
            return "guardian"
        return "end"
        
    graph.add_conditional_edges(
        "scribe",
        after_scribe,
        {"guardian": "guardian", "end": END}
    )
    
    graph.add_edge("guardian", END)
    
    return graph.compile()
