# Contributing to EliteContent

Thank you for your interest in contributing to EliteContent! We welcome contributions from everyone.

## Development Workflow

We use a **Git Branching Strategy** to ensure code stability:

1.  **`main`**: This is the protected branch for stable, production-ready code. Direct commits are restricted.
2.  **`dev`**: This is the active development branch. All new features and fixes should be merged here first.
3.  **Feature Branches**: Create a new branch for each feature or bug fix (e.g., `feature/email-writer`, `fix/login-bug`).

### Process

1.  Clone the repository.
2.  Checkout the `dev` branch: `git checkout dev`
3.  Create a new branch: `git checkout -b feature/your-feature-name`
4.  Make your changes and commit them.
5.  Push your branch to the remote repository.
6.  Open a Pull Request (PR) targeting the `dev` branch.
7.  Once approved and merged into `dev`, it will eventually be merged into `main` for release.

## Project Structure

-   **`frontend/`**: Angular application (UI).
-   **`backend/`**: FastAPI application (API).

## Setup Instructions

### Frontend
1.  Navigate to `frontend/`: `cd frontend`
2.  Install dependencies: `npm install`
3.  Start development server: `npm start`

### Backend
1.  Navigate to `backend/`: `cd backend`
2.  Create virtual environment: `python -m venv .venv`
3.  Activate virtual environment: `source .venv/bin/activate` (or Windows equivalent)
4.  Install dependencies: `pip install -r requirements.txt`
5.  Start server: `uvicorn main:app --reload`
