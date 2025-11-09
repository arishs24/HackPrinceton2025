@echo off
echo Starting ml-backend server on port 8001...
echo.
cd /d %~dp0
echo Current directory: %CD%
echo.
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
pause

