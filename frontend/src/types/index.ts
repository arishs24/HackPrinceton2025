// Type definitions matching backend schemas

export interface UploadResponse {
  case_id: string;
  filename: string;
  status: string;
}

export interface MeshData {
  vertices: number[][];
  faces: number[][];
  labels?: number[];
  colors?: number[][];
}

export interface SegmentationResponse {
  mesh_data: MeshData;
  label_names: Record<string, string>;
  case_id: string;
}

export interface SimulationRequest {
  case_id: string;
  remove_region?: string;
  skull_opening_size?: number;
}

export interface SimulationMetrics {
  max_displacement_mm: number;
  avg_stress_kpa: number;
  affected_volume_cm3: number;
  vulnerable_regions: string[];
}

export interface SimulationResponse {
  deformed_mesh: MeshData;
  metrics: SimulationMetrics;
  heatmap_data: number[];
  case_id: string;
}

export interface GeminiResponse {
  technical_summary: string;
  patient_summary: string;
  conversation_id: string;
}

