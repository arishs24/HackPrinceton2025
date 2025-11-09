"""
Router for STL file management
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import STLListResponse, STLFileInfo
from typing import List
import os
import glob

router = APIRouter()

STL_BASE_DIR = "stl"
os.makedirs(STL_BASE_DIR, exist_ok=True)


@router.get("/stl/{case_id}", response_model=STLListResponse)
async def list_stl_files(case_id: str):
    """
    List all STL files for a given case ID.
    """
    case_stl_dir = os.path.join(STL_BASE_DIR, case_id)
    
    if not os.path.exists(case_stl_dir):
        return STLListResponse(
            case_id=case_id,
            stl_files=[],
            status="no_stl_files_found"
        )
    
    # Find all STL files
    stl_files = glob.glob(os.path.join(case_stl_dir, "*.stl"))
    
    stl_info_list = []
    for stl_path in stl_files:
        filename = os.path.basename(stl_path)
        # Extract region name from filename (remove .stl and label suffix if present)
        name = filename.replace(".stl", "")
        # Remove trailing _number pattern if present
        if "_" in name and name.split("_")[-1].isdigit():
            parts = name.rsplit("_", 1)
            if parts[1].isdigit():
                name = parts[0]
                label = int(parts[1])
            else:
                label = 0
        else:
            label = 0
        
        # Replace underscores with spaces for display
        display_name = name.replace("_", " ")
        
        stl_info_list.append(STLFileInfo(
            filename=filename,
            name=display_name,
            label=label,
            voxels=0  # We don't store voxel count in STL files
        ))
    
    return STLListResponse(
        case_id=case_id,
        stl_files=stl_info_list,
        status="ready" if stl_info_list else "processing"
    )


@router.get("/stl/{case_id}/{filename}")
async def get_stl_file(case_id: str, filename: str):
    """
    Serve STL file for download/viewing.
    """
    case_stl_dir = os.path.join(STL_BASE_DIR, case_id)
    stl_path = os.path.join(case_stl_dir, filename)
    
    if not os.path.exists(stl_path):
        raise HTTPException(status_code=404, detail="STL file not found")
    
    from fastapi.responses import FileResponse
    return FileResponse(
        stl_path,
        media_type="application/octet-stream",
        filename=filename
    )

