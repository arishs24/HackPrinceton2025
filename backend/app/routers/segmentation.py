from fastapi import APIRouter, HTTPException
from app.models.schemas import SegmentationResponse, MeshData
from app.services.segmentation_engine import process_dicom_to_mesh
from pydantic import BaseModel

router = APIRouter()


class SegmentRequest(BaseModel):
    case_id: str


@router.post("/segment", response_model=SegmentationResponse)
async def segment_brain(request: SegmentRequest):
    """
    Perform AI-powered segmentation of brain structures
    Processes uploaded DICOM slices or single volume files
    Uses marching cubes algorithm to generate 3D mesh from medical imaging data
    """
    case_id = request.case_id

    # Process DICOM files and generate 3D mesh
    # If case has DICOM files, performs actual 3D reconstruction from 2D slices
    # Falls back to mock data if no DICOM files are found
    mesh_data = process_dicom_to_mesh(case_id)

    label_names = {
        "0": "skull",
        "1": "white_matter",
        "2": "grey_matter",
        "3": "tumor"
    }

    return SegmentationResponse(
        mesh_data=mesh_data,
        label_names=label_names,
        case_id=case_id
    )
