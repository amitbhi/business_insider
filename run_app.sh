#!/bin/bash

# Navigate to the project directory securely
DIR="/home/amit/apps/business_insider"
cd "$DIR"

echo "==============================================="
echo "🧠 BUSINESS INSIDER INTELLIGENCE ENGINE "
echo "==============================================="

echo "Cleaning up any old processes..."
fuser -k 8000/tcp 2>/dev/null
fuser -k 8503/tcp 2>/dev/null
sleep 2

# Activate the virtual environment
source venv/bin/activate

echo "Initializing local intelligence models..."

# Spin up FastAPI Backend layer
echo "-> Starting Backend Pipeline (Port 8000)..."
uvicorn backend.main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

# Wait 3 seconds to ensure FastAPI is fully booted
sleep 3

# Spin up Streamlit Frontend GUI
echo "-> Starting Visual Dashboard..."
streamlit run frontend/app.py --server.port=8503 &
FRONTEND_PID=$!

# Give streamlit a second to boot, then explicitly open the browser
sleep 3
python -m webbrowser "http://localhost:8503" 2>/dev/null

# Ensure shutdown is graceful across all modules
cleanup() {
    echo "Cleaning up Intelligence Engine processes..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM EXIT

# Block output and hold script until interrupted
wait $FRONTEND_PID
