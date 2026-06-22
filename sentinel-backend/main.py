import os
import asyncio
import json
import uuid
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from typing import List, Dict, Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
import aiosqlite

from config import DEMO_DURATION_SECONDS
from database import DB_PATH, init_db
from data.seed_data import seed_data
from models.schemas import DashboardMetrics
from agents.orchestrator import build_sentinel_graph, SentinelState

# Global event queue for SSE
event_queues: List[asyncio.Queue] = []
graph = build_sentinel_graph()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB on startup
    await init_db()
    await seed_data()
    yield
    # Cleanup on shutdown

app = FastAPI(title="SENTINEL Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def broadcast_event(event_type: str, data: dict):
    for queue in event_queues:
        await queue.put({"type": event_type, "data": data})

@app.get("/api/stream")
async def stream_events(request: Request):
    queue = asyncio.Queue()
    event_queues.append(queue)
    
    async def event_generator():
        try:
            while True:
                if await request.is_disconnected():
                    break
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=15.0)
                    yield {
                        "event": event["type"],
                        "data": json.dumps(event["data"])
                    }
                except asyncio.TimeoutError:
                    yield {"event": "ping", "data": "keepalive"}
        finally:
            if queue in event_queues:
                event_queues.remove(queue)
                
    return EventSourceResponse(event_generator())

@app.get("/api/dashboard")
async def get_dashboard():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        
        # Simple aggregate queries
        async with db.execute("SELECT COUNT(*) FROM risk_events WHERE status='ACTIVE'") as c:
            active_risks = (await c.fetchone())[0]
            
        async with db.execute("SELECT COUNT(*) FROM risk_events WHERE status='ACTIVE' AND severity='CRITICAL'") as c:
            critical_risks = (await c.fetchone())[0]
            
        async with db.execute("SELECT COUNT(*) FROM workers") as c:
            total_workers = (await c.fetchone())[0]
            
        async with db.execute("SELECT COUNT(*) FROM work_permits WHERE status='ACTIVE'") as c:
            active_permits = (await c.fetchone())[0]
            
        async with db.execute("SELECT COUNT(*) FROM sensors") as c:
            sensors_online = (await c.fetchone())[0]
            
        return {
            "active_risks": active_risks,
            "critical_risks": critical_risks,
            "workers_on_site": total_workers,
            "workers_safe": total_workers - 15 if critical_risks > 0 else total_workers,
            "overall_crs": 0.89 if critical_risks > 0 else 0.12,
            "compliance_score": 87,
            "active_permits": active_permits,
            "sensors_online": sensors_online,
            "sensors_anomaly": 2 if critical_risks > 0 else 0,
            "last_updated": datetime.now(timezone.utc).isoformat()
        }

@app.get("/api/zones")
async def get_zones():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM zones") as c:
            zones = [dict(row) for row in await c.fetchall()]
        return {"zones": zones}

@app.get("/api/sensors")
async def get_sensors():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT s.*, z.name as zone_name FROM sensors s JOIN zones z ON s.zone_id = z.id") as c:
            sensors = [dict(row) for row in await c.fetchall()]
            
        # Add mock sparklines and readings
        for s in sensors:
            s["value"] = s["normal_range_low"] + (s["normal_range_high"] - s["normal_range_low"]) / 2
            s["sparkline"] = [s["value"] * (1 + 0.05 * i) for i in range(-5, 5)]
            s["normalized_risk"] = 0.1
            s["is_anomaly"] = False
            s["status"] = "ACTIVE"
            s["trend"] = "STABLE"
            
        return {"sensors": sensors}

@app.get("/api/permits")
async def get_permits():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT p.*, z.name as zone_name FROM work_permits p JOIN zones z ON p.zone_id = z.id WHERE p.status='ACTIVE'") as c:
            permits = [dict(row) for row in await c.fetchall()]
        return {"permits": permits}

@app.get("/api/workers")
async def get_workers():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM workers") as c:
            workers = [dict(row) for row in await c.fetchall()]
        return {"workers": workers}

# Basic demo endpoint to trigger the workflow
@app.post("/api/demo")
async def trigger_demo():
    await broadcast_event("demo_progress", {"status": "started", "message": "Demo initialized..."})
    
    # 1. Fetch current state from DB
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        
        async with db.execute("SELECT * FROM zones") as c:
            zones = [dict(row) for row in await c.fetchall()]
            
        async with db.execute("SELECT s.*, z.name as zone_name FROM sensors s JOIN zones z ON s.zone_id = z.id") as c:
            sensors = [dict(row) for row in await c.fetchall()]
            
        async with db.execute("SELECT * FROM work_permits WHERE status='ACTIVE'") as c:
            permits = [dict(row) for row in await c.fetchall()]
            
        async with db.execute("SELECT * FROM workers") as c:
            workers = [dict(row) for row in await c.fetchall()]
            
    # Modify one sensor to be anomalous for the demo (Zone 1 H2S sensor)
    for s in sensors:
        if s["id"] == "sensor-001":
            s["value"] = 7.5
            s["trend"] = "RISING"

    # Setup initial state
    initial_state = {
        "sensor_readings": sensors,
        "active_permits": permits,
        "workers": workers,
        "zones": zones,
        "equipment": [],
        "run_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "demo_mode": True,
        "errors": []
    }
    
    # Run the graph in background
    asyncio.create_task(run_graph_and_broadcast(initial_state))
    return {"status": "DEMO_STARTED"}

async def run_graph_and_broadcast(initial_state: dict):
    state = initial_state
    
    # Run through graph nodes sequentially manually to control SSE timing for demo
    await asyncio.sleep(2)
    state = await watcher_node(state)
    await broadcast_event("agent_status", {"agent": "WATCHER", "status": "COMPLETED", "summary": state["watcher_summary"]})
    
    await asyncio.sleep(2)
    state = await auditor_node(state)
    await broadcast_event("agent_status", {"agent": "AUDITOR", "status": "COMPLETED", "summary": state["auditor_summary"]})
    
    await asyncio.sleep(2)
    state = await analyst_node(state)
    await broadcast_event("agent_status", {"agent": "ANALYST", "status": "COMPLETED", "summary": state["analyst_summary"]})
    if state.get("risk_events"):
        await broadcast_event("risk_detected", state["risk_events"][0])
    
    if any(r["crs_score"] > 0.35 for r in state.get("risk_events", [])):
        await asyncio.sleep(2)
        state = await oracle_node(state)
        await broadcast_event("agent_status", {"agent": "ORACLE", "status": "COMPLETED", "summary": state["oracle_summary"]})
        
        await asyncio.sleep(2)
        state = await scribe_node(state)
        await broadcast_event("agent_status", {"agent": "SCRIBE", "status": "COMPLETED", "summary": "Reports generated."})
        
        if any(r["severity"] == "CRITICAL" for r in state.get("risk_events", [])):
            await asyncio.sleep(2)
            state = await guardian_node(state)
            await broadcast_event("agent_status", {"agent": "GUARDIAN", "status": "COMPLETED", "summary": state["guardian_summary"]})
            if state.get("emergency_actions"):
                await broadcast_event("emergency_action", state["emergency_actions"])
