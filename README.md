# Synovia: AI-Driven Brain Surgery Simulation Platform

![NeuroSim](https://img.shields.io/badge/Built%20for-HackPrinceton%202025-blue)

Synovia is a cutting-edge web application that transforms brain MRI/CT scans into interactive biomechanical simulations for surgical planning. Using AI-powered segmentation, real-time 3D visualization, and finite element analysis, Synovia helps surgeons predict tissue deformation and assess risks before performing tumor resection surgery.

## 🌟 Features
- **🧠 AI-Powered 3D Segmentation**: Automatic identification of brain structures (skull, white matter, grey matter, tumor)
- **⚡ Interactive 3D Visualization**: Real-time brain rendering with Three.js and React Three Fiber
- **🔬 Biomechanical FEA Simulation: Utilize advanced finite element analysis (FEA) with patient-specific anatomical models to simulate post-tumor-removal tissue deformation, applying continuum mechanics, constitutive material models, and numerical solvers to predict stress-strain distributions and optimize surgical outcomes.
- **💡 Google Gemini Integration**: AI-generated surgical insights in both technical and patient-friendly language
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
- **Uvicorn** ASGI server


## Quick Start

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

---
