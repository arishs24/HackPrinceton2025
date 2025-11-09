# 🧠 Synovia: AI-Driven Brain Surgery Simulation Platform  
### *Project: Synovia*  
**Built at HackPrinceton 2025

**Synovia** is an advanced **AI and physics-based surgical simulation platform** that converts raw MRI and CT brain scans into **interactive 3D biomechanical models** for neurosurgical planning.  
By merging **machine learning segmentation**, **finite element modeling**, and **real-time 3D rendering**, Synovia allows surgeons to visualize, simulate, and predict the impact of brain tumor resections before performing surgery.  

---

## 🌟 Core Features  

### 🧬 AI-Powered 3D Segmentation  
- Converts 2D MRI or CT DICOM files into volumetric 3D meshes using a hybrid CNN and transformer segmentation model trained on GPU clusters.  
- Identifies key neuroanatomical structures including the skull, grey matter, white matter, ventricles, and tumor.  
- Trained and optimized on **DigitalOcean Gradient GPU Droplets** with **A100 and H100 architectures**, using mixed precision and ONNX export for real-time inference.  

### 🔬 Physics-Based Biomechanical Simulation  
- Implements **nonlinear finite element analysis (FEA)** and **continuum mechanics solvers** to simulate realistic tissue deformation after tumor removal.  
- Models **viscoelastic and anisotropic properties** of brain matter to accurately predict displacement and stress patterns.  
- Computes full tensor fields for displacement, strain, and von Mises stress using **NumPy**, **SciPy**, and **PyVista** accelerated by **CUDA** on DigitalOcean GPUs.  
- Integrates **physics-informed neural networks (PINNs)** to combine numerical solvers with data-driven predictions for faster simulation performance.  

### ⚡ Real-Time 3D Visualization  
- Developed using **React Three Fiber** and **Three.js** for high-fidelity, interactive 3D visualization.  
- Displays live **stress tensor heatmaps** and mechanical gradients synchronized with backend simulation output.  
- Custom GLSL shaders provide material translucency, cortical depth, and realistic lighting for a medical-grade rendering experience.  

### 🤖 Gemini-Driven Surgical Reasoning  
- Integrated with **Google Gemini 2.0 API** for advanced interpretation of biomechanical and anatomical data.  
- Produces both **technical surgical insights** and **patient-friendly summaries** to support clinician decision-making.  
- Generates real-time neurological risk assessments and recovery predictions based on stress propagation patterns.  

### ☁️ Cloud-Native GPU Infrastructure  
- Deployed using **DigitalOcean’s Gradient AI Cloud** with Kubernetes orchestration and GPU-backed Droplets.  
- Distributes heavy compute loads across multiple GPUs for parallel tensor calculations and reduced FEA simulation time.  
- Stores MRI and mesh data on persistent object storage for rapid retrieval and post-analysis.  
- Automated CI/CD pipelines deploy containerized FastAPI microservices to DigitalOcean’s App Platform.  

### 🎨 Stress Heatmap and Analytics  
- Visualizes principal stress directions, displacement vectors, and strain energy in real time.  
- Color-coded 3D overlays help identify critical regions under mechanical stress before surgery.  

---

## 🧩 Tech Stack  

### **Frontend**
- React 18 + TypeScript  
- Three.js + React Three Fiber  
- TailwindCSS for responsive medical UI  
- Zustand for state management  
- Axios for API communication  
- Vite for optimized builds  

### **Backend**
- FastAPI (Python 3.10+)  
- PyTorch + TensorFlow for deep learning segmentation  
- NumPy, SciPy, PyVista for FEA and numerical modeling  
- Google Gemini API for AI-driven neurological reasoning  
- Pydantic for schema validation  
- Docker and Kubernetes for scalable deployment on DigitalOcean GPU clusters  

---

## ⚙️ Quick Start  

### **Backend Setup**
```bash
cd ml-backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
Create an .env file:

ini
Copy code
GEMINI_API_KEY=your_gemini_api_key
CORS_ORIGINS=http://localhost:5173
Run the server:

bash
Copy code
uvicorn main:app --reload --host 0.0.0.0 --port 8001
Frontend Setup
bash
Copy code
cd frontend
npm install --legacy-peer-deps
npm run dev
Open in your browser: http://localhost:5173

🧠 System Architecture
Data Ingestion: MRI and CT scans are uploaded and converted into normalized voxel grids.

Segmentation: Deep CNN and transformer models process data into high-resolution 3D meshes.

Simulation: The FEA solver computes tissue stress, strain, and deformation patterns in GPU-accelerated environments.

AI Interpretation: Gemini analyzes biomechanical tensors and generates neurological risk insights.

Visualization: Interactive 3D rendering visualizes structural deformation and highlights regions under critical load.

Cloud Deployment: All inference and simulations run on DigitalOcean GPU infrastructure using Kubernetes scaling.

🚀 What Makes Synovia Unique
True AI-Physics Integration: Combines real physics with machine learning-driven insights.

GPU-Accelerated FEA: Complete biomechanical simulation powered by multi-GPU compute nodes.

Physics-Informed ML: PINNs bridge data and differential equations for ultra-fast mechanical predictions.

AI Interprets Physics: Gemini converts complex tensor data into readable insights for surgeons.

Built in under 48 hours using DigitalOcean’s GPU infrastructure, advanced ML, and physics-based modeling.

