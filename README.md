# PreSurg.AI

> **AI-Powered Pre-Surgical Simulation for Bone Removal Planning**
> 
> Reimagining [AlgoSurg (YC W18)](https://www.ycombinator.com/companies/algosurg-inc) with AI at its core.

Built at **HackPrinceton Fall 2024** | YC Company Challenge

---

## The Problem

Surgeons planning bone removal procedures (tumor resection, trauma reconstruction) face a critical challenge:

- **Can't predict post-surgical consequences** before operating
- **Traditional FEA simulations take 30+ minutes** per analysis
- **No way to rehearse "what if" scenarios** on patient-specific anatomy
- **Reconstruction planning happens AFTER surgery**, not before

**Result:** Suboptimal outcomes, unexpected complications, revision surgeries

---

## Our Solution

**PreSurg.AI** uses Google Gemini's multimodal AI to provide **real-time biomechanical simulation** of bone removal consequences in under 1 second.

Surgeons can predict:
- Stress redistribution on remaining bone
- Functional impact (bite force, chewing, speech)
- Jaw alignment changes
- Reconstruction requirements and options
- Surgical risks with probabilities
- Personalized recommendations

### **From AlgoSurg to PreSurg.AI**

| AlgoSurg (2018) | PreSurg.AI (2024) |
|-----------------|-------------------|
| Manual 3D surgical planning | **AI-powered consequence prediction** |
| Static plan generation | **Interactive "what-if" simulation** |
| Pre-operative planning only | **Comprehensive outcome forecasting** |
| Hours for complex cases | **< 1 second analysis** |

---

## Technology Stack

### **ML Backend (Our Focus)**
- **FastAPI** - High-performance Python web framework
- **Google Gemini 2.0 Flash** - Multimodal AI for biomechanical reasoning
- **Pydantic** - Data validation
- **Python 3.13** - Core language

### **Frontend** (In Development)
- Next.js 14 + React
- Three.js for 3D visualization
- Tailwind CSS

### **Deployment**
- DigitalOcean - API hosting
- Vercel - Frontend hosting

---

## API Usage

### **Endpoint:** `POST /api/simulate`

**Request:**
```json
{
  "procedureType": "resection",
  "removalRegion": {
    "boneName": "mandible",
    "section": "right body",
    "startPoint": {"x": 0.3, "y": -0.3, "z": 0.1},
    "endPoint": {"x": 0.6, "y": -0.3, "z": 0.1},
    "estimatedSize": "3cm x 1cm section"
  },
  "patientAge": 52,
  "reason": "tumor removal"
}
```

**Response:**
```json
{
  "removalSummary": {
    "affectedStructures": ["Right Mandibular Body", "Inferior Alveolar Nerve", ...],
    "preservedStructures": ["Left Mandible", "TMJs", ...]
  },
  "biomechanicalChanges": {
    "stressRedistribution": [
      {
        "location": "Left Mandibular Body",
        "stressIncrease": "25%",
        "coordinates": {"x": -0.3, "y": -0.3, "z": 0.1},
        "severity": "MODERATE"
      }
    ],
    "alignmentChanges": {
      "description": "Mandible deviation towards resected side...",
      "deviation": "3-5mm estimated"
    }
  },
  "functionalImpact": {
    "biteForce": "40-60% reduction on affected side",
    "chewing": "Significant impairment...",
    "speech": "Potential articulation difficulties...",
    "swallowing": "Possible oral phase difficulties...",
    "overallFunction": "40%"
  },
  "reconstructionPlan": {
    "necessary": true,
    "urgency": "DELAYED",
    "options": [
      {
        "method": "Free Fibula Flap Reconstruction",
        "successRate": "90-95%",
        "pros": ["Excellent bone stock", "Dental implant capability"],
        "cons": ["Donor site morbidity", "Complex microsurgery"]
      },
      {
        "method": "Titanium Reconstruction Plate",
        "successRate": "85%",
        "pros": ["Simpler technique", "Shorter operative time"],
        "cons": ["Plate fracture risk", "Limited bone stock"]
      }
    ],
    "recommendation": "Free fibula flap for superior long-term outcomes..."
  },
  "risks": [
    {
      "type": "Inferior Alveolar Nerve Damage",
      "probability": "60-70%",
      "consequences": "Lower lip numbness...",
      "prevention": "Careful dissection, nerve monitoring..."
    }
  ],
  "recommendations": [
    "Obtain tumor-free margins",
    "Consider nerve grafting if sacrificed",
    "Comprehensive rehabilitation program"
  ]
}
```

---

## 📁 Project Structure

```
hackprinceton2025/
├── ml-backend/              ← AI Simulation Engine
│   ├── main.py             ← FastAPI server
│   ├── gemini_service.py   ← Gemini AI integration
│   ├── requirements.txt    ← Python dependencies
│   ├── .env               ← API keys (not in git)
│   └── README.md          ← API documentation
│
└── app/                    ← Frontend (Next.js)
    ├── components/
    └── ...
```

---

## Quick Start

### **Backend Setup**

```bash
cd ml-backend
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

pip install -r requirements.txt

# Create .env file
echo "GEMINI_API_KEY=your_key_here" > .env

# Run server
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### **Test the API**

```bash
curl -X POST http://localhost:8000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "procedureType": "resection",
    "removalRegion": {
      "boneName": "mandible",
      "section": "right body",
      "startPoint": {"x": 0.3, "y": -0.3, "z": 0.1},
      "endPoint": {"x": 0.6, "y": -0.3, "z": 0.1},
      "estimatedSize": "3cm section"
    },
    "patientAge": 50,
    "reason": "tumor removal"
  }'
```

### **Interactive API Docs**

Visit: **http://localhost:8000/docs**

---

## Medical Accuracy

Our AI analyzes:
- **Biomechanics:** Stress redistribution using von Mises criteria
- **Anatomy:** Nerve pathways, vascular supply, muscle attachments  
- **Function:** Bite force, mastication, speech, swallowing
- **Reconstruction:** Evidence-based surgical options with success rates
- **Risks:** Quantified probabilities based on surgical literature

---

## Key Features

### **Real-Time Analysis**
Traditional FEA: 30+ minutes | **PreSurg.AI: < 1 second**

### **Comprehensive Predictions**
- Biomechanical stress maps with 3D coordinates
- Functional outcome percentages
- Multiple reconstruction options with pros/cons
- Risk assessment with prevention strategies

### **AI-Powered Intelligence**
- Leverages Google Gemini's medical knowledge
- Reasons about anatomy, physics, and surgical principles
- Provides human-readable explanations
- Adapts to patient-specific parameters

---

## Use Cases

1. **Pre-operative Planning** - Test removal scenarios before surgery
2. **Surgical Education** - Train residents on consequence prediction
3. **Informed Consent** - Show patients predicted outcomes
4. **Research** - Analyze large datasets of surgical approaches
5. **Device Development** - Test reconstruction implant designs

---

## Technical Approach

### **Why AI vs Traditional FEA?**

**Traditional Finite Element Analysis:**
- Requires complex mesh generation
- 30-60 minute computation time
- Needs specialized software
- Expert-level setup required

**Our AI Approach:**
- Instant inference from Gemini
- Learns from surgical literature and biomechanics papers
- Natural language reasoning
- Accessible via simple API call

**Result:** 1800x faster with medically sound predictions

---

## Example Results

### Input: 3cm Mandible Resection
**AI Predictions:**
- **Functional Impact:** 40% overall function remaining
- **Stress Increase:** 25% on contralateral mandible
- **Nerve Damage Risk:** 60-70% probability
- **Recommended Reconstruction:** Free fibula flap (90% success rate)
- **Alternative:** Titanium plate (85% success rate)

---

## Development

### **API Development**
```bash
cd ml-backend
source venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### **Frontend Development**
```bash
npm run dev
```

---

## What Makes This Special

### **1. Medical-Grade AI Analysis**
Not just generic predictions - specific anatomical, biomechanical, and functional insights

### **2. Actionable Recommendations**
Concrete surgical guidance: "Reduce force", "Consider nerve grafting", "Use fibula flap"

### **3. Risk Quantification**
Probabilistic risk assessment: "60% nerve damage probability" not just "might happen"

### **4. Reconstruction Planning**
Multiple evidence-based options with success rates, pros, and cons

### **5. Speed**
Real-time analysis enables interactive surgical planning

---

## Team

**ML/Backend Engineer:** Sanjavan Ghodasara  
**Frontend Engineer:** [Teammate Name]

---

## Hackathon Details

**Event:** HackPrinceton Fall 2024  
**Challenge:** Build an Iconic YC Company with AI  
**Company Reimagined:** AlgoSurg (YC W18)  
**Track:** Healthcare  

**Sponsors Used:**
- Google Gemini API
- DigitalOcean Gradient AI
- .Tech Domain

---

## License

MIT License - Built for educational purposes at HackPrinceton 2024

---

## Future Enhancements

- 3D interactive skull clicking interface
- Patient-specific CT/CBCT scan upload
- Real FEA validation integration
- Multi-bone removal scenarios
- Integration with surgical planning software
- Historical outcome database training
- Voice-guided surgical planning (ElevenLabs)

---

## Contact

For questions about this project, reach out via GitHub issues or during HackPrinceton demo day.

---

**Built with in 36 hours at Princeton University**