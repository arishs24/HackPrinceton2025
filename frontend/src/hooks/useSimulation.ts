import { useState, useCallback } from 'react';
import { loadSampleData, segmentBrain, runSimulation } from '../utils/api';
import type { MeshData, SimulationMetrics } from '../types';

export const useSimulation = () => {
  const [originalMesh, setOriginalMesh] = useState<MeshData | null>(null);
  const [deformedMesh, setDeformedMesh] = useState<MeshData | null>(null);
  const [metrics, setMetrics] = useState<SimulationMetrics | null>(null);
  const [heatmapData, setHeatmapData] = useState<number[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isSimulated, setIsSimulated] = useState(false);
  const [caseId, setCaseId] = useState<string | null>(null);

  const loadSample = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await loadSampleData();
      setOriginalMesh(response.mesh_data);
      setCaseId(response.case_id);
      setIsSimulated(false);
      setDeformedMesh(null);
      setMetrics(null);
      setHeatmapData([]);
    } catch (err: any) {
      setError(err.message || 'Failed to load sample data');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const segment = useCallback(async (uploadedCaseId: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await segmentBrain(uploadedCaseId);
      setOriginalMesh(response.mesh_data);
      setCaseId(response.case_id);
      setIsSimulated(false);
      setDeformedMesh(null);
      setMetrics(null);
      setHeatmapData([]);
    } catch (err: any) {
      setError(err.message || 'Failed to segment brain');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const simulate = useCallback(async () => {
    if (!caseId) {
      setError('No case loaded. Please load a sample or upload a scan first.');
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      const response = await runSimulation(caseId, 'tumor', 5.0);
      setDeformedMesh(response.deformed_mesh);
      setMetrics(response.metrics);
      setHeatmapData(response.heatmap_data);
      setIsSimulated(true);
    } catch (err: any) {
      setError(err.message || 'Failed to run simulation');
    } finally {
      setIsLoading(false);
    }
  }, [caseId]);

  const reset = useCallback(() => {
    setOriginalMesh(null);
    setDeformedMesh(null);
    setMetrics(null);
    setHeatmapData([]);
    setIsSimulated(false);
    setCaseId(null);
    setError(null);
  }, []);

  return {
    originalMesh,
    deformedMesh,
    metrics,
    heatmapData,
    isLoading,
    error,
    isSimulated,
    loadSample,
    segment,
    simulate,
    reset,
  };
};

