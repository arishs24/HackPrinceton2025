from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime


class UploadResponse(BaseModel):
    case_id: str
    filename: str
    status: str


class MeshData(BaseModel):
    vertices: List[List[float]]
    faces: List[List[int]]
    labels: Optional[List[int]] = None
    colors: Optional[List[List[float]]] = None


class SegmentationResponse(BaseModel):
    mesh_data: MeshData
    label_names: Dict[str, str]
    case_id: str


class SimulationRequest(BaseModel):
    case_id: str
    remove_region: str = "tumor"
    skull_opening_size: float = 5.0


class SimulationMetrics(BaseModel):
    max_displacement_mm: float
    avg_stress_kpa: float
    affected_volume_cm3: float
    vulnerable_regions: List[str]


class SimulationResponse(BaseModel):
    deformed_mesh: MeshData
    metrics: SimulationMetrics
    heatmap_data: List[float]
    case_id: str


class GeminiRequest(BaseModel):
    simulation_results: Dict[str, Any]
    query: Optional[str] = None
    conversation_id: Optional[str] = None


class GeminiResponse(BaseModel):
    technical_summary: str
    patient_summary: str
    conversation_id: str


class SnowflakeSimulationData(BaseModel):
    case_id: str
    timestamp: datetime
    tumor_location: str
    tumor_volume: float
    max_displacement: float
    avg_stress: float
    affected_regions: List[str]
    simulation_json: Dict[str, Any]


class STLFileInfo(BaseModel):
    filename: str
    name: str
    label: int
    voxels: int


class STLListResponse(BaseModel):
    case_id: str
    stl_files: List[STLFileInfo]
    status: str