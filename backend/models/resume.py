from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class ResumeGenerationRequest(BaseModel):
    """Request model for resume generation with comprehensive inputs"""
    
    # REQUIRED FIELDS
    job_description: str = Field(..., description="Full job description text")
    target_job_title: str = Field(..., description="Target job title (e.g., 'Senior Software Engineer')")
    years_of_experience: int = Field(..., description="Total years of professional experience", ge=0, le=50)
    core_skills: List[str] = Field(..., description="Core skills to highlight (e.g., ['Python', 'FastAPI', 'AI'])")
    
    # OPTIONAL FIELDS - Industry & Style
    industry: Optional[str] = Field(None, description="Industry (IT, Finance, Healthcare, Marketing, etc.)")
    tone_style: str = Field(default="ATS", description="Tone: Formal, Strong, ATS, Clean")
    career_level: str = Field(default="Mid", description="Career level: Entry, Mid, Senior, Lead, Executive")
    
    # OPTIONAL FIELDS - Content Enhancement
    achievements: Optional[List[str]] = Field(None, description="Key achievements to emphasize")
    work_authorization: Optional[str] = Field(None, description="Work authorization status (e.g., 'US Citizen', 'H1B')")
    additional_context: Optional[str] = Field(None, description="Additional context or special requirements")
    
    # OPTIONAL FIELDS - Format & AI
    format_type: str = Field(default="ATS-Friendly", description="Format: Minimal, ATS-Friendly, Modern, Executive")
    use_multi_agent: bool = Field(default=False, description="Use multi-agent system for 2x quality")
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
