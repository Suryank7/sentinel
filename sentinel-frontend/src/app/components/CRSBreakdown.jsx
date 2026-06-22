"use client";
import React from 'react';

export default function CRSBreakdown({ riskEvent }) {
  if (!riskEvent) {
    return (
      <div className="card" style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <span className="text-muted">No active compound risks</span>
      </div>
    );
  }

  const { breakdown, crs_score, severity } = riskEvent;
  
  return (
    <div className="card" style={{ height: '100%' }}>
      <h3 style={{ marginBottom: '16px' }}>CRS Formula Breakdown</h3>
      
      <div className="flex justify-between items-center" style={{ marginBottom: '16px', padding: '12px', background: 'var(--bg-primary)', borderRadius: '8px' }}>
        <div>
          <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Final Score</div>
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: `var(--${severity.toLowerCase()})` }}>
            {crs_score.toFixed(3)}
          </div>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Severity</div>
          <div style={{ fontSize: '16px', fontWeight: 'bold', color: `var(--${severity.toLowerCase()})` }}>
            {severity}
          </div>
        </div>
      </div>
      
      <div style={{ display: 'grid', gap: '8px' }}>
        <div className="flex justify-between">
          <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Base Score (Sum of Risks)</span>
          <span style={{ fontSize: '13px', fontWeight: 'bold' }}>{breakdown.base_score.toFixed(3)}</span>
        </div>
        
        <div className="flex justify-between">
          <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Cascade Multiplier</span>
          <span style={{ fontSize: '13px', fontWeight: 'bold', color: breakdown.cascade_factor > 1 ? 'var(--critical)' : 'inherit' }}>
            x {breakdown.cascade_factor.toFixed(1)}
          </span>
        </div>
        {breakdown.cascade_reason && (
          <div style={{ fontSize: '11px', color: 'var(--critical)', textAlign: 'right', marginTop: '-4px' }}>
            {breakdown.cascade_reason}
          </div>
        )}
        
        <div className="flex justify-between">
          <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Regulatory Penalty</span>
          <span style={{ fontSize: '13px', fontWeight: 'bold', color: breakdown.regulatory_penalty > 0 ? 'var(--critical)' : 'inherit' }}>
            + {(breakdown.regulatory_penalty * 100).toFixed(0)}%
          </span>
        </div>
      </div>
      
      <div style={{ marginTop: '16px', paddingTop: '16px', borderTop: '1px solid var(--border-default)' }}>
        <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '8px' }}>Contributing Factors</div>
        {breakdown.individual_factors.map((f, i) => (
          <div key={i} className="flex justify-between items-center" style={{ marginBottom: '4px' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-primary)' }} title={f.name}>
              {f.name.length > 20 ? f.name.substring(0, 20) + '...' : f.name}
            </span>
            <div className="flex items-center gap-sm">
              <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>W:{f.weight}</span>
              <span style={{ fontSize: '12px', fontWeight: 'bold', color: 'var(--high)' }}>{f.contribution.toFixed(2)}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
