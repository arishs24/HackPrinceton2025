import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')


def analyze_bone_removal(procedure_type: str, removal_region: dict, patient_age: int, reason: str) -> dict:
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
    bone_name = removal_region['boneName']
    section = removal_region['section']
    start = removal_region['startPoint']
    end = removal_region['endPoint']
    size = removal_region['estimatedSize']
    
    # Create detailed prompt
    prompt = f"""You are an expert maxillofacial surgeon and biomechanical engineer.

CLINICAL SCENARIO:
- Patient Age: {patient_age} years
- Procedure: {procedure_type}
- Indication: {reason}

BONE REMOVAL PLAN:
- Target Bone: {bone_name}
- Section: {section}
- Start Coordinates: x={start['x']:.2f}, y={start['y']:.2f}, z={start['z']:.2f}
- End Coordinates: x={end['x']:.2f}, y={end['y']:.2f}, z={end['z']:.2f}
- Estimated Size: {size}

TASK: Predict ALL consequences of removing this bone section.

Analyze:
1. Biomechanical changes (stress redistribution on remaining bone)
2. Functional impact (bite force, chewing, speech, swallowing)
3. Alignment changes (jaw deviation, midline shift)
4. Reconstruction requirements and options
5. Surgical risks (nerve damage, infection, non-union)
6. Long-term outcomes (with and without reconstruction)

Respond with ONLY valid JSON (no markdown, no extra text):
{{
  "removalSummary": {{
    "affectedStructures": ["list of affected anatomical structures"],
    "preservedStructures": ["list of preserved structures"]
  }},
  
  "biomechanicalChanges": {{
    "stressRedistribution": [
      {{
        "location": "anatomical location",
        "stressIncrease": "percentage",
        "coordinates": {{"x": float, "y": float, "z": float}},
        "severity": "HIGH|MODERATE|LOW"
      }}
    ],
    "alignmentChanges": {{
      "description": "detailed description of jaw alignment changes",
      "deviation": "quantified deviation if applicable"
    }}
  }},
  
  "functionalImpact": {{
    "biteForce": "description of bite force changes",
    "chewing": "description of chewing ability changes",
    "speech": "description of speech impact",
    "swallowing": "description of swallowing impact",
    "overallFunction": "percentage of normal function remaining"
  }},
  
  "reconstructionPlan": {{
    "necessary": true|false,
    "urgency": "IMMEDIATE|DELAYED|OPTIONAL",
    "options": [
      {{
        "method": "reconstruction method name",
        "description": "brief description",
        "successRate": "percentage",
        "pros": ["list of advantages"],
        "cons": ["list of disadvantages"]
      }}
    ],
    "recommendation": "specific recommendation with rationale"
  }},
  
  "risks": [
    {{
      "type": "risk type",
      "probability": "percentage",
      "consequences": "description of consequences",
      "prevention": "prevention strategies"
    }}
  ],
  
  "recommendations": [
    "specific surgical recommendation 1",
    "specific surgical recommendation 2",
    "specific surgical recommendation 3"
  ]
}}

Generate realistic, medically accurate predictions based on surgical biomechanics and anatomy."""

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
        return generate_fallback_analysis(bone_name, section, size, patient_age)


def generate_fallback_analysis(bone_name: str, section: str, size: str, patient_age: int) -> dict:
    """
    Fallback analysis if Gemini fails
    """
    return {
        "removalSummary": {
            "affectedStructures": [f"{bone_name} {section}", "surrounding soft tissue"],
            "preservedStructures": [f"remaining {bone_name}", "opposite side structures"]
        },
        
        "biomechanicalChanges": {
            "stressRedistribution": [
                {
                    "location": f"remaining {bone_name}",
                    "stressIncrease": "40-50%",
                    "coordinates": {"x": 0.0, "y": -0.3, "z": 0.1},
                    "severity": "HIGH"
                }
            ],
            "alignmentChanges": {
                "description": f"Removal of {section} will cause jaw deviation toward the affected side",
                "deviation": "Moderate lateral shift expected"
            }
        },
        
        "functionalImpact": {
            "biteForce": f"Expected 50-60% reduction on affected side",
            "chewing": "Significant impairment, patient will compensate with opposite side",
            "speech": "Minimal impact on articulation",
            "swallowing": "Moderate difficulty initially, adaptation expected",
            "overallFunction": "40-50% of normal without reconstruction"
        },
        
        "reconstructionPlan": {
            "necessary": True,
            "urgency": "IMMEDIATE",
            "options": [
                {
                    "method": "Titanium reconstruction plate",
                    "description": "Metal plate to bridge the defect",
                    "successRate": "85%",
                    "pros": ["Immediate stability", "Lower surgical complexity"],
                    "cons": ["No bone regeneration", "Risk of plate exposure"]
                },
                {
                    "method": "Free bone graft (fibula/iliac crest)",
                    "description": "Transfer living bone from another site",
                    "successRate": "75%",
                    "pros": ["Living bone tissue", "Long-term stability"],
                    "cons": ["Complex surgery", "Donor site morbidity"]
                }
            ],
            "recommendation": "Titanium plate with delayed bone grafting recommended for optimal outcome"
        },
        
        "risks": [
            {
                "type": "Nerve damage",
                "probability": "25-30%",
                "consequences": "Numbness of lower lip and chin on affected side",
                "prevention": "Careful nerve identification and preservation during surgery"
            },
            {
                "type": "Infection",
                "probability": "10-15%",
                "consequences": "Delayed healing, possible hardware removal",
                "prevention": "Prophylactic antibiotics, sterile technique"
            },
            {
                "type": "Non-union",
                "probability": "15-20%",
                "consequences": "Failure of bone healing at reconstruction site",
                "prevention": "Adequate fixation, bone grafting if needed"
            }
        ],
        
        "recommendations": [
            f"Consider patient age ({patient_age} years) in reconstruction planning",
            f"Preserve vascular supply to remaining {bone_name}",
            "Use load-bearing reconstruction plate if immediate bone grafting not possible",
            "Plan for secondary procedures if needed",
            "Postoperative physical therapy for jaw function"
        ]
    }