#!/bin/bash
# EliteContent Backend Startup Script
# This script activates the virtual environment and starts the backend server

cd "$(dirname "$0")"
source venv/bin/activate
uvicorn main:app --reload --port 8000
