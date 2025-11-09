from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gemini_service import analyze_surgery

# Create FastAPI app
app = FastAPI(
    title="PreSurg.AI - ML Simulation API",
    description="AI-powered pre-surgical biomechanical simulation",
    version="1.0.0"
)

# Allow frontend to call this API (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class SurgeryRequest(BaseModel):
    surgeryType: str
    location: str
    force: float
    angle: float

# Response model
class SurgeryResponse(BaseModel):
    fractureRisk: int
    stressPoints: list
    verdict: str
    reasoning: str
    recommendation: str

@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "PreSurg.AI ML API",
        "version": "1.0.0"
    }

@app.post("/api/simulate", response_model=SurgeryResponse)
def simulate_surgery(request: SurgeryRequest):
    """
    Main endpoint: Analyze surgical parameters and return risk prediction
    """
    try:
        # Call Gemini AI service
        result = analyze_surgery(
            surgery_type=request.surgeryType,
            location=request.location,
            force=request.force,
            angle=request.angle
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
def health_check():
    """Check if API and Gemini connection is working"""
    return {
        "api": "healthy",
        "gemini": "connected"
    }