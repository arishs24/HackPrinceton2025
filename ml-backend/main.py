from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gemini_service import analyze_brain_removal

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

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "PreSurg.AI Brain Surgery ML API",
        "version": "1.0.0",
        "organ": "brain"
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

@app.get("/api/health")
def health_check():
    return {"api": "healthy", "gemini": "connected", "organ": "brain"}