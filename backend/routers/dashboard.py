from fastapi import APIRouter
from services.universal_rag import UniversalRAG
from services.ai_service import AIService

router = APIRouter()
universal_rag = UniversalRAG()
ai_service = AIService()

@router.get("/stats")
async def get_dashboard_stats():
    """Get global statistics for the dashboard"""
    
    # Get counts from RAG collections
    collections = ['resumes', 'documents', 'emails', 'social', 'creative']
    stats = {}
    total_items = 0
    
    for col in collections:
        col_stats = universal_rag.get_collection_stats(col)
        count = col_stats.get('count', 0)
        stats[col] = count
        total_items += count
        
    return {
        "total_generated": total_items,
        "collections": stats,
        "ai_service": ai_service.service_type,
        "system_status": "operational"
    }
