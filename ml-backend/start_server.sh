#!/bin/bash
echo "Starting ml-backend server on port 8001..."
cd "$(dirname "$0")"
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001

