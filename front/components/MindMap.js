import React from 'react';

export default function MindMap({ data }) {
  return (
    <div>
      <h2>脑图展示</h2>
      <ul>
        {data.map((device, index) => (
          <li key={index}>
            <strong>{device.name}</strong>
            <ul>
              {device.metrics.map((metric, idx) => (
                <li key={idx}>{metric}</li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </div>
  );
} 