<<<<<<< HEAD
# PreSurg.AI

> **AI-Powered Pre-Surgical Simulation for Bone Removal Planning**
> 
> Reimagining [AlgoSurg (YC W18)](https://www.ycombinator.com/companies/algosurg-inc) with AI at its core.

Built at **HackPrinceton Fall 2025** | YC Company Challenge

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
=======
# NeuroSim: AI-Driven Brain Surgery Simulation Platform

![NeuroSim](https://img.shields.io/badge/Built%20for-HackPrinceton%202025-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![React](https://img.shields.io/badge/React-18+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

**name** is a cutting-edge web application that transforms brain MRI/CT scans into interactive biomechanical simulations for surgical planning. Using AI-powered segmentation, real-time 3D visualization, and finite element analysis, [__] helps surgeons predict tissue deformation and assess risks before performing tumor resection surgery.

## 🌟 Features

- **🧠 AI-Powered 3D Segmentation**: Automatic identification of brain structures (skull, white matter, grey matter, tumor)
- **⚡ Interactive 3D Visualization**: Real-time brain rendering with Three.js and React Three Fiber
- **🔬 Biomechanical FEA Simulation**: Predict tissue deformation and stress distribution after tumor removal
- **💡 Google Gemini Integration**: AI-generated surgical insights in both technical and patient-friendly language
- **📊 Snowflake Data Analytics**: Store and retrieve simulation data for case comparison and statistical analysis
- **🎨 Stress Heatmap Visualization**: Color-coded display of tissue stress levels
- **📱 Responsive Design**: Modern, medical-grade UI with TailwindCSS

## 🏗️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **Three.js** + React Three Fiber for 3D rendering
- **TailwindCSS** for styling
- **Zustand** for state management
- **Axios** for API communication
- **Vite** for fast development

### Backend
- **FastAPI** (Python 3.10+)
- **NumPy & SciPy** for biomechanical calculations
- **PyVista** for mesh generation
- **Google Gemini API** for AI insights
- **Snowflake** for data storage
- **Uvicorn** ASGI server

## 📦 Project Structure

```
NeuroSim/
├── frontend/                 # React + TypeScript frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── BrainViewer3D.tsx
│   │   │   ├── FileUpload.tsx
│   │   │   ├── SimulationControls.tsx
│   │   │   ├── GeminiInsights.tsx
│   │   │   └── ComparisonView.tsx
│   │   ├── hooks/           # Custom React hooks
│   │   ├── utils/           # API utilities
│   │   ├── types/           # TypeScript types
│   │   └── App.tsx
│   └── package.json
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/        # API endpoints
│   │   ├── services/       # Business logic
│   │   ├── models/         # Pydantic schemas
│   │   └── utils/
│   ├── requirements.txt
│   └── .env.example
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** and npm
- **Google Gemini API Key** ([Get one here](https://ai.google.dev/))
- **Snowflake Account** (optional for demo)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your API keys:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   SNOWFLAKE_ACCOUNT=your_account (optional)
   SNOWFLAKE_USER=your_user (optional)
   SNOWFLAKE_PASSWORD=your_password (optional)
   CORS_ORIGINS=http://localhost:5173
   ```

5. **Run the backend server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   Backend will be available at: `http://localhost:8000`

   API docs at: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory** (in a new terminal):
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install --legacy-peer-deps
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```

4. **Run the development server**:
   ```bash
   npm run dev
   ```

   Frontend will be available at: `http://localhost:5173`

## 📖 Usage Guide

### Quick Demo

1. **Open the application** at `http://localhost:5173`

2. **Click "Load Sample Brain Scan"** to load pre-segmented brain data

3. **View the 3D brain** with color-coded regions:
   - 🤍 White: Skull
   - 🟡 Off-white: White matter
   - 🔵 Grey: Grey matter
   - 🔴 Red: Tumor

4. **Click "Remove Tumor & Simulate"** to run FEA simulation

5. **View results**:
   - Before/After comparison with 3D deformation
   - Stress heatmap (blue = low, red = high)
   - Biomechanical metrics
   - AI-generated insights from Google Gemini

### Upload Custom Data

1. **Drag and drop** or click to upload brain scan files:
   - NIfTI (`.nii`, `.nii.gz`)
   - DICOM (`.dcm`)
   - Images (`.png`, `.jpg`)

2. **Automatic segmentation** will identify brain structures

3. **Run simulation** and analyze results

## 🔧 API Endpoints

### Upload
```http
POST /api/upload
Content-Type: multipart/form-data

Response: { "case_id": "uuid", "filename": "scan.nii", "status": "uploaded" }
```

### Segmentation
```http
POST /api/segment
Content-Type: application/json

{
  "case_id": "uuid"
}

Response: { "mesh_data": {...}, "label_names": {...}, "case_id": "uuid" }
```

### Simulation
```http
POST /api/simulate
Content-Type: application/json

{
  "case_id": "uuid",
  "remove_region": "tumor",
  "skull_opening_size": 5.0
}

Response: { "deformed_mesh": {...}, "metrics": {...}, "heatmap_data": [...] }
```

### Gemini Insights
```http
POST /api/gemini/analyze
Content-Type: application/json

{
  "simulation_results": {...}
}

Response: { "technical_summary": "...", "patient_summary": "..." }
```

### Snowflake
```http
POST /api/snowflake/save
GET  /api/snowflake/similar/{tumor_location}?limit=5
```

## 🧪 Development

### Run Tests
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

### Build for Production
```bash
# Frontend
cd frontend
npm run build

# Backend - use production ASGI server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🎯 Key Implementation Details

### Biomechanical Simulation

The FEA simulation uses a simplified distance-based deformation model:

```python
displacement = max_displacement * exp(-distance_from_tumor / decay_factor)
stress = displacement_magnitude * stress_factor
```

This approach provides fast, interactive results suitable for surgical planning. For production use, consider implementing full finite element analysis with proper material properties.

### Mock Data Strategy

For hackathon speed, the app uses:
- **Mock brain mesh**: Generated sphere with noise for brain-like appearance
- **Mock segmentation**: Pre-labeled regions based on spatial position
- **Mock Snowflake**: In-memory storage (replace with real connector)

### Google Gemini Prompts

Gemini receives simulation metrics and generates two summaries:
1. **Technical**: For surgical team with biomechanical analysis
2. **Patient-friendly**: Simple language explanations

Fallback responses are included if API fails.

## 🏆 Sponsor Integration

### Google Gemini
- Real-time AI analysis of surgical simulations
- Dual-mode explanations (technical + patient-friendly)
- Conversational follow-up questions support

### Snowflake
- Simulation data persistence
- Similar case retrieval based on tumor characteristics
- Statistical analysis across historical cases
- Foundation for RAG-enhanced Gemini insights

## 🚧 Roadmap

- [ ] Real MONAI-based brain segmentation
- [ ] Full FEA with material properties (Young's modulus, Poisson's ratio)
- [ ] WebGL 2.0 optimization for larger meshes
- [ ] Multi-user collaboration features
- [ ] VR support for immersive surgical planning
- [ ] Integration with hospital PACS systems

## 📄 License

MIT License - see LICENSE file for details

## 👥 Team

Built for HackPrinceton 2025

## 🙏 Acknowledgments

- **Google Gemini** for AI-powered insights
- **Snowflake** for data intelligence
- **Three.js community** for 3D visualization tools
- **FastAPI** for modern Python API framework

---
>>>>>>> main
