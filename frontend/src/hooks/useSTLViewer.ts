import { useState, useEffect, useCallback } from 'react';
import { listSTLFiles, runFEA } from '../utils/api';
import type { STLFileInfo, FEAResponse } from '../types';

export const useSTLViewer = (caseId: string | null) => {
  const [stlFiles, setStlFiles] = useState<STLFileInfo[]>([]);
  const [selectedStructure, setSelectedStructure] = useState<STLFileInfo | null>(null);
  const [selectedCoordinates, setSelectedCoordinates] = useState<{ x: number; y: number; z: number } | undefined>(undefined);
  const [feaResults, setFeaResults] = useState<FEAResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingFEA, setIsLoadingFEA] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [polling, setPolling] = useState(false);

  // Poll for STL files if caseId exists
  useEffect(() => {
    if (!caseId) {
      setStlFiles([]);
      setSelectedStructure(null);
      setFeaResults(null);
      setPolling(false);
      return;
    }

    let interval: NodeJS.Timeout | null = null;
    let isMounted = true;

    const fetchSTLFiles = async () => {
      try {
        const response = await listSTLFiles(caseId);
        if (!isMounted) return;
        
        // Simulate "segmenting" delay - poll a few times before showing files
        const pollCount = (window as any).__stlPollCount || 0;
        (window as any).__stlPollCount = pollCount + 1;
        
        // After 2 polls (6 seconds), show all files
        if (pollCount >= 2) {
          // Show all files we got from the API
          setStlFiles(response.stl_files);
          setPolling(false);
          if (interval) {
            clearInterval(interval);
            interval = null;
          }
          (window as any).__stlPollCount = 0;
          console.log(`Loaded ${response.stl_files.length} STL files`);
        } else {
          // Keep showing "segmenting" and polling
          setStlFiles([]);
          setPolling(true);
          if (!interval) {
            interval = setInterval(fetchSTLFiles, 3000);
          }
        }
      } catch (err: any) {
        if (!isMounted) return;
        console.error('Error fetching STL files:', err);
        setError(err.message || 'Failed to load STL files');
        setPolling(false);
        if (interval) {
          clearInterval(interval);
          interval = null;
        }
      }
    };

    fetchSTLFiles();

    return () => {
      isMounted = false;
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [caseId]);

  const [feaParams, setFeaParams] = useState<{
    coordinates?: { x: number; y: number; z: number };
    volume_to_remove?: string;
    patient_age?: number;
    procedure_type?: string;
    reason?: string;
  }>({
    volume_to_remove: 'variable',
    patient_age: 45,
    procedure_type: 'tumor resection',
    reason: 'low-grade glioma',
  });

  const runFEASimulationInternal = useCallback(async (
    structure: STLFileInfo,
    coordinates?: { x: number; y: number; z: number },
    params?: typeof feaParams
  ) => {
    if (!caseId) return;

    setIsLoadingFEA(true);
    setError(null);

    try {
      const currentParams = params || feaParams;
      const results = await runFEA(
        caseId,
        structure.name,
        structure.label,
        structure.filename,
        {
          ...currentParams,
          coordinates: coordinates || currentParams.coordinates,
        }
      );
      setFeaResults(results);
    } catch (err: any) {
      setError(err.message || 'Failed to run FEA simulation');
    } finally {
      setIsLoadingFEA(false);
    }
  }, [caseId, feaParams]);

  const selectStructure = useCallback((structure: STLFileInfo, coordinates?: { x: number; y: number; z: number }) => {
    setSelectedStructure(structure);
    setSelectedCoordinates(coordinates);
    setFeaResults(null); // Clear previous FEA results
    
    // Update coordinates if provided
    let updatedParams = feaParams;
    if (coordinates) {
      updatedParams = { ...feaParams, coordinates };
      setFeaParams(updatedParams);
    }
    
    // Automatically run FEA when structure is selected
    if (caseId) {
      runFEASimulationInternal(structure, coordinates, updatedParams);
    }
  }, [caseId, feaParams, runFEASimulationInternal]);

  const runFEASimulation = useCallback(async () => {
    if (!selectedStructure || !caseId) {
      setError('Please select a structure first');
      return;
    }
    await runFEASimulationInternal(selectedStructure);
  }, [selectedStructure, caseId, runFEASimulationInternal]);

  const updateFEAParams = useCallback((params: Partial<typeof feaParams>) => {
    setFeaParams(prev => ({ ...prev, ...params }));
  }, []);

  return {
    stlFiles,
    selectedStructure,
    selectedCoordinates,
    feaResults,
    isLoading,
    isLoadingFEA,
    error,
    selectStructure,
    runFEASimulation,
    feaParams,
    updateFEAParams,
    isPolling: polling,
  };
};

