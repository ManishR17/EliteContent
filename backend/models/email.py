from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class EmailRequest(BaseModel):
    """Request model for email generation"""
    email_type: str = Field(..., description="Type: professional, marketing, follow_up, cold_outreach, thank_you")
    recipient: str = Field(..., description="Recipient name or role")
    purpose: str = Field(..., description="Purpose of the email")
    tone: str = Field(default="professional", description="Tone: formal, friendly, persuasive, casual")
    key_points: List[str] = Field(default_factory=list, description="Key points to cover")
    call_to_action: Optional[str] = Field(None, description="Desired call to action")
    context: Optional[str] = Field(None, description="Additional context")
    use_multi_agent: bool = Field(default=False, description="Use multi-agent system")
    enable_explanation: bool = Field(default=False, description="Include explanation")


class EmailResponse(BaseModel):
    """Response model for email generation"""
    subject: str = Field(..., description="Email subject line")
    body: str = Field(..., description="Email body content")
    signature: Optional[str] = Field(None, description="Suggested signature")
    suggestions: List[str] = Field(default_factory=list, description="Improvement tips")
    spam_score: float = Field(default=0.0, description="Estimated spam score (0-100, lower is better)")
    # AI Intelligence
    similar_emails_used: Optional[int] = Field(None, description="Similar emails for context")
    multi_agent_result: Optional[Dict] = Field(None, description="Multi-agent results")
    explanation: Optional[Dict] = Field(None, description="Email strategy explanation")
    quality_score: Optional[int] = Field(None, description="Quality score")
