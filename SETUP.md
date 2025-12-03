# EliteContent - Setup Guide

## Prerequisites
- Python 3.9+
- Node.js 18+
- API key from Anthropic (Claude)

## Quick Start (Single Port Deployment)

The application is configured to run both frontend and backend on a single port (8000).

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Configure .env with your API key
# AI_SERVICE=claude
# ANTHROPIC_API_KEY=sk-ant-your-key
# CLAUDE_MODEL=claude-3-haiku-20240307
```

### 2. Frontend Build

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Build the Angular application
npm run build
```

### 3. Run the Application

You only need to run the backend server. It will serve the built frontend automatically.

```bash
# From backend directory
./venv/bin/uvicorn main:app --reload --port 8000
```

### 4. Access the Application

Open your browser and go to: **http://localhost:8000**

## Configuration

The AI service is configured in `backend/.env`.

**Important:** For this API key tier, use the Haiku model:
```bash
AI_SERVICE=claude
CLAUDE_MODEL=claude-3-haiku-20240307
MAX_TOKENS=4000
TEMPERATURE=0.7
```

## Troubleshooting

**AI Errors (404/500):**
- Ensure `CLAUDE_MODEL` is set to `claude-3-haiku-20240307` in `.env`.
- Verify your API key in `.env`.
- Restart the server after changing `.env`.

**Frontend not loading:**
- Ensure you ran `npm run build` in the frontend directory.
- Check if `backend/frontend/dist/elitecontent-ui/browser` exists.
- Check browser console for errors.

**Server won't start:**
- Check if port 8000 is in use: `lsof -ti:8000 | xargs kill -9`
- Verify Python dependencies: `pip install -r requirements.txt`
