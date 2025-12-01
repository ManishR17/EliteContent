from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class SocialMediaRequest(BaseModel):
    """Request model for social media content generation"""
    platform: str = Field(..., description="Platform: twitter, linkedin, instagram, facebook")
    content_type: str = Field(..., description="Type: post, thread, caption, story")
    topic: str = Field(..., description="Topic or theme")
    tone: str = Field(default="engaging", description="Tone: professional, casual, humorous, inspirational")
    include_hashtags: bool = Field(default=True, description="Include hashtags")
    include_emoji: bool = Field(default=True, description="Include emojis")
    target_audience: Optional[str] = Field(None, description="Target audience")
    call_to_action: Optional[str] = Field(None, description="Call to action")
    use_multi_agent: bool = Field(default=False, description="Use multi-agent system")
    enable_explanation: bool = Field(default=False, description="Include explanation")


class SocialMediaResponse(BaseModel):
    """Response model for social media content"""
    content: str = Field(..., description="Generated content")
    hashtags: List[str] = Field(default_factory=list, description="Suggested hashtags")
    character_count: int = Field(..., description="Character count")
    platform_optimized: bool = Field(default=True, description="Whether content is optimized for platform")
    engagement_tips: List[str] = Field(default_factory=list, description="Tips to boost engagement")
    alternative_versions: Optional[List[str]] = Field(None, description="Alternative content variations")
    # AI Intelligence
    similar_posts_used: Optional[int] = Field(None, description="Similar posts for context")
    recommended_hashtags: Optional[List[Dict]] = Field(None, description="RAG hashtag recommendations")
    multi_agent_result: Optional[Dict] = Field(None, description="Multi-agent results")
    explanation: Optional[Dict] = Field(None, description="Strategy explanation")
    quality_score: Optional[int] = Field(None, description="Quality score")
