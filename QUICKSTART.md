# NeuroSim Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Clone and Navigate
```bash
cd HackPrinceton2025
```

### Step 2: Start Backend (Terminal 1)

```bash
# Navigate to backend
cd backend

# Create virtual environment (first time only)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies (first time only)
pip install -r requirements.txt

# Add your Gemini API key to .env file
# Edit backend/.env and add: GEMINI_API_KEY=your_key_here

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend will run at:** `http://localhost:8000`

### Step 3: Start Frontend (Terminal 2)

```bash
# Navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install --legacy-peer-deps

# Start development server
npm run dev
```

**Frontend will run at:** `http://localhost:5173`

### Step 4: Use the App

1. Open browser to `http://localhost:5173`
2. Click **"Load Sample Brain Scan"**
3. Click **"Remove Tumor & Simulate"**
4. View 3D visualization and AI insights!

## 📝 API Key Setup

### Get Google Gemini API Key (FREE)

1. Go to [Google AI Studio](https://ai.google.dev/)
2. Click "Get API Key"
3. Copy your key
4. Add to `backend/.env`:
   ```
   GEMINI_API_KEY=your_actual_key_here
   ```

**Note:** Snowflake is optional for demo - the app will use mock data if not configured.

## 🔍 Troubleshooting

### Backend Issues

**Port already in use?**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```
Then update frontend `.env`:
```
VITE_API_BASE_URL=http://localhost:8001/api
```

**Import errors?**
Make sure you're in the virtual environment:
```bash
which python  # Should show path to venv/bin/python
```

### Frontend Issues

**Dependency conflicts?**
```bash
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

**Port 5173 in use?**
Vite will automatically use next available port (5174, 5175, etc.)

## 🎯 Demo Flow

1. **Load Sample** → See 3D brain with tumor (red region)
2. **Simulate** → Watch tissue deform after tumor removal
3. **View Heatmap** → Blue = low stress, Red = high stress
4. **Read Insights** → Google Gemini explains results
5. **Compare** → Before/After side-by-side view

## 🛠️ Development Mode

Both servers run with hot reload:
- **Backend**: Edit Python files → Auto-reloads
- **Frontend**: Edit React files → Instant updates

## 📊 API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

## 🐛 Common Errors

**"Failed to generate insights"**
- Check Gemini API key in `.env`
- Ensure backend can access internet

**3D viewer not loading**
- Check browser console for errors
- Try clearing cache and reload

**Upload not working**
- Check `backend/uploads` folder exists
- Verify file format is supported

## 💡 Tips

- Use **Chrome or Firefox** for best 3D performance
- **Sample data** loads instantly (no upload needed)
- **Gemini insights** may take 3-5 seconds to generate
- **3D view**: Click and drag to rotate, scroll to zoom

---

Need help? Check the main [README.md](README.md) for detailed documentation!
