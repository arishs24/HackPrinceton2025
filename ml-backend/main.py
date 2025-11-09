from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import uuid
import os
import aiofiles
import glob
from gemini_service import analyze_brain_removal
from segmentation_service import process_nifti_to_stl_files

app = FastAPI(
    title="PreSurg.AI - Brain Surgery ML API",
    description="AI-powered pre-surgical brain tissue removal simulation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories
UPLOAD_DIR = "uploads"
# STL folder is in project root, not ml-backend folder
# Get the directory where this file is located (ml-backend/)
ml_backend_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to project root, then into stl/
project_root = os.path.dirname(ml_backend_dir)
STL_BASE_DIR = os.path.join(project_root, "stl")
STL_BASE_DIR = os.path.abspath(STL_BASE_DIR)
os.makedirs(UPLOAD_DIR, exist_ok=True)
# Don't create stl dir if it doesn't exist - it should already exist
print(f"STL_BASE_DIR: {STL_BASE_DIR}")
print(f"STL directory exists: {os.path.exists(STL_BASE_DIR)}")

# NEW: Proper coordinate model
class Coordinates(BaseModel):
    x: float
    y: float
    z: float

class RemovalRegion(BaseModel):
    brainRegion: str
    hemisphere: str
    coordinates: Coordinates  # Now properly typed!
    volumeToRemove: str

class SurgeryRequest(BaseModel):
    procedureType: str
    removalRegion: RemovalRegion
    patientAge: int
    reason: str

# NEW: Structure-based FEA request with optional parameters
class StructureFEARequest(BaseModel):
    case_id: str
    structure_name: str
    structure_label: int
    stl_filename: str
    # Optional parameters for simulation
    coordinates: Optional[Coordinates] = None
    volume_to_remove: Optional[str] = None
    patient_age: Optional[int] = None
    procedure_type: Optional[str] = None
    reason: Optional[str] = None

# Upload and STL models
class UploadResponse(BaseModel):
    case_id: str
    filename: str
    status: str

class STLFileInfo(BaseModel):
    filename: str
    name: str
    label: int
    voxels: int

class STLListResponse(BaseModel):
    case_id: str
    stl_files: List[STLFileInfo]
    status: str

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "PreSurg.AI Brain Surgery ML API",
        "version": "1.0.0",
        "organ": "brain"
    }

@app.get("/api")
def api_root():
    """API root endpoint"""
    return {
        "status": "online",
        "endpoints": {
            "upload": "/api/upload",
            "segment": "/api/segment",
            "stl_list": "/api/stl/{case_id}",
            "stl_file": "/api/stl/{case_id}/{filename}",
            "fea": "/api/fea",
            "simulate": "/api/simulate",
            "health": "/api/health"
        }
    }

# Upload endpoint
@app.post("/api/upload", response_model=UploadResponse)
async def upload_scan(files: List[UploadFile] = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    """
    Upload brain scan file(s) - supports .nii.gz files
    Automatically triggers segmentation in background
    """
    case_id = str(uuid.uuid4())
    case_dir = os.path.join(UPLOAD_DIR, case_id)
    os.makedirs(case_dir, exist_ok=True)

    allowed_extensions = {'.nii', '.nii.gz'}
    uploaded_files = []

    for file in files:
        file_ext = os.path.splitext(file.filename)[1].lower()

        if file_ext == '.gz':
            if not file.filename.lower().endswith('.nii.gz'):
                raise HTTPException(status_code=400, detail=f"Invalid file format: {file.filename}")
            file_ext = '.nii.gz'

        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File format not supported: {file.filename}. Allowed: {allowed_extensions}"
            )

        file_path = os.path.join(case_dir, file.filename)

        try:
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            uploaded_files.append(file.filename)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving file {file.filename}: {str(e)}")

    # For now, just mark as segmenting (we'll load existing STL files from stl/ folder)
    # TODO: Enable actual segmentation later
    has_nifti = any(f.lower().endswith('.nii.gz') or f.lower().endswith('.nii') for f in uploaded_files)
    status = "uploaded"
    
    if has_nifti:
        # Don't actually segment, just mark as "segmenting" to show loading state
        # We'll load existing STL files from the stl/ folder instead
        status = "uploaded_and_segmenting"

    return UploadResponse(
        case_id=case_id,
        filename=f"{len(uploaded_files)} files" if len(uploaded_files) > 1 else uploaded_files[0],
        status=status
    )

# STL endpoints
@app.get("/api/stl/{case_id}", response_model=STLListResponse)
async def list_stl_files(case_id: str):
    """
    List all STL files for a given case ID
    For now, returns all STL files from the root stl/ folder (not case-specific)
    """
    # For now, load all STL files from root stl/ folder
    # Later we can make it case-specific: case_stl_dir = os.path.join(STL_BASE_DIR, case_id)
    stl_pattern = os.path.join(STL_BASE_DIR, "*.stl")
    stl_files = glob.glob(stl_pattern)
    print(f"[STL List] Looking in: {stl_pattern}")
    print(f"[STL List] Found {len(stl_files)} STL files")
    
    # If no files in root, check case-specific folder
    if not stl_files:
        case_stl_dir = os.path.join(STL_BASE_DIR, case_id)
        if os.path.exists(case_stl_dir):
            stl_files = glob.glob(os.path.join(case_stl_dir, "*.stl"))
            print(f"[STL List] Checked case folder: {case_stl_dir}, found {len(stl_files)} files")
    
    stl_info_list = []
    for stl_path in stl_files:
        filename = os.path.basename(stl_path)
        name = filename.replace(".stl", "")
        
        # Clean up name - remove leading underscores and numbers
        name = name.lstrip("_")
        if name and name[0].isdigit():
            # Remove leading digits
            name = name.lstrip("0123456789_")
        
        # Try to extract label from name (e.g., "Gray_Matter_2" -> label 2)
        label = 0
        if "_" in name:
            parts = name.rsplit("_", 1)
            if parts[1].isdigit():
                label = int(parts[1])
                name = parts[0]
        
        # Clean display name
        display_name = name.replace("_", " ").replace("  ", " ").strip()
        if not display_name:
            display_name = filename.replace(".stl", "")
        
        stl_info_list.append(STLFileInfo(
            filename=filename,
            name=display_name,
            label=label,
            voxels=0
        ))
    
    # Sort by name for better display
    stl_info_list.sort(key=lambda x: x.name)
    
    # Return all files immediately (frontend will handle showing "segmenting" delay)
    return STLListResponse(
        case_id=case_id,
        stl_files=stl_info_list,
        status="ready" if stl_info_list else "processing"
    )

@app.get("/api/stl/{case_id}/{filename}")
async def get_stl_file(case_id: str, filename: str):
    """
    Serve STL file for download/viewing
    For now, looks in root stl/ folder first, then case-specific folder
    """
    # First try root stl/ folder
    stl_path = os.path.join(STL_BASE_DIR, filename)
    
    # If not found, try case-specific folder
    if not os.path.exists(stl_path):
        case_stl_dir = os.path.join(STL_BASE_DIR, case_id)
        stl_path = os.path.join(case_stl_dir, filename)
    
    if not os.path.exists(stl_path):
        raise HTTPException(status_code=404, detail=f"STL file not found: {filename}")
    
    return FileResponse(
        stl_path,
        media_type="application/octet-stream",
        filename=filename
    )

# Segment endpoint (for compatibility with old frontend code)
# Note: Segmentation now happens automatically after upload
class SegmentRequest(BaseModel):
    case_id: str

@app.post("/api/segment")
async def segment_brain(request: SegmentRequest):
    """
    Segment brain structures (for compatibility)
    Note: Segmentation is now automatic after upload, but this endpoint
    returns the current STL file status for the case
    """
    case_id = request.case_id
    
    # Check if STL files exist
    case_stl_dir = os.path.join(STL_BASE_DIR, case_id)
    stl_files = glob.glob(os.path.join(case_stl_dir, "*.stl")) if os.path.exists(case_stl_dir) else []
    
    # Return a response compatible with the old SegmentationResponse format
    # But we'll use STL files instead
    return {
        "case_id": case_id,
        "status": "ready" if stl_files else "processing",
        "stl_files_available": len(stl_files) > 0,
        "message": "Segmentation is automatic after upload. Check /api/stl/{case_id} for STL files."
    }

@app.post("/api/simulate")
def simulate_surgery(request: SurgeryRequest):
    """Analyze brain tissue removal consequences"""
    try:
        result = analyze_brain_removal(
            procedure_type=request.procedureType,
            removal_region=request.removalRegion.dict(),
            patient_age=request.patientAge,
            reason=request.reason
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/fea")
def run_fea_simulation(request: StructureFEARequest):
    """
    Analyze a selected brain structure using Gemini AI.
    When a user clicks on a structure (e.g., "Left hippocampus proper"), 
    this analyzes the consequences of removing that structure.
    Returns comprehensive neurological analysis including FEA-like stress distribution.
    """
    try:
        # Parse structure name to extract brain region and hemisphere
        structure_name_lower = request.structure_name.lower()
        
        # Extract hemisphere
        if "left" in structure_name_lower:
            hemisphere = "left"
            brain_region = request.structure_name.replace("Left", "").replace("left", "").strip()
        elif "right" in structure_name_lower:
            hemisphere = "right"
            brain_region = request.structure_name.replace("Right", "").replace("right", "").strip()
        else:
            # Default to left if not specified
            hemisphere = "left"
            brain_region = request.structure_name
        
        # Clean up brain region name (remove common suffixes)
        brain_region = brain_region.replace("(2)", "").replace("(3)", "").strip()
        
        # Use provided parameters or defaults
        procedure_type = request.procedure_type or "tumor resection"
        patient_age = request.patient_age or 45
        reason = request.reason or f"Tumor removal from {request.structure_name}"
        volume_to_remove = request.volume_to_remove or "variable"
        
        # Use provided coordinates or default to center
        if request.coordinates:
            coordinates = {
                "x": request.coordinates.x,
                "y": request.coordinates.y,
                "z": request.coordinates.z
            }
        else:
            coordinates = {"x": 0.0, "y": 0.0, "z": 0.0}
        
        # Use Gemini to analyze the structure removal
        result = analyze_brain_removal(
            procedure_type=procedure_type,
            removal_region={
                "brainRegion": brain_region,
                "hemisphere": hemisphere,
                "coordinates": coordinates,
                "volumeToRemove": volume_to_remove
            },
            patient_age=patient_age,
            reason=reason
        )
        
        # Debug: Print Gemini response structure
        print(f"Gemini response keys: {result.keys()}")
        print(f"Removal summary: {result.get('removalSummary', {})}")
        
        # Extract affected regions from Gemini's removalSummary
        removal_summary = result.get("removalSummary", {})
        affected_regions = removal_summary.get("affectedRegions", [])
        preserved_regions = removal_summary.get("preservedRegions", [])
        
        # Also check if regions are in other parts of the response
        if not affected_regions:
            # Try to extract from risks or other sections
            risks = result.get("risks", [])
            for risk in risks:
                if isinstance(risk, dict) and "consequences" in risk:
                    # Try to extract brain regions from risk consequences
                    consequences = risk.get("consequences", "")
                    if isinstance(consequences, str) and len(consequences) > 10:
                        # Could parse regions from text, but for now just use structure name
                        pass
        
        # If no affected regions, use the structure name and common adjacent areas
        if not affected_regions:
            affected_regions = [request.structure_name]
            # Add common adjacent structures based on brain region type
            if "gyrus" in brain_region.lower() or "cortex" in brain_region.lower():
                affected_regions.append("Adjacent cortical areas")
            if "hippocampus" in brain_region.lower():
                affected_regions.append("Temporal lobe connections")
            if "frontal" in brain_region.lower():
                affected_regions.append("Prefrontal connections")
        
        # Determine stress levels based on neurological deficits severity and actual regions
        high_stress_regions = []
        moderate_stress_regions = []
        low_stress_regions = []
        
        # Check neurological deficits to determine stress
        neuro_deficits = result.get("neurologicalDeficits", {})
        max_severity = "NONE"
        
        for deficit_type, deficit_info in neuro_deficits.items():
            if isinstance(deficit_info, dict) and deficit_info.get("affected"):
                severity = deficit_info.get("severity", "MODERATE")
                
                # Track maximum severity
                severity_order = {"SEVERE": 3, "MODERATE": 2, "MILD": 1, "NONE": 0}
                if severity_order.get(severity, 0) > severity_order.get(max_severity, 0):
                    max_severity = severity
                
                # Get specific affected areas from deficit description
                description = deficit_info.get("description", "")
                body_parts = deficit_info.get("bodyParts", [])
                
                # Extract brain region names from description if possible
                # Look for common brain anatomy terms
                brain_terms = ["gyrus", "cortex", "lobe", "nucleus", "tract", "pathway", "area", "region"]
                extracted_regions = []
                if description:
                    desc_lower = description.lower()
                    # Try to find brain region mentions
                    for term in brain_terms:
                        if term in desc_lower:
                            # Extract surrounding words as potential region name
                            words = description.split()
                            for i, word in enumerate(words):
                                if term in word.lower():
                                    # Get 2-3 words around the term
                                    start = max(0, i-1)
                                    end = min(len(words), i+2)
                                    region_phrase = " ".join(words[start:end])
                                    if region_phrase not in extracted_regions and len(region_phrase) > 5:
                                        extracted_regions.append(region_phrase)
                
                # Add to appropriate stress level with cleaner formatting
                if severity == "SEVERE":
                    if extracted_regions:
                        high_stress_regions.extend(extracted_regions[:2])  # Limit to 2
                    elif body_parts:
                        high_stress_regions.append(f"Contralateral {body_parts[0]} motor cortex")
                    else:
                        high_stress_regions.append(f"{deficit_type.capitalize()} pathways")
                elif severity == "MODERATE":
                    if extracted_regions:
                        moderate_stress_regions.extend(extracted_regions[:2])
                    elif body_parts:
                        moderate_stress_regions.append(f"{body_parts[0]} motor pathways")
                    else:
                        # Clean up description - remove redundant parts
                        clean_desc = description.replace(f"{deficit_type.lower()} ", "").replace("deficits ", "").replace("expected from ", "")
                        if len(clean_desc) > 60:
                            clean_desc = clean_desc[:60] + "..."
                        if clean_desc and clean_desc not in moderate_stress_regions:
                            moderate_stress_regions.append(clean_desc)
                else:
                    if extracted_regions:
                        low_stress_regions.extend(extracted_regions[:1])
                    elif description and len(description) < 50:
                        low_stress_regions.append(description)
        
        # Use actual affected regions from Gemini for stress distribution
        # Primary resection site is always high stress (and only in high stress)
        if request.structure_name not in high_stress_regions:
            high_stress_regions.insert(0, request.structure_name)  # Put at front
        
        # Remove structure name from other stress levels to avoid duplication
        moderate_stress_regions = [r for r in moderate_stress_regions if r.lower() != request.structure_name.lower()]
        low_stress_regions = [r for r in low_stress_regions if r.lower() != request.structure_name.lower()]
        
        # Add adjacent regions from affected_regions (these are from Gemini's analysis)
        for region in affected_regions:
            if region and region.lower() != request.structure_name.lower():
                # Check if it's already in any stress category
                region_lower = region.lower()
                already_added = (
                    any(r.lower() == region_lower for r in high_stress_regions) or
                    any(r.lower() == region_lower for r in moderate_stress_regions) or
                    any(r.lower() == region_lower for r in low_stress_regions)
                )
                
                if not already_added:
                    # Determine stress level based on region type and keywords
                    if any(keyword in region_lower for keyword in ["primary", "direct", "immediate", "critical", "eloquent"]):
                        high_stress_regions.append(region)
                    elif any(keyword in region_lower for keyword in ["adjacent", "connected", "nearby", "surrounding", "associated"]):
                        moderate_stress_regions.append(region)
                    else:
                        # Default to moderate for affected regions (they're affected, so not low stress)
                        moderate_stress_regions.append(region)
        
        # Add preserved regions as low stress
        for region in preserved_regions[:3]:  # Limit to first 3
            if region not in low_stress_regions:
                low_stress_regions.append(region)
        
        # Calculate max stress based on severity
        stress_map = {"SEVERE": 180.0, "MODERATE": 120.0, "MILD": 85.0, "NONE": 60.0}
        max_stress = stress_map.get(max_severity, 100.0)
        
        # Remove duplicates and limit regions
        high_stress_regions = list(dict.fromkeys(high_stress_regions))[:5]  # Preserve order, remove dupes
        moderate_stress_regions = list(dict.fromkeys(moderate_stress_regions))[:5]
        low_stress_regions = list(dict.fromkeys(low_stress_regions))[:5]
        
        # Ensure we have at least the structure name in high stress
        if not high_stress_regions or high_stress_regions[0].lower() != request.structure_name.lower():
            high_stress_regions.insert(0, request.structure_name)
        
        # Add FEA results to the Gemini analysis
        result["fea_results"] = {
            "structure_name": request.structure_name,
            "structure_label": request.structure_label,
            "stl_filename": request.stl_filename,
            "max_stress_kpa": max_stress,
            "affected_regions": affected_regions if affected_regions else [request.structure_name],
            "stress_distribution": {
                "high_stress": high_stress_regions,
                "moderate_stress": moderate_stress_regions,
                "low_stress": low_stress_regions
            }
        }
        
        return result
    except Exception as e:
        print(f"Error in FEA simulation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
def health_check():
    return {"api": "healthy", "gemini": "connected", "organ": "brain"}