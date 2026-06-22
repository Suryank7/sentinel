"use client";
import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

export default function PredictionChart({ prediction }) {
  if (!prediction) {
    return (
      <div className="card" style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <span className="text-muted">No active predictions</span>
      </div>
    );
  }

  const { incident_probability, intervention_window } = prediction;
  
  const data = [
    { time: 'Now', prob: incident_probability['1_hour'] ? incident_probability['1_hour'] * 100 : 0 },
    { time: '+1h', prob: incident_probability['1_hour'] ? incident_probability['1_hour'] * 100 : 0 },
    { time: '+4h', prob: incident_probability['4_hours'] ? incident_probability['4_hours'] * 100 : 0 },
    { time: '+12h', prob: incident_probability['12_hours'] ? incident_probability['12_hours'] * 100 : 0 },
    { time: '+24h', prob: incident_probability['24_hours'] ? incident_probability['24_hours'] * 100 : 0 },
  ];

  return (
    <div className="card" style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <h3 style={{ marginBottom: '16px' }}>ORACLE Forecast</h3>
      
      <div style={{ flex: 1, minHeight: '150px' }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 5, right: 5, left: -20, bottom: 5 }}>
            <XAxis dataKey="time" stroke="var(--text-muted)" fontSize={11} tickLine={false} axisLine={false} />
            <YAxis stroke="var(--text-muted)" fontSize={11} tickLine={false} axisLine={false} domain={[0, 100]} />
            <Tooltip 
              contentStyle={{ backgroundColor: 'var(--bg-elevated)', border: 'none', borderRadius: '8px' }}
              itemStyle={{ color: 'var(--critical)' }}
            />
            <ReferenceLine y={85} stroke="var(--critical)" strokeDasharray="3 3" label={{ position: 'top', value: 'Critical', fill: 'var(--critical)', fontSize: 10 }} />
            <Line type="monotone" dataKey="prob" stroke="var(--agent-oracle)" strokeWidth={3} dot={{ r: 4, fill: 'var(--agent-oracle)' }} activeDot={{ r: 6 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
      
      <div style={{ marginTop: '12px', padding: '12px', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid var(--border-critical)', borderRadius: '8px' }}>
        <div style={{ fontSize: '11px', color: 'var(--critical)', fontWeight: 'bold', marginBottom: '4px' }}>INTERVENTION WINDOW</div>
        <div style={{ fontSize: '12px', color: 'var(--text-primary)' }}>{intervention_window}</div>
      </div>
    </div>
  );
}
