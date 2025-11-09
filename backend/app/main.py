from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="NeuroSim API",
    description="AI-Driven Brain Surgery Simulation Platform",
    version="1.0.0"
)

# Configure CORS - Allow all localhost ports for development
cors_origins_env = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:5174")
origins = [origin.strip() for origin in cors_origins_env.split(",")]

# Ensure common development ports are included
default_origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:3000",
]
for origin in default_origins:
    if origin not in origins:
        origins.append(origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from app.routers import upload, segmentation, simulation, gemini, snowflake, stl

# Include routers
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(segmentation.router, prefix="/api", tags=["segmentation"])
app.include_router(simulation.router, prefix="/api", tags=["simulation"])
app.include_router(gemini.router, prefix="/api/gemini", tags=["gemini"])
app.include_router(snowflake.router, prefix="/api/snowflake", tags=["snowflake"])
app.include_router(stl.router, prefix="/api", tags=["stl"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to NeuroSim API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
