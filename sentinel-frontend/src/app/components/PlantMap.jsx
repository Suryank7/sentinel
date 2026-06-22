"use client";
import React from 'react';

export default function PlantMap({ zones, workers, permits, crsScore }) {
  // Simple hackathon plant map layout rendering SVG
  
  const getSeverityColor = (severity) => {
    switch(severity) {
      case 'CRITICAL': return 'var(--critical)';
      case 'HIGH': return 'var(--high)';
      case 'MEDIUM': return 'var(--medium)';
      case 'LOW': return 'var(--low)';
      case 'NORMAL': return 'var(--normal)';
      default: return '#1a3a2a'; // Default normal green
    }
  };

  return (
    <div className="card" style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <h3 style={{ marginBottom: '16px', display: 'flex', justifyContent: 'space-between' }}>
        <span>Geospatial Plant Heatmap</span>
        <span style={{ fontSize: '12px', background: 'var(--bg-elevated)', padding: '4px 8px', borderRadius: '4px' }}>
          Workers: {workers.length} | Active Permits: {permits.length}
        </span>
      </h3>
      
      <div style={{ flex: 1, backgroundColor: 'var(--bg-secondary)', borderRadius: '8px', overflow: 'hidden', position: 'relative' }}>
        <svg viewBox="0 0 100 80" style={{ width: '100%', height: '100%' }}>
          {/* Render Zones */}
          {zones.map((zone) => {
            const isCritical = zone.severity === 'CRITICAL';
            return (
              <g key={zone.id}>
                <rect 
                  x={zone.position?.x || zone.x_position} 
                  y={zone.position?.y || zone.y_position} 
                  width={zone.position?.width || zone.width} 
                  height={zone.position?.height || zone.height} 
                  fill={zone.fill_color || getSeverityColor(zone.severity)}
                  stroke={isCritical ? '#ff6b6b' : 'rgba(255,255,255,0.2)'}
                  strokeWidth="0.5"
                  rx="1"
                  style={{ 
                    transition: 'fill 1s ease',
                    animation: isCritical ? 'criticalPulse 2s infinite' : 'none'
                  }}
                />
                <text 
                  x={(zone.position?.x || zone.x_position) + 2} 
                  y={(zone.position?.y || zone.y_position) + 5} 
                  fill="white" 
                  fontSize="3" 
                  fontWeight="bold"
                >
                  {zone.code}
                </text>
              </g>
            );
          })}

          {/* Render Workers */}
          {workers.map((worker) => (
            <circle 
              key={worker.id}
              cx={worker.x_position}
              cy={worker.y_position}
              r="0.8"
              fill={worker.status === 'EVACUATING' ? 'var(--critical)' : (worker.status === 'SAFE' ? 'var(--normal)' : 'var(--accent-primary)')}
              style={{
                transition: 'all 1s ease',
                animation: worker.status === 'EVACUATING' ? 'workerDotPulse 1s infinite' : 'none'
              }}
            >
              <title>{worker.name} - {worker.role}</title>
            </circle>
          ))}
          
          {/* Render Permits */}
          {permits.map((permit, i) => {
            const zone = zones.find(z => z.id === permit.zone_id);
            if (!zone) return null;
            const px = (zone.position?.x || zone.x_position) + (zone.position?.width || zone.width) - 4;
            const py = (zone.position?.y || zone.y_position) + 4 + (i * 3);
            return (
              <text key={permit.id} x={px} y={py} fontSize="3" fill={permit.status === 'SUSPENDED' ? 'var(--critical)' : 'var(--medium)'}>
                {permit.type === 'HOT_WORK' ? '🔥' : '⚠️'}
              </text>
            );
          })}
        </svg>
      </div>
      
      <div className="flex gap-md" style={{ marginTop: '12px', fontSize: '12px', justifyContent: 'center' }}>
        <span className="flex items-center gap-xs"><span style={{width: 8, height: 8, background: 'var(--normal)', display: 'inline-block', borderRadius: '50%'}}></span> Safe</span>
        <span className="flex items-center gap-xs"><span style={{width: 8, height: 8, background: 'var(--medium)', display: 'inline-block', borderRadius: '50%'}}></span> Med</span>
        <span className="flex items-center gap-xs"><span style={{width: 8, height: 8, background: 'var(--high)', display: 'inline-block', borderRadius: '50%'}}></span> High</span>
        <span className="flex items-center gap-xs"><span style={{width: 8, height: 8, background: 'var(--critical)', display: 'inline-block', borderRadius: '50%'}}></span> Critical</span>
      </div>
    </div>
  );
}
