# AI ATS Resume Writer - Quick Setup Guide

## Prerequisites
- Python 3.8+
- Node.js 16+
- API key from Anthropic (Claude) or OpenAI

## Installation Steps

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your API key
# For Claude:
# AI_SERVICE=claude
# ANTHROPIC_API_KEY=sk-ant-your-key-here
#
# For OpenAI:
# AI_SERVICE=openai
# OPENAI_API_KEY=sk-your-key-here
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already done)
npm install
```

### 3. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 4. Access the Application

Open your browser and go to: `http://localhost:55909`

Navigate to the Resume feature and start generating ATS-optimized resumes!

## Getting API Keys

### Claude (Anthropic)
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new key
5. Copy and paste into `.env`

### OpenAI
1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new key
5. Copy and paste into `.env`

## Configuration

The AI service can be configured in `.env`:

```bash
AI_SERVICE=claude  # or openai
MAX_TOKENS=4000
TEMPERATURE=0.7
```

## Troubleshooting

**Backend won't start:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version`

**AI errors:**
- Verify API key is set in `.env`
- Check API service setting matches your key type
- Ensure API account has credits

**File upload fails:**
- Verify `python-multipart` is installed
- Check file is PDF or DOCX format
- File size should be under 10MB

## Support

For issues or questions, check the full walkthrough.md document.
