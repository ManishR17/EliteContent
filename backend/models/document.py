from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class DocumentRequest(BaseModel):
    """Request model for document generation with comprehensive inputs"""
    
    # REQUIRED FIELDS
    document_type: str = Field(..., description="Type: cover_letter, proposal, report, memo, business_plan")
    document_title: str = Field(..., description="Document title or subject")
    purpose: str = Field(..., description="Purpose of the document (e.g., 'Secure funding', 'Report Q4 results')")
    target_audience: str = Field(..., description="Intended audience (e.g., 'Executive Team', 'Investors')")
    key_points: List[str] = Field(..., description="Key points to include in the document")
    
    # OPTIONAL FIELDS - Style & Format
    tone_style: str = Field(default="Formal", description="Tone: Formal, Friendly, Technical, Persuasive")
    length: str = Field(default="Medium", description="Length: Short (1 page), Medium (2-3 pages), Long (5+ pages)")
    formatting_preference: str = Field(default="Corporate", description="Format: Simple, Corporate, Detailed")
    
    # OPTIONAL FIELDS - Content Enhancement
    attachments_description: Optional[str] = Field(None, description="Description of attachments (if any)")
    context: Optional[str] = Field(None, description="Additional context or background information")
    
    # OPTIONAL FIELDS - AI Enhancement
    use_multi_agent: bool = Field(default=False, description="Use multi-agent system for 2x quality")
    enable_explanation: bool = Field(default=False, description="Include explanation of structure")


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
