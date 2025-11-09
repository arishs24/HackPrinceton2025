import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')


def analyze_brain_removal(procedure_type: str, removal_region: dict, patient_age: int, reason: str) -> dict:
    """
    Analyze consequences of removing a bone section.
    
    Args:
        procedure_type: Type of procedure (e.g., "resection")
        removal_region: Dict with boneName, section, startPoint, endPoint, estimatedSize
        patient_age: Patient age in years
        reason: Reason for surgery (e.g., "tumor removal")
    
    Returns:
        Comprehensive analysis of removal consequences
    """
    
    # Extract removal details
    brain_region = removal_region['brainRegion']  # "frontal lobe"
    hemisphere = removal_region.get('hemisphere', 'left')  # "left" or "right"
    coordinates = removal_region.get('coordinates', {'x': 0, 'y': 0, 'z': 0})
    volume = removal_region['volumeToRemove']  # "2cm³"
    
    # Create detailed prompt
    prompt = f"""You are an expert neurosurgeon and neurologist specializing in brain tumor resection and functional neurosurgery.

CLINICAL SCENARIO:
- Patient Age: {patient_age} years
- Procedure: {procedure_type}
- Indication: {reason}

BRAIN TISSUE REMOVAL PLAN:
- Brain Region: {brain_region}
- Hemisphere: {hemisphere}
- Coordinates: x={coordinates['x']:.2f}, y={coordinates['y']:.2f}, z={coordinates['z']:.2f}
- Volume to Remove: {volume}

COORDINATE SYSTEM: All coordinates are normalized (-1 to 1 range)
- x: -1 (left) to +1 (right)
- y: -1 (inferior) to +1 (superior)  
- z: -1 (posterior) to +1 (anterior)
- Origin: Center of brain

TASK: Predict ALL neurological and functional consequences of removing this brain tissue.

Analyze:
1. Neurological deficits (motor, sensory, cognitive, language)
2. Functional impact (movement, speech, memory, personality)
3. Compensatory mechanisms and neuroplasticity potential
4. Surgical approach and risks
5. Recovery prognosis and rehabilitation needs
6. Long-term quality of life

Respond with ONLY valid JSON (no markdown, no extra text):
{{
  "removalSummary": {{
    "affectedRegions": ["specific brain areas affected"],
    "preservedRegions": ["critical areas preserved"],
    "eloquentCortex": true|false
  }},
  
  "neurologicalDeficits": {{
    "motor": {{
      "affected": true|false,
      "description": "specific motor deficits",
      "severity": "SEVERE|MODERATE|MILD|NONE",
      "bodyParts": ["affected body parts"]
    }},
    "sensory": {{
      "affected": true|false,
      "description": "sensory changes",
      "severity": "SEVERE|MODERATE|MILD|NONE"
    }},
    "cognitive": {{
      "affected": true|false,
      "functions": ["memory", "attention", "executive function"],
      "description": "cognitive impact details",
      "severity": "SEVERE|MODERATE|MILD|NONE"
    }},
    "language": {{
      "affected": true|false,
      "type": "expressive|receptive|both|none",
      "description": "language deficits",
      "severity": "SEVERE|MODERATE|MILD|NONE"
    }}
  }},
  
  "functionalImpact": {{
    "mobility": "description of movement changes",
    "independence": "percentage of ADL independence",
    "communication": "ability to communicate",
    "cognition": "cognitive function level",
    "overallQualityOfLife": "percentage of pre-surgery QOL"
  }},
  
  "surgicalApproach": {{
    "recommendedApproach": "awake craniotomy|asleep surgery",
    "mapping": {{
      "required": true|false,
      "methods": ["intraoperative MRI", "cortical stimulation"],
      "reason": "why mapping is needed"
    }},
    "margins": {{
      "recommended": "distance in mm",
      "eloquentProximity": "distance to eloquent cortex"
    }}
  }},
  
  "risks": [
    {{
      "type": "specific neurological risk",
      "probability": "percentage",
      "consequences": "detailed consequences",
      "prevention": "prevention strategies",
      "reversibility": "permanent|potentially reversible|reversible"
    }}
  ],
  
  "recoveryPrognosis": {{
    "neuroplasticity": {{
      "potential": "HIGH|MODERATE|LOW",
      "factors": ["age", "lesion location", "rehabilitation"],
      "timeline": "expected recovery timeline"
    }},
    "rehabilitation": {{
      "required": true|false,
      "types": ["physical therapy", "speech therapy", "cognitive rehabilitation"],
      "duration": "estimated duration",
      "expectedImprovement": "percentage improvement possible"
    }},
    "longTermOutcome": {{
      "bestCase": "description of best outcome",
      "worstCase": "description of worst outcome",
      "mostLikely": "most probable outcome"
    }}
  }},
  
  "recommendations": [
    "specific surgical recommendation 1",
    "specific surgical recommendation 2",
    "specific surgical recommendation 3"
  ]
}}

Generate realistic, medically accurate neurological predictions based on functional neuroanatomy and neurosurgical literature."""

    try:
        # Call Gemini
        response = model.generate_content(prompt)
        text = response.text
        
        # Clean up response
        text = text.replace('```json', '').replace('```', '').strip()
        
        # Parse JSON
        result = json.loads(text)
        return result
        
    except Exception as e:
        print(f"Error: {e}")
        # Return fallback analysis
        return generate_fallback_analysis(brain_region, hemisphere, volume, patient_age)


def generate_fallback_analysis(brain_region: str, hemisphere: str, volume: str, patient_age: int) -> dict:
    """
    Fallback neurological analysis if Gemini fails
    """
    is_left = hemisphere == "left"
    
    return {
        "removalSummary": {
            "affectedRegions": [f"{hemisphere} {brain_region}"],
            "preservedRegions": ["Contralateral hemisphere", "Brainstem"],
            "eloquentCortex": brain_region in ["frontal lobe", "temporal lobe", "parietal lobe"]
        },
        
        "neurologicalDeficits": {
            "motor": {
                "affected": "motor" in brain_region.lower() or "frontal" in brain_region.lower(),
                "description": "Possible contralateral motor weakness",
                "severity": "MODERATE",
                "bodyParts": ["Opposite side of body"]
            },
            "cognitive": {
                "affected": True,
                "functions": ["Working memory", "Executive function"],
                "description": f"Cognitive deficits expected from {brain_region} removal",
                "severity": "MODERATE"
            },
            "language": {
                "affected": is_left and brain_region in ["frontal lobe", "temporal lobe"],
                "type": "expressive" if "frontal" in brain_region else "receptive",
                "description": "Language deficits if dominant hemisphere",
                "severity": "MODERATE" if is_left else "MILD"
            }
        },
        
        "functionalImpact": {
            "mobility": "Potential motor weakness on opposite side",
            "independence": "60-70%",
            "communication": "Moderate language impairment expected" if is_left else "Minimal impact",
            "cognition": "Working memory and attention deficits likely",
            "overallQualityOfLife": "65%"
        },
        
        "surgicalApproach": {
            "recommendedApproach": "awake craniotomy" if is_left else "asleep surgery",
            "mapping": {
                "required": True,
                "methods": ["Cortical stimulation", "fMRI"],
                "reason": "To preserve eloquent cortex"
            },
            "margins": {
                "recommended": "5-10mm from eloquent areas",
                "eloquentProximity": "Close to critical regions"
            }
        },
        
        "risks": [
            {
                "type": "Motor deficit",
                "probability": "30%",
                "consequences": "Weakness on opposite side",
                "prevention": "Awake surgery with motor mapping",
                "reversibility": "potentially reversible"
            },
            {
                "type": "Cognitive impairment",
                "probability": "50%",
                "consequences": "Memory and executive deficits",
                "prevention": "Minimize resection volume",
                "reversibility": "partially reversible"
            },
            {
                "type": "Seizures",
                "probability": "25%",
                "consequences": "Post-op seizures",
                "prevention": "Prophylactic anti-epileptics",
                "reversibility": "manageable with medication"
            }
        ],
        
        "recoveryPrognosis": {
            "neuroplasticity": {
                "potential": "HIGH" if patient_age < 40 else "MODERATE",
                "factors": [f"Age {patient_age}", "Rehabilitation intensity"],
                "timeline": "6-12 months for maximum recovery"
            },
            "rehabilitation": {
                "required": True,
                "types": ["Physical therapy", "Cognitive rehab", "Speech therapy"],
                "duration": "6-12 months",
                "expectedImprovement": "60-80%"
            },
            "longTermOutcome": {
                "bestCase": "Near-complete recovery with intensive rehab",
                "worstCase": "Permanent moderate deficits",
                "mostLikely": "Partial recovery to 70-80% function"
            }
        },
        
        "recommendations": [
            f"Patient age {patient_age} {'favorable' if patient_age < 50 else 'consider carefully'} for recovery",
            "Awake craniotomy with brain mapping recommended",
            "Intensive rehabilitation starting immediately post-op",
            "Anti-epileptic prophylaxis for 6-12 months"
        ]
    }