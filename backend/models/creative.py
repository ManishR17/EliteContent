from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class CreativeRequest(BaseModel):
    """Request model for creative content generation"""
    content_type: str = Field(..., description="Type: blog, story, script, poem, article")
    topic: str = Field(..., description="Topic or theme")
    style: str = Field(default="informative", description="Style: humorous, serious, inspirational, technical")
    target_audience: str = Field(..., description="Target audience")
    length: str = Field(default="medium", description="Length: short, medium, long")
    keywords: List[str] = Field(default_factory=list, description="SEO keywords to include")
    tone: str = Field(default="engaging", description="Overall tone")
    use_multi_agent: bool = Field(default=False, description="Use multi-agent system")
    enable_explanation: bool = Field(default=False, description="Include explanation")


class CreativeResponse(BaseModel):
    """Response model for creative content"""
    content: str = Field(..., description="Generated creative content")
    title: str = Field(..., description="Generated title")
    tags: List[str] = Field(default_factory=list, description="Content tags")
    seo_score: int = Field(default=0, description="SEO optimization score (0-100)", ge=0, le=100)
    word_count: int = Field(..., description="Word count")
    readability_score: float = Field(default=0.0, description="Readability score")
    # AI Intelligence
    similar_content_used: Optional[int] = Field(None, description="Similar content for context")
    multi_agent_result: Optional[Dict] = Field(None, description="Multi-agent results")
    explanation: Optional[Dict] = Field(None, description="Creative choices explanation")
    quality_score: Optional[int] = Field(None, description="Quality score")
