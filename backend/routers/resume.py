from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List, Optional
import json

from models.resume import ResumeGenerationRequest, ResumeGenerationResponse
from services.resume_parser import ResumeParser
from services.ai_service import AIService
from services.ats_optimizer import ATSOptimizer
from services.universal_rag import UniversalRAG
from services.multi_agent_system import MultiAgentOrchestrator
from services.explainability_service import ExplainabilityService

router = APIRouter()

# Initialize services
resume_parser = ResumeParser()
ai_service = AIService()
ats_optimizer = ATSOptimizer()
universal_rag = UniversalRAG()
multi_agent = MultiAgentOrchestrator()
explainability = ExplainabilityService()


@router.post("/generate", response_model=ResumeGenerationResponse)
async def generate_resume(request: ResumeGenerationRequest):
    """
    Generate a tailored, ATS-optimized resume with AI intelligence
    
    **Features:**
    - AI-powered resume generation (Claude/OpenAI)
    - ATS optimization and scoring
    - Skills matching analysis
    - RAG-based job matching (optional)
    - Multi-agent system for 2× quality (optional)
    - Explainability for transparency (optional)
    
    This endpoint accepts resume details and job requirements,
    then generates a customized resume optimized for ATS systems.
    """
    try:
        # Generate resume content using AI
        if ai_service.service_type == "demo":
            tailored_resume = _generate_demo_resume(request)
            multi_agent_result = None
            quality_score = None
        elif request.use_multi_agent:
            # Use multi-agent system for higher quality
            print("🤖 Multi-Agent: Starting resume generation...")
            
            ma_request = {
                'type': 'resume',
                'topic': request.target_job_title,
                'requirements': [
                    f"Experience: {request.years_of_experience} years",
                    f"Skills: {', '.join(request.core_skills[:5])}",
                    f"Tone: {request.tone_style}",
                    f"Format: {request.format_type}",
                    f"Target ATS score: 85+"
                ],
                'criteria': {
                    'ats_optimization': True,
                    'keyword_matching': True,
                    'clarity': True,
                    'professionalism': True
                }
            }
            
            ma_result = await multi_agent.generate_content(
                ma_request,
                context=request.job_description,
                quality_threshold=80
            )
            
            tailored_resume = ma_result['content']
            multi_agent_result = {
                'final_score': ma_result['final_score'],
                'iterations': len(ma_result['iterations']),
                'improvement': ma_result.get('improvement', 0)
            }
            quality_score = ma_result['final_score']
            print(f"✅ Multi-Agent complete (Score: {quality_score}/100)")
        else:
            # Standard AI generation
            tailored_resume = await _generate_resume_content(request)
            multi_agent_result = None
            quality_score = None
        
        # Calculate ATS score and analysis
        ats_score, analysis = ats_optimizer.calculate_ats_score(
            resume_text=tailored_resume,
            job_description=request.job_description
        )
        
        # Generate improvement suggestions
        suggestions = ats_optimizer.generate_suggestions(analysis)
        
        # Explainability (if requested)
        explanation = None
        if request.enable_explanation:
            print("💡 Generating explanation...")
            explanation = await explainability.explain_resume_choices(
                tailored_resume,
                request.job_description,
                f"Skills: {', '.join(request.core_skills)}"
            )
            print("✅ Explanation generated")
        
        # Build response
        response = ResumeGenerationResponse(
            tailored_resume=tailored_resume,
            ats_score=ats_score,
            matched_skills=analysis['matched_skills'],
            missing_skills=analysis['missing_skills'],
            suggestions=suggestions,
            keyword_density=analysis['keyword_density'],
            multi_agent_result=multi_agent_result,
            explanation=explanation,
            quality_score=quality_score
        )
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate resume: {str(e)}"
        )


async def _generate_resume_content(request: ResumeGenerationRequest) -> str:
    """Generate resume content using AI"""
    
    # Build comprehensive AI prompt
    skills_text = ", ".join(request.core_skills)
    achievements_text = "\n".join(f"- {ach}" for ach in request.achievements) if request.achievements else "N/A"
    
    prompt = f"""Generate a professional, ATS-optimized resume.

**Job Details:**
- Target Position: {request.target_job_title}
- Years of Experience: {request.years_of_experience}
- Industry: {request.industry or 'Not specified'}
- Career Level: {request.career_level}

**Job Description:**
{request.job_description}

**Candidate Skills:**
{skills_text}

**Key Achievements:**
{achievements_text}

**Resume Requirements:**
- Tone Style: {request.tone_style}
- Format Type: {request.format_type}
- Work Authorization: {request.work_authorization or 'Not specified'}

**Additional Context:**
{request.additional_context or 'None provided'}

**Instructions:**
1. Create a professional resume tailored to the job description
2. Use {request.tone_style} tone throughout
3. Apply {request.format_type} formatting
4. Highlight all candidate skills, especially those matching the job description
5. Incorporate key achievements naturally
6. Optimize for ATS systems with proper keywords
7. Structure for {request.career_level} career level
8. Target {request.years_of_experience} years of experience level
9. Include relevant sections: Summary, Experience, Skills, Education, Achievements
10. Make it compelling and professional

Generate ONLY the resume content, no meta-commentary."""

    # Generate with AI
    if ai_service.service_type == "claude":
        return await ai_service._generate_with_claude(prompt)
    elif ai_service.service_type == "openai":
        return await ai_service._generate_with_openai(prompt)
    else:
        return _generate_demo_resume(request)


def _generate_demo_resume(request: ResumeGenerationRequest) -> str:
    """Generate demo resume without AI"""
    
    skills_text = ", ".join(request.core_skills[:10])
    achievements_text = "\n".join(f"• {ach}" for ach in request.achievements[:5]) if request.achievements else "• Led successful projects\n• Exceeded performance targets\n• Mentored junior team members"
    
    return f"""[YOUR NAME]
[Your Address] | [City, State ZIP]
[Email] | [Phone] | [LinkedIn]

PROFESSIONAL SUMMARY

{request.career_level} professional with {request.years_of_experience} years of experience in {request.industry or 'the industry'}. Seeking {request.target_job_title} position to leverage expertise in {', '.join(request.core_skills[:3])}.

CORE SKILLS

{skills_text}

PROFESSIONAL EXPERIENCE

{request.target_job_title} (Similar Role)
Company Name | Dates
• Managed projects aligned with job requirements
• Utilized skills: {', '.join(request.core_skills[:5])}
• Delivered results in fast-paced environment

KEY ACHIEVEMENTS

{achievements_text}

EDUCATION

[Degree] in [Field]
[University Name] | [Year]

CERTIFICATIONS

• Relevant certifications for {request.target_job_title}

{f'WORK AUTHORIZATION: {request.work_authorization}' if request.work_authorization else ''}

---
NOTE: This is a DEMO resume. For AI-tailored resumes, add your API key to backend/.env"""


@router.get("/health")
async def health_check():
    """Health check endpoint for resume service"""
    return {
        "status": "healthy",
        "service": "resume",
        "ai_service": ai_service.service_type,
        "features": {
            "rag": True,
            "multi_agent": True,
            "explainability": True
        },
        "rag_stats": universal_rag.get_collection_stats('resumes')
    }
