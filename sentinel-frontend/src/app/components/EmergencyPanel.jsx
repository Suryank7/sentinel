"use client";
import React from 'react';
import { AlertOctagon, CheckCircle } from 'lucide-react';

export default function EmergencyPanel({ actions }) {
  if (!actions || actions.length === 0) {
    return (
      <div className="card" style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <span className="text-muted">No emergency actions</span>
      </div>
    );
  }

  return (
    <div className="card" style={{ height: '100%', border: '1px solid var(--border-critical)', boxShadow: 'var(--shadow-critical)' }}>
      <h3 style={{ marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--critical)' }}>
        <AlertOctagon size={20} /> GUARDIAN Emergency Protocols
      </h3>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {actions.map((action, i) => (
          <div key={i} style={{ 
            padding: '12px', 
            background: action.status === 'EXECUTING' || action.status === 'COMPLETED' ? 'var(--bg-elevated)' : 'var(--bg-primary)', 
            borderRadius: '8px',
            borderLeft: `4px solid ${action.status === 'EXECUTING' ? 'var(--critical)' : (action.status === 'COMPLETED' ? 'var(--normal)' : 'var(--medium)')}`
          }}>
            <div className="flex justify-between items-center" style={{ marginBottom: '4px' }}>
              <span style={{ fontSize: '14px', fontWeight: 'bold' }}>{action.type}</span>
              <span style={{ 
                fontSize: '10px', 
                padding: '2px 6px', 
                borderRadius: '4px',
                background: action.status === 'COMPLETED' ? 'rgba(34, 197, 94, 0.2)' : 'rgba(239, 68, 68, 0.2)',
                color: action.status === 'COMPLETED' ? 'var(--normal)' : 'var(--critical)'
              }}>
                {action.status}
              </span>
            </div>
            <div style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>{action.description}</div>
            
            {action.status === 'PROPOSED' && action.requires_confirmation && (
              <div style={{ marginTop: '12px', display: 'flex', gap: '8px' }}>
                <button style={{ 
                  flex: 1, padding: '6px', background: 'var(--critical)', color: 'white', 
                  border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '12px', fontWeight: 'bold'
                }}>
                  AUTHORIZE
                </button>
                <button style={{ 
                  flex: 1, padding: '6px', background: 'transparent', color: 'var(--text-primary)', 
                  border: '1px solid var(--border-default)', borderRadius: '4px', cursor: 'pointer', fontSize: '12px'
                }}>
                  REJECT
                </button>
              </div>
            )}
            
            {action.status === 'COMPLETED' && (
              <div style={{ marginTop: '8px', fontSize: '11px', color: 'var(--normal)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                <CheckCircle size={12} /> Executed at {new Date(action.executed_at).toLocaleTimeString()}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
