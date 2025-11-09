import React from 'react';
import type { SimulationMetrics } from '../types';

interface SimulationControlsProps {
  onLoadSample: () => void;
  onSimulate: () => void;
  isLoading: boolean;
  hasData: boolean;
  isSimulated: boolean;
  metrics: SimulationMetrics | null;
}

export const SimulationControls: React.FC<SimulationControlsProps> = ({
  onLoadSample,
  onSimulate,
  isLoading,
  hasData,
  isSimulated,
  metrics,
}) => {
  return (
    <div className="space-y-4">
      <div className="space-y-2">
        <button
          onClick={onLoadSample}
          disabled={isLoading}
          className="w-full btn-primary text-sm"
        >
          {isLoading ? 'Loading...' : 'Load Sample Brain'}
        </button>

        <button
          onClick={onSimulate}
          disabled={isLoading || !hasData || isSimulated}
          className="w-full btn-secondary text-sm disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Simulating...' : 'Remove Tumor & Simulate'}
        </button>
      </div>

      {metrics && (
        <div className="border-t border-gray-200 pt-4 space-y-3">
          <h3 className="text-sm font-semibold text-gray-700">Simulation Metrics</h3>
          
          <div className="grid grid-cols-1 gap-2">
            <MetricCard
              label="Max Displacement"
              value={`${metrics.max_displacement_mm.toFixed(2)} mm`}
              color="text-blue-600"
            />
            <MetricCard
              label="Avg Stress"
              value={`${metrics.avg_stress_kpa.toFixed(1)} kPa`}
              color="text-orange-600"
            />
            <MetricCard
              label="Affected Volume"
              value={`${metrics.affected_volume_cm3.toFixed(2)} cm³`}
              color="text-purple-600"
            />
          </div>

          {metrics.vulnerable_regions.length > 0 && (
            <div className="mt-3">
              <h4 className="text-xs font-semibold text-gray-600 mb-2">Vulnerable Regions</h4>
              <ul className="space-y-1">
                {metrics.vulnerable_regions.map((region, idx) => (
                  <li key={idx} className="text-xs text-gray-700 bg-yellow-50 px-2 py-1 rounded">
                    {region}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

const MetricCard: React.FC<{ label: string; value: string; color: string }> = ({
  label,
  value,
  color,
}) => (
  <div className="bg-gray-50 rounded-lg px-3 py-2">
    <p className="text-xs text-gray-600">{label}</p>
    <p className={`text-sm font-semibold ${color}`}>{value}</p>
  </div>
);

