"use client";

import React, { useState, useEffect } from 'react';
import RiskMetricCard from './components/RiskMetricCard';
import PlantMap from './components/PlantMap';
import AgentTimeline from './components/AgentTimeline';
import CRSBreakdown from './components/CRSBreakdown';
import PredictionChart from './components/PredictionChart';
import EmergencyPanel from './components/EmergencyPanel';
import { Shield, PlayCircle } from 'lucide-react';

// Make sure backend uses correct port
const API_BASE = 'http://localhost:8000/api';

export default function Dashboard() {
  const [metrics, setMetrics] = useState({
    active_risks: 0, critical_risks: 0, workers_safe: 0, workers_on_site: 0, overall_crs: 0.1
  });
  const [zones, setZones] = useState([]);
  const [sensors, setSensors] = useState([]);
  const [workers, setWorkers] = useState([]);
  const [permits, setPermits] = useState([]);
  
  const [agents, setAgents] = useState([]);
  const [activeRiskEvent, setActiveRiskEvent] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [emergencyActions, setEmergencyActions] = useState([]);
  
  const [demoRunning, setDemoRunning] = useState(false);

  // Initial data fetch
  useEffect(() => {
    const fetchInitial = async () => {
      try {
        const [mRes, zRes, sRes, wRes, pRes] = await Promise.all([
          fetch(`${API_BASE}/dashboard`),
          fetch(`${API_BASE}/zones`),
          fetch(`${API_BASE}/sensors`),
          fetch(`${API_BASE}/workers`),
          fetch(`${API_BASE}/permits`)
        ]);
        
        if (mRes.ok) setMetrics(await mRes.json());
        if (zRes.ok) setZones((await zRes.json()).zones);
        if (sRes.ok) setSensors((await sRes.json()).sensors);
        if (wRes.ok) setWorkers((await wRes.json()).workers);
        if (pRes.ok) setPermits((await pRes.json()).permits);
      } catch (e) {
        console.error("Failed to fetch initial data", e);
      }
    };
    fetchInitial();
  }, []);

  // SSE Subscription
  useEffect(() => {
    const eventSource = new EventSource(`${API_BASE}/stream`);
    
    eventSource.addEventListener('demo_progress', (e) => {
      setDemoRunning(true);
      setAgents([]);
      setActiveRiskEvent(null);
      setPrediction(null);
      setEmergencyActions([]);
    });
    
    eventSource.addEventListener('agent_status', (e) => {
      const data = JSON.parse(e.data);
      data.time = new Date().toLocaleTimeString();
      setAgents(prev => [...prev, data]);
    });
    
    eventSource.addEventListener('risk_detected', (e) => {
      const data = JSON.parse(e.data);
      setActiveRiskEvent(data);
      // Update map colors based on risk
      setZones(prev => prev.map(z => 
        data.zones_affected.includes(z.id) ? { ...z, severity: data.severity } : z
      ));
      setMetrics(prev => ({
        ...prev, 
        active_risks: prev.active_risks + 1,
        critical_risks: data.severity === 'CRITICAL' ? prev.critical_risks + 1 : prev.critical_risks,
        overall_crs: data.crs_score
      }));
    });
    
    eventSource.addEventListener('emergency_action', (e) => {
      const data = JSON.parse(e.data);
      setEmergencyActions(data);
      
      // Update worker status for evacuation
      const evactions = data.filter(a => a.type === 'EVACUATE_ZONE');
      if (evactions.length > 0) {
        setWorkers(prev => prev.map(w => ({ ...w, status: 'EVACUATING' })));
      }
    });

    return () => eventSource.close();
  }, []);

  const triggerDemo = async () => {
    setDemoRunning(true);
    try {
      await fetch(`${API_BASE}/demo`, { method: 'POST' });
    } catch (e) {
      console.error(e);
      setDemoRunning(false);
    }
  };

  return (
    <div style={{ padding: 'var(--space-md)', minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <header className="flex justify-between items-center" style={{ marginBottom: 'var(--space-md)' }}>
        <div className="flex items-center gap-sm">
          <Shield size={32} color="var(--accent-primary)" />
          <div>
            <h1 style={{ fontSize: '24px', letterSpacing: '1px' }}>SENTINEL</h1>
            <p className="text-muted" style={{ fontSize: '12px' }}>AI-Powered Safety Command Centre</p>
          </div>
        </div>
        
        <button 
          onClick={triggerDemo}
          disabled={demoRunning}
          style={{
            padding: '10px 20px',
            background: demoRunning ? 'var(--bg-elevated)' : 'var(--gradient-hero)',
            color: 'white',
            border: 'none',
            borderRadius: 'var(--radius-md)',
            fontWeight: 'bold',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            cursor: demoRunning ? 'not-allowed' : 'pointer',
            boxShadow: demoRunning ? 'none' : '0 4px 15px rgba(239, 68, 68, 0.4)'
          }}
        >
          <PlayCircle size={20} />
          {demoRunning ? 'SIMULATION RUNNING' : 'INITIATE CRS SIMULATION'}
        </button>
      </header>

      {/* KPI Row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 'var(--space-md)', marginBottom: 'var(--space-md)' }}>
        <RiskMetricCard 
          title="Compound Risk Score" 
          value={metrics.overall_crs.toFixed(2)} 
          subtitle="Plant-wide risk index" 
          severity={metrics.overall_crs > 0.85 ? 'CRITICAL' : (metrics.overall_crs > 0.35 ? 'MEDIUM' : 'NORMAL')} 
          icon="activity" 
        />
        <RiskMetricCard 
          title="Active Risk Events" 
          value={metrics.active_risks} 
          subtitle={`${metrics.critical_risks} critical risks`} 
          severity={metrics.critical_risks > 0 ? 'CRITICAL' : 'NORMAL'} 
          icon="alert" 
          isNew={demoRunning && metrics.active_risks > 0}
        />
        <RiskMetricCard 
          title="Workers Safe" 
          value={`${metrics.workers_safe}/${metrics.workers_on_site}`} 
          subtitle="Real-time personnel tracking" 
          severity={metrics.workers_safe < metrics.workers_on_site ? 'CRITICAL' : 'NORMAL'} 
          icon="shield" 
        />
        <RiskMetricCard 
          title="Compliance Health" 
          value={`${metrics.compliance_score || 100}%`} 
          subtitle="Regulatory adherence" 
          severity={metrics.compliance_score < 90 ? 'MEDIUM' : 'NORMAL'} 
          icon="check" 
        />
      </div>

      {/* Main Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr 300px', gap: 'var(--space-md)', flex: 1 }}>
        
        {/* Left Column - Pipeline */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-md)' }}>
          <div style={{ flex: 1 }}>
            <AgentTimeline agents={agents} />
          </div>
        </div>
        
        {/* Center Column - Map & Breakdown */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-md)' }}>
          <div style={{ flex: 2 }}>
            <PlantMap zones={zones} workers={workers} permits={permits} crsScore={metrics.overall_crs} />
          </div>
          <div style={{ flex: 1 }}>
            <CRSBreakdown riskEvent={activeRiskEvent} />
          </div>
        </div>
        
        {/* Right Column - Prediction & Action */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-md)' }}>
          <div style={{ flex: 1 }}>
            <PredictionChart prediction={prediction || (activeRiskEvent?.crs_score > 0.35 ? {
                incident_probability: {'1_hour': 0.85, '4_hours': 0.95, '12_hours': 0.99, '24_hours': 0.99},
                intervention_window: 'Immediate action required. Escalate to site command.'
            } : null)} />
          </div>
          <div style={{ flex: 1.5 }}>
            <EmergencyPanel actions={emergencyActions} />
          </div>
        </div>
        
      </div>
    </div>
  );
}
