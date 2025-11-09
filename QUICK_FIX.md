# Quick Fix: Connection Refused Error

## The Problem
The error `ERR_CONNECTION_REFUSED` means the backend server isn't running. The frontend is trying to connect to `http://localhost:8001/api` but can't find the server.

## Solution: Start the Backend

### Step 1: Open a Terminal/Command Prompt

### Step 2: Navigate to ml-backend folder
```bash
cd ml-backend
```

### Step 3: Install dependencies (if needed)
```bash
pip install -r requirements.txt
```

### Step 4: Start the server
```bash
# Windows PowerShell/CMD
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001

# Or if you have the run.py file
python run.py
```

### Step 5: Verify it's running
You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 6: Test in browser
Open: http://localhost:8001/api/health

You should see: `{"api":"healthy","gemini":"connected","organ":"brain"}`

### Step 7: Try uploading again
Now go back to your frontend and try uploading the .nii.gz file again.

## Alternative: Use Different Port

If port 8001 is already in use:

1. Start backend on different port:
   ```bash
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8002
   ```

2. Create `.env` file in `frontend/` folder:
   ```
   VITE_API_BASE_URL=http://localhost:8002/api
   ```

3. Restart frontend dev server

## Troubleshooting

### "Module not found" errors?
Make sure you're in the `ml-backend` directory and dependencies are installed:
```bash
cd ml-backend
pip install -r requirements.txt
```

### Port already in use?
```bash
# Windows - Find what's using port 8001
netstat -ano | findstr :8001

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Still not working?
1. Check that the backend terminal shows "Uvicorn running on..."
2. Try accessing http://localhost:8001 in your browser
3. Check Windows Firewall isn't blocking the connection
4. Make sure no antivirus is blocking port 8001

