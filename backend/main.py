from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers import resume, document, email, social, creative, research, dashboard, auth
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize rate limiter
rate_limit_enabled = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
rate_limit_per_min = os.getenv("RATE_LIMIT_PER_MINUTE", "60")

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{rate_limit_per_min}/minute"] if rate_limit_enabled else []
)

app = FastAPI(
    title="EliteContent API",
    description="Backend for EliteContent AI Platform - Professional content generation with AI, RAG, and MCP",
    version="3.0.0"
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.on_event("startup")
async def startup():
    from database import engine, Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for single-port deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to Angular build directory
FRONTEND_DIR = Path(__file__).parent.parent / "frontend" / "dist" / "elitecontent-ui" / "browser"

# Include routers for all features
app.include_router(resume.router, prefix="/api/resume", tags=["resume"])
app.include_router(document.router, prefix="/api/document", tags=["document"])
app.include_router(email.router, prefix="/api/email", tags=["email"])
app.include_router(social.router, prefix="/api/social", tags=["social-media"])
app.include_router(creative.router, prefix="/api/creative", tags=["creative"])
app.include_router(research.router, prefix="/api/research", tags=["research"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

# Root endpoint removed - Angular UI serves from root
# API documentation available at /docs
# @app.get("/")
# @limiter.limit("100/minute")
# async def root(request: Request):
#     return {
#         "message": "Welcome to EliteContent API v3.0",
#         "version": "3.0.0",
#         "features": [
#             "Resume Generation with ATS Optimization",
#             "Document Generation (Cover Letters, Proposals, Reports)",
#             "Email Generation (Professional, Marketing, Follow-ups)",
#             "Social Media Content (Twitter, LinkedIn, Instagram, Facebook)",
#             "Creative Content (Blogs, Stories, Scripts)",
#             "Research with RAG, Vector Search, and MCP (GitHub, arXiv, PubMed)"
#         ],
#         "enhancements": [
#             "RAG with ChromaDB vector store",
#             "Redis caching for performance",
#             "MCP integrations (GitHub, arXiv, PubMed)",
#             "Rate limiting protection",
#             "Semantic search with embeddings"
#         ]
#     }

@app.get("/api/health")
@limiter.limit("200/minute")
async def health_check(request: Request):
    from services.cache_service import CacheService
    from services.vector_store import VectorStore
    
    cache = CacheService()
    vector_store = VectorStore()
    
    return {
        "status": "healthy",
        "version": "3.0.0",
        "cache": cache.get_stats(),
        "vector_store": vector_store.get_stats()
    }


# Mount static files for Angular frontend
if FRONTEND_DIR.exists():
    # Serve static assets (JS, CSS, etc.)
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIR)), name="assets")
    
    # Catch-all route to serve Angular app
    @app.get("/{full_path:path}")
    async def serve_angular(full_path: str):
        """Serve Angular app for all non-API routes"""
        # Skip API routes
        if full_path.startswith("api/"):
            return {"error": "Not found"}
        
        # Serve specific files if they exist
        file_path = FRONTEND_DIR / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        
        # Serve index.html for all other routes (Angular routing)
        index_path = FRONTEND_DIR / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
        else:
            return {"error": "Frontend not found", "path": str(FRONTEND_DIR)}
else:
    print(f"⚠️  Frontend build not found at {FRONTEND_DIR}")
    print("   Run 'cd frontend && npm run build' to build the frontend")
