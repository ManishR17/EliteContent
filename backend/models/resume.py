from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class ResumeGenerationRequest(BaseModel):
    """Request model for resume generation"""
    job_description: str = Field(..., description="Job description text")
    target_role: str = Field(..., description="Target job title/role")
    experience_level: str = Field(..., description="Experience level (Entry Level, Mid-Level, Senior, Lead, Executive)")
    skills_to_highlight: List[str] = Field(default_factory=list, description="Skills to emphasize")
    tone_preference: str = Field(default="Professional", description="Tone preference (Professional, Confident, Humble, Assertive, Balanced)")
    format_type: str = Field(default="ATS-Friendly", description="Resume format type (Minimal, ATS-Friendly, Modern, Executive)")
    additional_achievements: Optional[str] = Field(None, description="Additional achievements to highlight")
    use_multi_agent: bool = Field(default=False, description="Use multi-agent system for higher quality")
    enable_explanation: bool = Field(default=False, description="Include explanation of choices")


class ResumeGenerationResponse(BaseModel):
    """Response model for resume generation"""
    tailored_resume: str = Field(..., description="Generated resume content")
    ats_score: int = Field(..., description="ATS compatibility score (0-100)", ge=0, le=100)
    matched_skills: List[str] = Field(default_factory=list, description="Skills from job description found in resume")
    missing_skills: List[str] = Field(default_factory=list, description="Skills from job description missing in resume")
    suggestions: List[str] = Field(default_factory=list, description="Suggestions for improvement")
    keyword_density: dict = Field(default_factory=dict, description="Keyword analysis")
    
    # NEW: AI Intelligence Features
    job_match_analysis: Optional[Dict] = Field(None, description="RAG-based job matching analysis")
    similar_resumes_used: Optional[int] = Field(None, description="Number of similar resumes used for context")
    multi_agent_result: Optional[Dict] = Field(None, description="Multi-agent system results")
    explanation: Optional[Dict] = Field(None, description="Explanation of generation choices")
    quality_score: Optional[int] = Field(None, description="Overall quality score from critic agent")


class ParsedResume(BaseModel):
    """Model for parsed resume data"""
    raw_text: str
    sections: dict = Field(default_factory=dict)
    skills: List[str] = Field(default_factory=list)
    experience_years: Optional[int] = None
