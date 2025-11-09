from fastapi import APIRouter, HTTPException
from app.models.schemas import SnowflakeSimulationData
from app.services.snowflake_service import save_simulation, get_similar_cases
from typing import List

router = APIRouter()


@router.post("/save")
async def save_simulation_data(data: SnowflakeSimulationData):
    """
    Save simulation data to Snowflake
    """
    try:
        result = await save_simulation(data)
        return {"status": "success", "message": "Simulation data saved", "case_id": data.case_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Snowflake save error: {str(e)}")


@router.get("/similar/{tumor_location}")
async def find_similar_cases(tumor_location: str, limit: int = 5):
    """
    Find similar cases from Snowflake based on tumor location
    """
    try:
        cases = await get_similar_cases(tumor_location, limit)
        return {"similar_cases": cases, "count": len(cases)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Snowflake query error: {str(e)}")
