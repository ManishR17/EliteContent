from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Source(BaseModel):
    """Source information for research"""
    title: str = Field(..., description="Source title")
    url: str = Field(..., description="Source URL")
    snippet: str = Field(..., description="Brief excerpt or summary")
    relevance_score: float = Field(default=0.0, description="Relevance score 0-1")
    source_type: str = Field(default="web", description="Source type: wikipedia, google, web, demo")
    content: Optional[str] = Field(None, description="Full extracted content")


class ResearchRequest(BaseModel):
    """Request model for research generation with comprehensive inputs"""
    
    # REQUIRED FIELDS
    topic: str = Field(..., description="Research topic or question")
    research_question: str = Field(..., description="Specific research question to answer")
    depth: str = Field(..., description="Depth: Quick (3-5 sources), Standard (5-10), Comprehensive (10-20)")
    
    # OPTIONAL FIELDS - Research Scope
    sources_count: int = Field(default=5, description="Number of sources to find", ge=1, le=20)
    citation_style: str = Field(default="APA", description="Citation style: APA, MLA, Chicago, IEEE")
    academic_level: str = Field(default="UG", description="Academic level: UG (Undergraduate), Graduate, PhD")
    
    # OPTIONAL FIELDS - Content Structure
    sections_needed: List[str] = Field(
        default_factory=lambda: ["introduction", "conclusion"],
        description="Sections: abstract, introduction, methodology, results, discussion, conclusion"
    )
    word_count: Optional[int] = Field(None, description="Target word count", ge=100, le=10000)
    focus_areas: List[str] = Field(default_factory=list, description="Specific areas to focus on")
    
    # OPTIONAL FIELDS - Sources
    sources_provided: Optional[List[str]] = Field(None, description="URLs or sources to include")
    include_citations: bool = Field(default=True, description="Include formatted citations")


class ResearchResponse(BaseModel):
    """Response model for research"""
    summary: str = Field(..., description="Research summary")
    key_findings: List[str] = Field(default_factory=list, description="Key findings")
    sources: List[Source] = Field(default_factory=list, description="Source references")
    citations: List[str] = Field(default_factory=list, description="Formatted citations")
    confidence_score: float = Field(default=0.0, description="Confidence in research quality (0-1)", ge=0, le=1)
    generated_at: datetime = Field(default_factory=datetime.now, description="Generation timestamp")
