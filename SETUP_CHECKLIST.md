# NeuroSim Setup Checklist ✅

## Pre-Flight Checklist

Use this checklist to ensure everything is ready for your demo.

### 1. System Requirements ✓

- [ ] Python 3.10 or higher installed
  ```bash
  python3 --version
  ```

- [ ] Node.js 18 or higher installed
  ```bash
  node --version
  ```

- [ ] npm installed
  ```bash
  npm --version
  ```

### 2. API Keys 🔑

- [ ] Google Gemini API Key obtained
  - Go to: https://ai.google.dev/
  - Create API key (it's free!)
  - Save it somewhere safe

- [ ] Snowflake credentials (OPTIONAL for demo)
  - Can skip for hackathon demo
  - App works with mock data

### 3. Backend Setup 🐍

- [ ] Navigate to backend directory
  ```bash
  cd backend
  ```

- [ ] Create virtual environment
  ```bash
  python3 -m venv venv
  ```

- [ ] Activate virtual environment
  ```bash
  # macOS/Linux:
  source venv/bin/activate

  # Windows:
  venv\Scripts\activate
  ```

- [ ] Install dependencies
  ```bash
  pip install -r requirements.txt
  ```
  ⏱️ This takes 2-3 minutes

- [ ] Configure environment variables
  ```bash
  # .env file should already exist
  # Add your Gemini API key:
  nano .env  # or use any text editor
  ```

  Edit this line:
  ```
  GEMINI_API_KEY=your_actual_key_here
  ```

- [ ] Test imports
  ```bash
  cd ..
  python test_imports.py
  ```
  Should show: ✅ All imports successful!

- [ ] Start backend server
  ```bash
  cd backend
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
  ```

- [ ] Verify backend is running
  - Open: http://localhost:8000
  - Should see: `{"message": "Welcome to NeuroSim API"}`
  - API docs: http://localhost:8000/docs

### 4. Frontend Setup ⚛️

**Open a NEW terminal** (keep backend running)

- [ ] Navigate to frontend directory
  ```bash
  cd frontend
  ```

- [ ] Install dependencies
  ```bash
  npm install --legacy-peer-deps
  ```
  ⏱️ This takes 3-5 minutes

- [ ] Verify .env file exists
  ```bash
  cat .env
  ```
  Should show: `VITE_API_BASE_URL=http://localhost:8000/api`

- [ ] Start frontend dev server
  ```bash
  npm run dev
  ```

- [ ] Verify frontend is running
  - Open: http://localhost:5173
  - Should see: NeuroSim landing page

### 5. Quick Test Run 🧪

- [ ] In browser at http://localhost:5173
  - [ ] Click "Load Sample Brain Scan"
  - [ ] 3D brain appears (4 color-coded regions)
  - [ ] Click "Remove Tumor & Simulate"
  - [ ] Before/After comparison appears
  - [ ] Stress heatmap shows (blue to red)
  - [ ] Metrics panel shows numbers
  - [ ] Gemini insights load (may take 3-5 seconds)
  - [ ] Both "For Surgeons" and "For Patients" tabs work

### 6. Troubleshooting Common Issues 🔧

#### Backend won't start
- [ ] Check Python version (must be 3.10+)
- [ ] Verify virtual environment is activated
- [ ] Try `pip install --upgrade pip`
- [ ] Check port 8000 isn't already in use

#### Frontend won't start
- [ ] Delete `node_modules` and `package-lock.json`
- [ ] Run `npm install --legacy-peer-deps` again
- [ ] Check Node version (must be 18+)

#### 3D viewer shows blank screen
- [ ] Check browser console (F12)
- [ ] Try Chrome or Firefox
- [ ] Verify backend is running and responding

#### Gemini insights fail
- [ ] Verify GEMINI_API_KEY in backend/.env
- [ ] Check backend terminal for error messages
- [ ] Test API key at https://ai.google.dev/
- [ ] Fallback summaries will show if API fails

#### Upload not working
- [ ] Verify `backend/uploads` folder exists
  ```bash
  mkdir -p backend/uploads
  ```

### 7. Demo Preparation 🎬

- [ ] Practice the full workflow 3 times
- [ ] Prepare 30-second introduction
- [ ] Have browser tabs ready:
  - [ ] Frontend (http://localhost:5173)
  - [ ] API docs (http://localhost:8000/docs)
  - [ ] GitHub repo (if you pushed it)

- [ ] Backup plan:
  - [ ] Take screenshots of working app
  - [ ] Record video of full demo
  - [ ] Have explanation ready if live demo fails

### 8. Optional Enhancements ⭐

- [ ] Push code to GitHub
- [ ] Deploy to Vercel (frontend) + Render (backend)
- [ ] Create presentation slides
- [ ] Prepare technical explanation of FEA
- [ ] List future improvements

### 9. Sponsor Prize Checklist 🏆

#### Google Gemini
- [ ] Gemini API clearly visible in demo
- [ ] Show both technical and patient summaries
- [ ] Explain how Gemini makes surgery understandable
- [ ] Mention fallback mechanism

#### Snowflake
- [ ] Explain data storage architecture
- [ ] Show case similarity feature (in API docs)
- [ ] Describe how it enables institutional learning
- [ ] Mention RAG potential

## Final Pre-Demo Checklist ✅

**5 minutes before demo:**

- [ ] Both servers running (backend + frontend)
- [ ] Browser tabs open and ready
- [ ] API key working (test Gemini insights)
- [ ] Demo workflow practiced
- [ ] Backup materials ready
- [ ] Confident smile 😊

## Emergency Quick Reset

If everything breaks:

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

Then reload browser at http://localhost:5173

---

## Success Criteria ✨

You're ready for demo when:
✅ Backend runs without errors
✅ Frontend loads in browser
✅ Sample data loads in < 2 seconds
✅ Simulation runs and shows results
✅ Gemini generates insights
✅ All UI components render correctly
✅ You can explain the tech stack
✅ You can explain sponsor integrations

---

**Good luck! 🚀**
