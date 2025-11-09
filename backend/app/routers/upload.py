from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.models.schemas import UploadResponse
from app.services.nifti_to_stl import process_nifti_to_stl_files
from typing import List
import uuid
import os
import aiofiles
import asyncio

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=UploadResponse)
async def upload_scan(files: List[UploadFile] = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    """
    Upload brain scan file(s) - supports single file or multiple DICOM slices
    For DICOM: Upload multiple .dcm files representing 2D slices
    For NIfTI: Upload single .nii or .nii.gz file containing 3D volume
    """
    # Generate unique case ID for this upload session
    case_id = str(uuid.uuid4())

    # Create case-specific directory
    case_dir = os.path.join(UPLOAD_DIR, case_id)
    os.makedirs(case_dir, exist_ok=True)

    # Validate file types
    allowed_extensions = {'.nii', '.nii.gz', '.dcm', '.png', '.jpg', '.jpeg'}
    uploaded_files = []

    for file in files:
        file_ext = os.path.splitext(file.filename)[1].lower()

        if file_ext == '.gz':
            # Handle .nii.gz
            if not file.filename.lower().endswith('.nii.gz'):
                raise HTTPException(status_code=400, detail=f"Invalid file format: {file.filename}")
            file_ext = '.nii.gz'

        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File format not supported: {file.filename}. Allowed: {allowed_extensions}"
            )

        # Save file in case directory
        file_path = os.path.join(case_dir, file.filename)

        try:
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            uploaded_files.append(file.filename)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving file {file.filename}: {str(e)}")

    # Determine file type for status message
    file_types = set([os.path.splitext(f)[1].lower() for f in uploaded_files])
    if '.dcm' in file_types:
        status = f"uploaded_{len(uploaded_files)}_dicom_slices"
    else:
        status = "uploaded"
    
    # If .nii.gz file uploaded, trigger automatic segmentation in background
    has_nifti = any(f.lower().endswith('.nii.gz') or f.lower().endswith('.nii') for f in uploaded_files)
    if has_nifti:
        # Find the NIfTI file
        nifti_file = None
        for f in uploaded_files:
            if f.lower().endswith('.nii.gz') or f.lower().endswith('.nii'):
                nifti_file = os.path.join(case_dir, f)
                break
        
        if nifti_file and os.path.exists(nifti_file):
            # Run segmentation in background
            try:
                background_tasks.add_task(
                    process_nifti_to_stl_files,
                    nifti_file,
                    case_id
                )
                status = "uploaded_and_segmenting"
            except Exception as e:
                print(f"Warning: Could not start background segmentation: {e}")
                status = "uploaded"

    return UploadResponse(
        case_id=case_id,
        filename=f"{len(uploaded_files)} files" if len(uploaded_files) > 1 else uploaded_files[0],
        status=status
    )
