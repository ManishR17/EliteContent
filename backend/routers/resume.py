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
async def generate_resume(
    file: UploadFile = File(..., description="Resume file (PDF or DOCX)"),
    job_description: str = Form(..., description="Job description"),
    target_role: str = Form(..., description="Target job title"),
    experience_level: str = Form(..., description="Experience level"),
    skills_to_highlight: str = Form(..., description="Skills to highlight (JSON array)"),
    tone_preference: str = Form(default="Professional", description="Tone preference"),
    format_type: str = Form(default="ATS-Friendly", description="Format type"),
    additional_achievements: Optional[str] = Form(None, description="Additional achievements"),
    use_multi_agent: bool = Form(default=False, description="Use multi-agent system for higher quality"),
    enable_explanation: bool = Form(default=False, description="Include explanation of choices")
):
    """
    Generate a tailored, ATS-optimized resume with AI intelligence
    
    **NEW Features:**
    - RAG-based job matching and context
    - Multi-agent system for 2× quality (optional)
    - Explainability for transparency (optional)
    - Similar resume context
    
    This endpoint accepts a resume file and job-related parameters,
    then generates a customized resume using AI that is optimized for
    Applicant Tracking Systems (ATS).
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.pdf', '.docx')):
            raise HTTPException(
                status_code=400,
                detail="Only PDF and DOCX files are supported"
            )
        
        # Read and parse resume file
        file_content = await file.read()
        parsed_resume = await resume_parser.parse_resume(file_content, file.filename)
        
        # Parse skills from JSON string
        try:
            skills_list = json.loads(skills_to_highlight)
            if not isinstance(skills_list, list):
                skills_list = []
        except json.JSONDecodeError:
            skills_list = []
        
        # Build request object
        request = ResumeGenerationRequest(
            job_description=job_description,
            target_role=target_role,
            experience_level=experience_level,
            skills_to_highlight=skills_list,
            tone_preference=tone_preference,
            format_type=format_type,
            additional_achievements=additional_achievements,
            use_multi_agent=use_multi_agent,
            enable_explanation=enable_explanation
        )
        
        # ==================== AI INTELLIGENCE LAYER ====================
        
        # 1. RAG: Get job match analysis
        print("🔍 RAG: Analyzing job-resume match...")
        job_match_analysis = universal_rag.match_resume_to_job(
            parsed_resume.raw_text,
            job_description
        )
        print(f"✅ Match score: {job_match_analysis['match_score']}%")
        
        # 2. RAG: Get similar successful resumes for context
        print("🔍 RAG: Finding similar resumes...")
        similar_resumes = universal_rag.get_similar_content(
            'resumes',
            f"{target_role} {experience_level}",
            n_results=5
        )
        print(f"✅ Found {len(similar_resumes)} similar resumes")
        
        # Build RAG context
        rag_context = "\n\n".join([
            f"Example Resume {i+1}:\n{resume['content'][:300]}..."
            for i, resume in enumerate(similar_resumes[:3])
        ])
        
        # 3. Generate resume (with or without multi-agent)
        if use_multi_agent:
            print("🤖 Multi-Agent: Starting generation...")
            
            # Prepare multi-agent request
            ma_request = {
                'type': 'resume',
                'topic': target_role,
                'requirements': [
                    f"Experience level: {experience_level}",
                    f"Tone: {tone_preference}",
                    f"Format: {format_type}",
                    f"Target ATS score: 85+"
                ],
                'criteria': {
                    'ats_optimization': True,
                    'keyword_matching': True,
                    'clarity': True,
                    'professionalism': True
                }
            }
            
            # Generate with multi-agent system
            ma_result = await multi_agent.generate_content(
                ma_request,
                context=rag_context,
                quality_threshold=80
            )
            
            tailored_resume = ma_result['content']
            multi_agent_result = {
                'final_score': ma_result['final_score'],
                'iterations': len(ma_result['iterations']),
                'improvement': ma_result.get('improvement', 0),
                'plan_steps': len(ma_result['plan'].get('steps', []))
            }
            quality_score = ma_result['final_score']
            
            print(f"✅ Multi-Agent complete (Score: {quality_score}/100)")
        else:
            # Standard generation
            tailored_resume = await ai_service.generate_tailored_resume(
                parsed_resume=parsed_resume,
                request=request
            )
            multi_agent_result = None
            quality_score = None
        
        # 4. Calculate ATS score and analysis
        ats_score, analysis = ats_optimizer.calculate_ats_score(
            resume_text=tailored_resume,
            job_description=job_description
        )
        
        # Generate improvement suggestions
        suggestions = ats_optimizer.generate_suggestions(analysis)
        
        # 5. Explainability (if requested)
        explanation = None
        if enable_explanation:
            print("💡 Generating explanation...")
            explanation = await explainability.explain_resume_choices(
                tailored_resume,
                job_description,
                parsed_resume.raw_text
            )
            print("✅ Explanation generated")
        
        # 6. Store in RAG for future context
        print("💾 Storing resume in RAG...")
        universal_rag.store_content(
            'resumes',
            tailored_resume,
            {
                'target_role': target_role,
                'experience_level': experience_level,
                'ats_score': ats_score,
                'format_type': format_type
            }
        )
        
        # Build enhanced response
        response = ResumeGenerationResponse(
            tailored_resume=tailored_resume,
            ats_score=ats_score,
            matched_skills=analysis['matched_skills'],
            missing_skills=analysis['missing_skills'],
            suggestions=suggestions,
            keyword_density=analysis['keyword_density'],
            # NEW: AI Intelligence features
            job_match_analysis=job_match_analysis,
            similar_resumes_used=len(similar_resumes),
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
