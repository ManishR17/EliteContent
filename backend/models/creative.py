from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class CreativeRequest(BaseModel):
    """Request model for creative content generation with comprehensive inputs"""
    
    # REQUIRED FIELDS
    content_type: str = Field(..., description="Type: Story, Script, Blog, Poem, Video Script, Article")
    topic: str = Field(..., description="Main topic or theme")
    target_audience: str = Field(..., description="Target audience (e.g., 'Kids', 'Adults', 'Professionals')")
    
    # OPTIONAL FIELDS - Creative Elements
    genre: Optional[str] = Field(None, description="Genre: Sci-Fi, Romance, Thriller, Comedy, Drama, Fantasy")
    main_characters: Optional[List[str]] = Field(None, description="Main characters and their traits")
    plot_idea: Optional[str] = Field(None, description="Plot idea or storyline")
    setting: Optional[str] = Field(None, description="Setting (place, time, environment)")
    
    # OPTIONAL FIELDS - Style & Tone
    writing_style: str = Field(default="Descriptive", description="Style: Cinematic, Descriptive, Fast-Paced, Minimalist")
    tone: str = Field(default="Neutral", description="Tone: Dark, Emotional, Humorous, Inspiring")
    length: str = Field(default="Medium", description="Length: Short, Medium, Long")
    dialogue_heavy: bool = Field(default=False, description="Include heavy dialogue")
    
    # OPTIONAL FIELDS - SEO & AI
    keywords: List[str] = Field(default_factory=list, description="SEO keywords to include")
    use_multi_agent: bool = Field(default=False, description="Use multi-agent system for 2x quality")
    enable_explanation: bool = Field(default=False, description="Include explanation of creative choices")


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
