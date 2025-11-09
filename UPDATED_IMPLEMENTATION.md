# Updated Implementation - Using ml-backend Only

## Overview
The implementation has been refactored to use **only the `ml-backend`** folder as the backend, which acts as the Gemini API wrapper and handles all backend operations including upload, segmentation, and FEA simulation.

## Architecture

### Backend (`ml-backend/`)
1. **main.py** - Main FastAPI application with all endpoints:
   - `POST /api/upload` - Upload .nii.gz files, automatically triggers segmentation
   - `GET /api/stl/{case_id}` - List STL files for a case
   - `GET /api/stl/{case_id}/{filename}` - Download STL file
   - `POST /api/fea` - Run FEA simulation on selected structure
   - `POST /api/simulate` - Original surgery simulation endpoint

2. **segmentation_service.py** - Uses existing segmentation scripts:
   - Imports functions from `segment_brain_regions.py` (in project root)
   - Uses `make_3d_model.py` approach for NIfTI to STL conversion
   - Processes: Segment → Extract regions → Convert to STL

3. **gemini_service.py** - Gemini API wrapper for FEA analysis

### Frontend (`frontend/`)
- All API calls now point to `ml-backend` (port 8001)
- STL viewer page at `/stl-viewer`
- Components unchanged from previous implementation

## Workflow

1. **Upload**: User uploads .nii.gz → `ml-backend` saves file
2. **Auto-Segmentation**: Background task calls `segment_brain_regions.py` functions
3. **STL Generation**: Uses `make_3d_model.py` approach to convert regions to STL
4. **Display**: Frontend polls for STL files and displays them
5. **FEA**: User selects structure → Calls `/api/fea` → Gemini analyzes → Results displayed

## Key Changes

- **Removed dependency on `/backend` folder**
- **All endpoints in `ml-backend/main.py`**
- **Uses existing `segment_brain_regions.py` and `make_3d_model.py` scripts**
- **Frontend API base URL: `http://localhost:8001/api`**

## Setup

1. **Install dependencies**:
   ```bash
   cd ml-backend
   pip install -r requirements.txt
   ```

2. **Start ml-backend**:
   ```bash
   cd ml-backend
   uvicorn main:app --reload --port 8001
   ```

3. **Start frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

4. **Access**: Navigate to `http://localhost:5173/stl-viewer`

## File Structure

```
ml-backend/
  main.py                    # All API endpoints
  segmentation_service.py    # Uses existing scripts
  gemini_service.py          # Gemini wrapper
  requirements.txt           # Updated with dependencies

frontend/
  src/
    pages/
      STLViewerPage.tsx      # Main STL viewer
    components/
      STLViewer.tsx          # 3D STL visualization
      STLStructureList.tsx   # Structure list
    hooks/
      useSTLViewer.ts        # STL management
    utils/
      api.ts                 # API calls (points to ml-backend)
```

## Notes

- Segmentation uses existing `segment_brain_regions.py` script functions
- STL conversion uses the same approach as `make_3d_model.py`
- All STL files saved to `stl/{case_id}/` directory
- Frontend automatically polls for new STL files during processing

