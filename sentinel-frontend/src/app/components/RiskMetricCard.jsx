"use client";

import React from 'react';
import { AlertTriangle, ShieldCheck, Activity, CheckCircle2 } from 'lucide-react';

export default function RiskMetricCard({ title, value, subtitle, severity, icon: IconName, isNew }) {
  const getSeverityColor = () => {
    switch(severity) {
      case 'CRITICAL': return 'var(--critical)';
      case 'HIGH': return 'var(--high)';
      case 'MEDIUM': return 'var(--medium)';
      case 'LOW': return 'var(--low)';
      case 'NORMAL': return 'var(--normal)';
      default: return 'var(--text-primary)';
    }
  };

  const getSeverityBg = () => {
    switch(severity) {
      case 'CRITICAL': return 'var(--critical-glow)';
      case 'HIGH': return 'var(--high-glow)';
      case 'MEDIUM': return 'var(--medium-glow)';
      case 'LOW': return 'var(--low-glow)';
      case 'NORMAL': return 'var(--normal-glow)';
      default: return 'var(--bg-surface)';
    }
  };

  const isCritical = severity === 'CRITICAL';

  return (
    <div 
      className="card flex-col"
      style={{
        borderLeft: `4px solid ${getSeverityColor()}`,
        animation: isCritical ? 'criticalPulse 2s infinite' : 'none'
      }}
    >
      <div className="flex justify-between items-center" style={{ marginBottom: '8px' }}>
        <span className="text-secondary" style={{ fontSize: '14px', fontWeight: 600 }}>{title}</span>
        {IconName === 'alert' && <AlertTriangle size={20} color={getSeverityColor()} />}
        {IconName === 'shield' && <ShieldCheck size={20} color={getSeverityColor()} />}
        {IconName === 'activity' && <Activity size={20} color={getSeverityColor()} />}
        {IconName === 'check' && <CheckCircle2 size={20} color={getSeverityColor()} />}
      </div>
      
      <div className="flex items-center gap-sm">
        <span style={{ fontSize: '32px', fontWeight: 700, color: getSeverityColor() }}>
          {value}
        </span>
        {severity && (
          <span style={{
            backgroundColor: getSeverityBg(),
            color: getSeverityColor(),
            padding: '2px 8px',
            borderRadius: '12px',
            fontSize: '12px',
            fontWeight: 'bold'
          }}>
            {severity}
          </span>
        )}
      </div>

      <div className="flex justify-between items-center" style={{ marginTop: '8px' }}>
        <span className="text-muted" style={{ fontSize: '12px' }}>{subtitle}</span>
        {isNew && (
          <span style={{ color: 'var(--critical)', fontSize: '12px', fontWeight: 'bold' }}>
            +1 new
          </span>
        )}
      </div>
    </div>
  );
}
