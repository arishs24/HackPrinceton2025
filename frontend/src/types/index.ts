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

export interface STLFileInfo {
  filename: string;
  name: string;
  label: number;
  voxels: number;
}

export interface STLListResponse {
  case_id: string;
  stl_files: STLFileInfo[];
  status: string;
}

export interface StructureFEARequest {
  case_id: string;
  structure_name: string;
  structure_label: number;
  stl_filename: string;
  coordinates?: { x: number; y: number; z: number };
  volume_to_remove?: string;
  patient_age?: number;
  procedure_type?: string;
  reason?: string;
}

export interface FEAResponse {
  fea_results: {
    structure_name: string;
    structure_label: number;
    max_stress_kpa: number;
    affected_regions: string[];
    stress_distribution: {
      high_stress: string[];
      moderate_stress: string[];
      low_stress: string[];
    };
  };
  removalSummary: any;
  neurologicalDeficits: any;
  functionalImpact: any;
  surgicalApproach: any;
  risks: any[];
  recoveryPrognosis: any;
  recommendations: string[];
}

