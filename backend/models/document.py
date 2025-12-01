from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class DocumentRequest(BaseModel):
    """Request model for document generation"""
    document_type: str = Field(..., description="Type of document: cover_letter, proposal, report, memo, business_plan")
    topic: str = Field(..., description="Main topic or subject of the document")
    target_audience: str = Field(..., description="Intended audience")
    tone: str = Field(default="formal", description="Tone: formal, casual, persuasive, technical")
    key_points: List[str] = Field(default_factory=list, description="Key points to include")
    length: str = Field(default="medium", description="Length: short (1 page), medium (2-3 pages), long (5+ pages)")
    context: Optional[str] = Field(None, description="Additional context or background")
    use_multi_agent: bool = Field(default=False, description="Use multi-agent system")
    enable_explanation: bool = Field(default=False, description="Include explanation")


class DocumentResponse(BaseModel):
    """Response model for document generation"""
    content: str = Field(..., description="Generated document content")
    word_count: int = Field(..., description="Total word count")
    readability_score: float = Field(..., description="Flesch reading ease score (0-100)")
    suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")
    document_type: str = Field(..., description="Type of document generated")
    # AI Intelligence
    similar_documents_used: Optional[int] = Field(None, description="Similar documents for context")
    templates_used: Optional[List[Dict]] = Field(None, description="Templates used")
    multi_agent_result: Optional[Dict] = Field(None, description="Multi-agent results")
    explanation: Optional[Dict] = Field(None, description="Structure explanation")
    quality_score: Optional[int] = Field(None, description="Quality score")
