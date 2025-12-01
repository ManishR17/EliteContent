from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routers import resume, document, email, social, creative, research, dashboard, auth
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os

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
    allow_origins=["http://localhost:4200"],  # Angular dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for all features
app.include_router(resume.router, prefix="/api/resume", tags=["resume"])
app.include_router(document.router, prefix="/api/document", tags=["document"])
app.include_router(email.router, prefix="/api/email", tags=["email"])
app.include_router(social.router, prefix="/api/social", tags=["social-media"])
app.include_router(creative.router, prefix="/api/creative", tags=["creative"])
app.include_router(research.router, prefix="/api/research", tags=["research"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

@app.get("/")
@limiter.limit("100/minute")
async def root(request: Request):
    return {
        "message": "Welcome to EliteContent API v3.0",
        "version": "3.0.0",
        "features": [
            "Resume Generation with ATS Optimization",
            "Document Generation (Cover Letters, Proposals, Reports)",
            "Email Generation (Professional, Marketing, Follow-ups)",
            "Social Media Content (Twitter, LinkedIn, Instagram, Facebook)",
            "Creative Content (Blogs, Stories, Scripts)",
            "Research with RAG, Vector Search, and MCP (GitHub, arXiv, PubMed)"
        ],
        "enhancements": [
            "RAG with ChromaDB vector store",
            "Redis caching for performance",
            "MCP integrations (GitHub, arXiv, PubMed)",
            "Rate limiting protection",
            "Semantic search with embeddings"
        ]
    }

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
