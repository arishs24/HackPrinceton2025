# STL-Based Brain Segmentation and FEA Pipeline - Implementation Summary

## Overview
This implementation creates a complete pipeline for uploading MRI scans (.nii.gz files), automatically segmenting them into brain structures, converting each structure to STL files, and running Finite Element Analysis (FEA) on selected structures.

## Architecture

### Backend (`backend/`)
1. **Upload Endpoint** (`app/routers/upload.py`)
   - Accepts .nii.gz file uploads
   - Automatically triggers segmentation in background after upload
   - Returns case_id for tracking

2. **Segmentation Service** (`app/services/nifti_to_stl.py`)
   - Segments NIfTI files into brain regions using SynthSeg (or fallback method)
   - Extracts individual regions as separate NIfTI files
   - Converts each region to STL format using marching cubes
   - Saves STL files to `stl/{case_id}/` directory

3. **STL Router** (`app/routers/stl.py`)
   - Lists all STL files for a case: `GET /api/stl/{case_id}`
   - Serves STL files: `GET /api/stl/{case_id}/{filename}`

### ML Backend (`ml-backend/`)
1. **FEA Endpoint** (`main.py`)
   - Accepts structure identifier (name, label, filename)
   - Runs FEA simulation using Gemini API
   - Returns stress distribution and affected regions
   - Endpoint: `POST /api/fea`

### Frontend (`frontend/`)
1. **STL Viewer Page** (`pages/STLViewerPage.tsx`)
   - Main page for the STL-based workflow
   - Accessible at `/stl-viewer` route

2. **STL Viewer Component** (`components/STLViewer.tsx`)
   - Loads and displays multiple STL files using Three.js
   - Supports selection by clicking on structures
   - Visualizes FEA results with color coding:
     - Orange: Selected structure
     - Red: High stress regions
     - Orange: Moderate stress
     - Yellow: Low stress
     - Gray: Normal

3. **STL Structure List** (`components/STLStructureList.tsx`)
   - Lists all available brain structures
   - Shows selected structure
   - Displays structure metadata

4. **STL Viewer Hook** (`hooks/useSTLViewer.ts`)
   - Manages STL file loading
   - Polls for new STL files during segmentation
   - Handles structure selection
   - Runs FEA simulations

## Workflow

1. **Upload**: User uploads .nii.gz file via frontend
2. **Automatic Segmentation**: Backend automatically:
   - Segments brain into labeled regions
   - Converts each region to STL format
   - Saves to `stl/{case_id}/` folder
3. **Display**: Frontend polls for STL files and displays them in 3D viewer
4. **Selection**: User clicks on a structure in the 3D viewer or list
5. **FEA Simulation**: User clicks "Run FEA Simulation" button
6. **Results**: FEA results are displayed:
   - Color-coded visualization on STL models
   - Stress distribution analysis
   - Affected regions list
   - Recommendations

## API Endpoints

### Backend (`http://localhost:8000`)
- `POST /api/upload` - Upload .nii.gz file
- `GET /api/stl/{case_id}` - List STL files for a case
- `GET /api/stl/{case_id}/{filename}` - Download STL file

### ML Backend (`http://localhost:8001`)
- `POST /api/fea` - Run FEA on selected structure
  ```json
  {
    "case_id": "uuid",
    "structure_name": "Gray Matter",
    "structure_label": 2,
    "stl_filename": "Gray_Matter.stl"
  }
  ```

## File Structure

```
backend/
  app/
    routers/
      upload.py          # File upload with auto-segmentation
      stl.py             # STL file management
    services/
      nifti_to_stl.py    # Segmentation and STL conversion
    models/
      schemas.py         # Added STLFileInfo, STLListResponse

ml-backend/
  main.py                # Added FEA endpoint

frontend/
  src/
    pages/
      STLViewerPage.tsx  # Main STL viewer page
    components/
      STLViewer.tsx      # 3D STL visualization
      STLStructureList.tsx # Structure list sidebar
    hooks/
      useSTLViewer.ts    # STL management hook
    utils/
      api.ts             # Added STL and FEA API calls
    types/
      index.ts           # Added STL and FEA types
```

## Dependencies

### Backend
- `nibabel` - NIfTI file handling
- `trimesh` - STL mesh processing
- `scikit-image` - Marching cubes algorithm

### Frontend
- `three` - 3D rendering (already installed)
- `@react-three/fiber` - React Three.js integration
- `@react-three/drei` - Three.js helpers

## Usage

1. **Start Backend**:
   ```bash
   cd backend
   uvicorn app.main:app --reload --port 8000
   ```

2. **Start ML Backend**:
   ```bash
   cd ml-backend
   uvicorn main:app --reload --port 8001
   ```

3. **Start Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

4. **Access STL Viewer**:
   - Navigate to `http://localhost:5173/stl-viewer`
   - Upload a .nii.gz file
   - Wait for segmentation (polls automatically)
   - Select a structure
   - Click "Run FEA Simulation"
   - View results

## Notes

- Segmentation runs in background after upload
- Frontend polls every 3 seconds for new STL files during processing
- STL files are stored in `stl/{case_id}/` directory
- FEA simulation uses Gemini API for analysis (can be replaced with actual FEA solver)
- The system supports both SynthSeg and fallback thresholding-based segmentation

