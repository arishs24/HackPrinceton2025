from fastapi import APIRouter, HTTPException
from app.models.schemas import GeminiRequest, GeminiResponse
from app.services.gemini_service import generate_surgical_insights
import uuid

router = APIRouter()


@router.post("/analyze", response_model=GeminiResponse)
async def analyze_simulation(request: GeminiRequest):
    """
    Generate AI-powered surgical insights using Google Gemini
    """
    try:
        # Generate or use existing conversation ID
        conversation_id = request.conversation_id or str(uuid.uuid4())

        # Get insights from Gemini
        technical_summary, patient_summary = await generate_surgical_insights(
            simulation_results=request.simulation_results,
            query=request.query,
            conversation_id=conversation_id
        )

        return GeminiResponse(
            technical_summary=technical_summary,
            patient_summary=patient_summary,
            conversation_id=conversation_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")
