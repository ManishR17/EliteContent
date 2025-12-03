from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class EmailRequest(BaseModel):
    """Request model for email generation with comprehensive inputs"""
    
    # REQUIRED FIELDS
    email_purpose: str = Field(..., description="Purpose: Follow-up, Complaint, Request, Inquiry, Introduction")
    recipient_type: str = Field(..., description="Recipient: HR, Client, Manager, Professor, Support, Colleague")
    key_points: List[str] = Field(..., description="Key points to cover in the email")
    
    # OPTIONAL FIELDS - Style & Tone
    tone_style: str = Field(default="Formal", description="Tone: Formal, Friendly, Assertive, Polite")
    urgency_level: str = Field(default="Normal", description="Urgency: Low, Normal, High, Urgent")
    
    # OPTIONAL FIELDS - Content Enhancement
    call_to_action: Optional[str] = Field(None, description="Desired action (e.g., 'Reply', 'Schedule meeting', 'Approve')")
    signature_details: Optional[str] = Field(None, description="Signature information (name, title, contact)")
    subject_line_preference: Optional[str] = Field(None, description="Preferred subject line (optional)")
    context: Optional[str] = Field(None, description="Additional context or background")
    
    # OPTIONAL FIELDS - AI Enhancement
    use_multi_agent: bool = Field(default=False, description="Use multi-agent system for 2x quality")
    enable_explanation: bool = Field(default=False, description="Include explanation of email strategy")


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
