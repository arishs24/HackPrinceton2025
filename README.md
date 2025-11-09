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
neurosim/
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
