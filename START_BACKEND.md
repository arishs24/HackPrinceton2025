# How to Start the Backend

## Quick Start

1. **Navigate to ml-backend directory**:
   ```bash
   cd ml-backend
   ```

2. **Install dependencies** (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server**:
   ```bash
   # Option 1: Using uvicorn directly
   uvicorn main:app --reload --host 0.0.0.0 --port 8001
   
   # Option 2: Using the run script
   python run.py
   ```

4. **Verify it's running**:
   - Open browser: http://localhost:8001
   - Should see: `{"status":"online","service":"PreSurg.AI Brain Surgery ML API",...}`
   - Or check: http://localhost:8001/api/health

## Troubleshooting

### Port 8001 already in use?
```bash
# Find what's using the port (Windows)
netstat -ano | findstr :8001

# Or use a different port
uvicorn main:app --reload --host 0.0.0.0 --port 8002
```

Then update frontend `.env` file:
```
VITE_API_BASE_URL=http://localhost:8002/api
```

### Connection Refused Error?
1. Make sure the backend is running (check terminal for "Uvicorn running on...")
2. Verify the port matches (default: 8001)
3. Check firewall settings
4. Try accessing http://localhost:8001/api/health in browser

### Import Errors?
Make sure you're in the ml-backend directory and all dependencies are installed:
```bash
cd ml-backend
pip install -r requirements.txt
```

## Expected Output

When the server starts, you should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

