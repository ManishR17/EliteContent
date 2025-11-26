# EliteContent Platform

EliteContent is an AI-powered content creation platform that generates professional resumes, documents, research papers, and creative writing.

## Project Structure

-   **`frontend/`**: Angular 21 application (UI)
-   **`backend/`**: FastAPI application (API)

## Getting Started

### Prerequisites
-   Node.js 20+
-   Python 3.11+

### Frontend Setup
1.  Navigate to `frontend/`:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start development server:
    ```bash
    npm start
    ```
    Access at `http://localhost:4200`

### Backend Setup
1.  Navigate to `backend/`:
    ```bash
    cd backend
    ```
2.  Create virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Start server:
    ```bash
    uvicorn main:app --reload
    ```
    Access at `http://localhost:8000`
    Docs at `http://localhost:8000/docs`

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.
