import axios from 'axios';
import type {
  UploadResponse,
  SegmentationResponse,
  SimulationResponse,
  GeminiResponse,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Upload scan file(s) - supports single file or multiple DICOM slices
export const uploadScan = async (files: File | File[]): Promise<UploadResponse> => {
  const formData = new FormData();

  // Handle both single file and multiple files
  const fileArray = Array.isArray(files) ? files : [files];

  // Append all files to form data
  fileArray.forEach(file => {
    formData.append('files', file);
  });

  const response = await api.post<UploadResponse>('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

// Segment brain structures
export const segmentBrain = async (caseId: string): Promise<SegmentationResponse> => {
  const response = await api.post<SegmentationResponse>('/segment', {
    case_id: caseId,
  });

  return response.data;
};

// Run simulation
export const runSimulation = async (
  caseId: string,
  removeRegion: string = 'tumor',
  skullOpeningSize: number = 5.0
): Promise<SimulationResponse> => {
  const response = await api.post<SimulationResponse>('/simulate', {
    case_id: caseId,
    remove_region: removeRegion,
    skull_opening_size: skullOpeningSize,
  });

  return response.data;
};

// Get Gemini insights
export const getGeminiInsights = async (
  simulationResults: any,
  query?: string,
  conversationId?: string
): Promise<GeminiResponse> => {
  const response = await api.post<GeminiResponse>('/gemini/analyze', {
    simulation_results: simulationResults,
    query,
    conversation_id: conversationId,
  });

  return response.data;
};

// Save to Snowflake
export const saveToSnowflake = async (data: any): Promise<any> => {
  const response = await api.post('/snowflake/save', data);
  return response.data;
};

// Get similar cases
export const getSimilarCases = async (tumorLocation: string, limit: number = 5): Promise<any> => {
  const response = await api.get(`/snowflake/similar/${tumorLocation}`, {
    params: { limit },
  });
  return response.data;
};

// Load sample data (triggers segmentation with mock case)
export const loadSampleData = async (): Promise<SegmentationResponse> => {
  return segmentBrain('sample-case-001');
};

