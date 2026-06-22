"use client";
import React from 'react';
import { Bot, CheckCircle2, CircleDashed } from 'lucide-react';

export default function AgentTimeline({ agents }) {
  // agents: [{ name: 'WATCHER', status: 'COMPLETED', summary: '...', time: '10:00:00' }, ...]
  
  const getAgentColor = (name) => {
    switch(name) {
      case 'WATCHER': return 'var(--agent-watcher)';
      case 'AUDITOR': return 'var(--agent-auditor)';
      case 'ANALYST': return 'var(--agent-analyst)';
      case 'ORACLE': return 'var(--agent-oracle)';
      case 'SCRIBE': return 'var(--agent-scribe)';
      case 'GUARDIAN': return 'var(--agent-guardian)';
      default: return 'var(--text-secondary)';
    }
  };

  return (
    <div className="card" style={{ height: '100%', overflowY: 'auto' }}>
      <h3 style={{ marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <Bot size={20} /> LangGraph Agent Pipeline
      </h3>
      
      <div style={{ position: 'relative', paddingLeft: '24px' }}>
        {/* Timeline Line */}
        <div style={{
          position: 'absolute', top: 0, bottom: 0, left: '11px', 
          width: '2px', background: 'var(--border-default)'
        }} />
        
        {agents.map((agent, index) => {
          const isComplete = agent.status === 'COMPLETED';
          const isRunning = agent.status === 'RUNNING';
          const color = getAgentColor(agent.name);
          
          return (
            <div key={index} style={{ marginBottom: '20px', position: 'relative' }}>
              <div style={{
                position: 'absolute', left: '-24px', top: '2px',
                background: 'var(--bg-primary)', borderRadius: '50%'
              }}>
                {isComplete ? (
                  <CheckCircle2 size={24} color={color} />
                ) : (
                  <CircleDashed size={24} color={isRunning ? color : 'var(--text-muted)'} 
                    style={{ animation: isRunning ? 'spin 2s linear infinite' : 'none' }} 
                  />
                )}
              </div>
              
              <div style={{ marginLeft: '12px' }}>
                <div className="flex justify-between items-center">
                  <span style={{ fontWeight: 'bold', color: isComplete || isRunning ? color : 'var(--text-muted)' }}>
                    {agent.name}
                  </span>
                  <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{agent.time}</span>
                </div>
                {agent.summary && (
                  <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '4px' }}>
                    {agent.summary}
                  </p>
                )}
              </div>
            </div>
          );
        })}
        {agents.length === 0 && (
          <p className="text-muted" style={{ fontSize: '13px' }}>Waiting for pipeline execution...</p>
        )}
      </div>
      <style dangerouslySetInnerHTML={{__html: `
        @keyframes spin { 100% { transform: rotate(360deg); } }
      `}} />
    </div>
  );
}
