import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def analyze_surgery(surgery_type: str, location: str, force: float, angle: float) -> dict:
    """
    Analyze surgical parameters using Gemini AI to predict biomechanical outcomes.
    
    Args:
        surgery_type: Type of surgery (osteotomy, implant, etc.)
        location: Target anatomical location (mandible, maxilla, etc.)
        force: Applied force in Newtons
        angle: Cutting angle in degrees
        
    Returns:
        Dictionary with fracture risk, stress points, verdict, reasoning, and recommendation
    """
    
    # Create the prompt
    prompt = f"""You are an expert biomechanical engineer specializing in maxillofacial surgery simulation and finite element analysis.

PATIENT DATA:
- Skull: Adult human, normal bone density
- Bone properties: Cortical bone (Young's modulus: 15 GPa, Poisson's ratio: 0.3)

SURGICAL PARAMETERS:
- Procedure: {surgery_type}
- Target Location: {location}
- Applied Force: {force} Newtons
- Cutting Angle: {angle} degrees

TASK: Perform a comprehensive biomechanical analysis and predict outcomes.

Analyze:
1. Von Mises stress distribution and concentration points
2. Fracture probability based on force magnitude, angle, and bone geometry
3. Risk of complications (nerve damage, vascular injury, structural failure)
4. Alternative safer surgical approaches

Respond with ONLY valid JSON (no markdown, no code blocks, no extra text):
{{
  "fractureRisk": <integer 0-100>,
  "stressPoints": [
    {{"x": <float -1 to 1>, "y": <float -1 to 1>, "z": <float -1 to 1>, "intensity": <float 0-1>}}
  ],
  "verdict": "<SAFE|CAUTION|DANGER>",
  "reasoning": "<concise 2-3 sentence biomechanical explanation>",
  "recommendation": "<specific actionable surgical advice>"
}}

Generate 4-6 realistic stress concentration points around the {location} region based on anatomical stress distribution patterns."""

    try:
        # Call Gemini API
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content(prompt)
        
        # Extract and clean JSON response
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        response_text = re.sub(r'```json\s*', '', response_text)
        response_text = re.sub(r'```\s*', '', response_text)
        
        # Parse JSON
        result = json.loads(response_text)
        
        # Validate and return
        return {
            "fractureRisk": int(result.get("fractureRisk", 50)),
            "stressPoints": result.get("stressPoints", []),
            "verdict": result.get("verdict", "CAUTION"),
            "reasoning": result.get("reasoning", "Analysis completed"),
            "recommendation": result.get("recommendation", "Proceed with standard protocols")
        }
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Response text: {response_text}")
        # Return fallback result
        return generate_fallback_result(surgery_type, location, force, angle)
        
    except Exception as e:
        print(f"Gemini API error: {e}")
        return generate_fallback_result(surgery_type, location, force, angle)


def generate_fallback_result(surgery_type: str, location: str, force: float, angle: float) -> dict:
    """
    Generate a physics-based fallback simulation if Gemini fails.
    """
    # Calculate fracture risk based on force
    fracture_risk = min(int((force / 100) * 80 + (angle / 90) * 20), 100)
    
    # Determine verdict
    if fracture_risk > 70:
        verdict = "DANGER"
    elif fracture_risk > 40:
        verdict = "CAUTION"
    else:
        verdict = "SAFE"
    
    # Generate stress points based on location
    stress_points = generate_stress_points(location, force / 100)
    
    return {
        "fractureRisk": fracture_risk,
        "stressPoints": stress_points,
        "verdict": verdict,
        "reasoning": f"Stress analysis indicates {fracture_risk}% fracture probability at {location} with {force}N force at {angle}° angle. Force magnitude is {'high' if force > 60 else 'moderate' if force > 30 else 'low'}.",
        "recommendation": f"{'Reduce force below 50N or adjust angle to 30-40°' if force > 60 else 'Current parameters are within acceptable range. Monitor stress distribution during procedure.'}"
    }


def generate_stress_points(location: str, intensity_factor: float) -> list:
    """
    Generate anatomically realistic stress concentration points.
    """
    stress_patterns = {
        "mandible": [
            {"x": 0.5, "y": -0.3, "z": 0.1, "intensity": intensity_factor * 0.9},
            {"x": -0.5, "y": -0.3, "z": 0.1, "intensity": intensity_factor * 0.85},
            {"x": 0, "y": -0.5, "z": 0, "intensity": intensity_factor * 0.95},
            {"x": 0.3, "y": -0.2, "z": -0.2, "intensity": intensity_factor * 0.7},
            {"x": -0.3, "y": -0.2, "z": -0.2, "intensity": intensity_factor * 0.65}
        ],
        "maxilla": [
            {"x": 0.4, "y": 0.2, "z": 0.1, "intensity": intensity_factor * 0.85},
            {"x": -0.4, "y": 0.2, "z": 0.1, "intensity": intensity_factor * 0.8},
            {"x": 0, "y": 0.3, "z": 0, "intensity": intensity_factor * 0.9},
            {"x": 0.2, "y": 0.1, "z": 0.2, "intensity": intensity_factor * 0.6}
        ],
        "zygomatic": [
            {"x": 0.6, "y": 0.1, "z": 0.2, "intensity": intensity_factor * 0.9},
            {"x": 0.4, "y": 0.2, "z": 0.3, "intensity": intensity_factor * 0.75},
            {"x": 0.5, "y": 0, "z": 0.1, "intensity": intensity_factor * 0.8}
        ],
        "temporal": [
            {"x": 0.7, "y": 0.3, "z": 0.1, "intensity": intensity_factor * 0.85},
            {"x": 0.5, "y": 0.4, "z": 0, "intensity": intensity_factor * 0.7},
            {"x": 0.6, "y": 0.2, "z": -0.1, "intensity": intensity_factor * 0.75}
        ]
    }
    
    return stress_patterns.get(location, stress_patterns["mandible"])