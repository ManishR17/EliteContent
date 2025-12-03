from fastapi import APIRouter, HTTPException
from models.document import DocumentRequest, DocumentResponse
from services.ai_service import AIService
from services.utils import count_words, calculate_readability
import os

router = APIRouter()
ai_service = AIService()


@router.post("/generate", response_model=DocumentResponse)
async def generate_document(request: DocumentRequest):
    """
    Generate various types of professional documents
    
    Supported document types:
    - cover_letter: Professional cover letters
    - proposal: Business proposals
    - report: Professional reports
    - memo: Business memos
    - business_plan: Business plans
    """
    try:
        content = await _generate_document_content(request)
        
        # Calculate metrics
        word_count = count_words(content)
        readability = calculate_readability(content)
        
        # Generate suggestions
        suggestions = _generate_suggestions(request, word_count, readability)
        
        return DocumentResponse(
            content=content,
            word_count=word_count,
            readability_score=readability,
            suggestions=suggestions,
            document_type=request.document_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def _generate_document_content(request: DocumentRequest) -> str:
    """Generate document content using AI or demo mode"""
    
    if ai_service.service_type == "demo":
        return _generate_demo_document(request)
    
    # Build comprehensive AI prompt using all enhanced fields
    prompt = f"""Generate a professional {request.document_type.replace('_', ' ')} document.

**Document Details:**
- Title: {request.document_title}
- Type: {request.document_type.replace('_', ' ')}
- Purpose: {request.purpose}
- Target Audience: {request.target_audience}
- Tone Style: {request.tone_style}
- Length: {request.length}
- Formatting Preference: {request.formatting_preference}

**Key Points to Include:**
{chr(10).join(f'- {point}' for point in request.key_points)}

**Additional Context:**
{request.context or 'None provided'}

**Attachments Reference:**
{request.attachments_description or 'No attachments'}

**Instructions:**
1. Create a well-structured {request.document_type.replace('_', ' ')} with clear sections
2. Use {request.tone_style} tone throughout the document
3. Write specifically for {request.target_audience} audience
4. Target {request.length} length (Short: 1 page, Medium: 2-3 pages, Long: 5+ pages)
5. Apply {request.formatting_preference} formatting style
6. Incorporate all key points naturally and cohesively
7. Ensure the document serves its stated purpose: {request.purpose}
8. Use professional language appropriate for the document type
9. Include proper headings, sections, and formatting
10. Make it actionable and impactful

Generate ONLY the document content with proper formatting. No meta-commentary."""

    # Generate with AI
    if ai_service.service_type == "claude":
        return await ai_service._generate_with_claude(prompt)
    elif ai_service.service_type == "openai":
        return await ai_service._generate_with_openai(prompt)
    else:
        return _generate_demo_document(request)


def _generate_demo_document(request: DocumentRequest) -> str:
    """Generate demo document without AI"""
    
    key_points_text = "\n".join(f"• {point}" for point in request.key_points)
    
    templates = {
        "cover_letter": f"""[Your Name]
[Your Address]
[City, State ZIP]
[Email]
[Phone]

[Date]

Dear Hiring Manager,

{request.document_title}

I am writing to express my strong interest in this opportunity. {request.purpose}

Throughout my career, I have developed expertise in:
{key_points_text}

{request.context or 'I am particularly drawn to this opportunity because of the potential to make a meaningful impact.'}

I look forward to discussing how my skills and experience align with your needs. Thank you for your consideration.

Sincerely,
[Your Name]

---
NOTE: This is a DEMO document. For AI-personalized content, add your API key to backend/.env""",

        "proposal": f"""BUSINESS PROPOSAL

{request.document_title.upper()}

EXECUTIVE SUMMARY

{request.purpose}

This proposal is designed specifically for {request.target_audience}.

OBJECTIVES

{key_points_text}

METHODOLOGY

Our approach combines industry best practices with innovative solutions tailored to your specific needs.

DELIVERABLES

- Phase 1: Initial Assessment and Planning
- Phase 2: Implementation
- Phase 3: Evaluation and Optimization

{request.context or 'Additional details and timeline can be discussed during consultation.'}

{request.attachments_description or ''}

NEXT STEPS

We look forward to discussing this proposal and addressing any questions you may have.

---
NOTE: This is a DEMO document. For AI-customized proposals, add your API key to backend/.env""",

        "report": f"""PROFESSIONAL REPORT

{request.document_title}

SUMMARY

{request.purpose}

This report is prepared for {request.target_audience}.

KEY FINDINGS

{key_points_text}

ANALYSIS

{request.context or 'Our investigation reveals important considerations that merit attention moving forward.'}

RECOMMENDATIONS

Based on our findings, we recommend a strategic approach that addresses identified opportunities and challenges.

{request.attachments_description or ''}

CONCLUSION

The insights presented in this report provide a foundation for informed decision-making.

---
NOTE: This is a DEMO document. For AI-tailored reports, add your API key to backend/.env""",

        "memo": f"""MEMORANDUM

TO: {request.target_audience}
FROM: [Your Name]
DATE: [Current Date]
RE: {request.document_title}

PURPOSE

{request.purpose}

KEY POINTS

{key_points_text}

BACKGROUND

{request.context or 'This memo addresses important matters that require attention.'}

ACTION ITEMS

Please review and provide feedback by [deadline].

---
NOTE: This is a DEMO memo. For AI-generated content, add your API key to backend/.env""",
    }
    
    return templates.get(request.document_type, templates["report"])


def _generate_suggestions(request: DocumentRequest, word_count: int, readability: float) -> list:
    """Generate improvement suggestions"""
    suggestions = []
    
    # Length suggestions
    if request.length == "short" and word_count > 500:
        suggestions.append("Consider condensing to meet 'short' length requirement (~250-500 words)")
    elif request.length == "medium" and (word_count < 500 or word_count > 1500):
        suggestions.append("Adjust length to meet 'medium' requirement (~500-1500 words)")
    elif request.length == "long" and word_count < 1500:
        suggestions.append("Expand content to meet 'long' length requirement (1500+ words)")
    
    # Readability suggestions
    if readability < 30:
        suggestions.append("Text is complex. Consider simplifying language for better readability")
    elif readability > 80:
        suggestions.append("Text is very simple. Consider adding more sophisticated vocabulary if appropriate")
    
    # Tone suggestions
    if request.tone == "formal" and readability > 60:
        suggestions.append("For formal tone, consider using more professional vocabulary")
    
    if not suggestions:
        suggestions.append("Document looks good! Well-structured for the intended audience.")
    
    return suggestions


@router.get("/health")
async def health_check():
    """Health check for document service"""
    return {
        "status": "healthy",
        "service": "document",
        "ai_service": ai_service.service_type
    }
