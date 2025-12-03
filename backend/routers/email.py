from fastapi import APIRouter, HTTPException
from models.email import EmailRequest, EmailResponse
from services.ai_service import AIService
from services.utils import estimate_spam_score
import os

router = APIRouter()
ai_service = AIService()


@router.post("/generate", response_model=EmailResponse)
async def generate_email(request: EmailRequest):
    """
    Generate professional emails for various purposes
    
    Supported email types:
    - professional: Standard professional communication
    - marketing: Marketing and promotional emails
    - follow_up: Follow-up emails
    - cold_outreach: Initial outreach emails
    - thank_you: Thank you emails
    """
    try:
        subject, body = await _generate_email_content(request)
        
        # Calculate spam score
        spam_score = estimate_spam_score(subject + " " + body)
        
        # Generate suggestions
        suggestions = _generate_suggestions(request, spam_score)
        
        signature = _generate_signature(request)
        
        return EmailResponse(
            subject=subject,
            body=body,
            signature=signature,
            suggestions=suggestions,
            spam_score=spam_score
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def _generate_email_content(request: EmailRequest) -> tuple:
    """Generate email subject and body"""
    
    if ai_service.service_type == "demo":
        return _generate_demo_email(request)
    
    # Build comprehensive AI prompt using all enhanced fields
    key_points_text = "\n".join(f'- {point}' for point in request.key_points)
    
    prompt = f"""Generate a professional email.

**Email Context:**
- Purpose: {request.email_purpose}
- Recipient Type: {request.recipient_type}
- Tone Style: {request.tone_style}
- Urgency Level: {request.urgency_level}

**Key Points to Cover:**
{key_points_text}

**Call to Action:**
{request.call_to_action or 'None specified - use appropriate closing'}

**Signature Details:**
{request.signature_details or 'Use standard professional signature'}

**Subject Line Preference:**
{request.subject_line_preference or 'Create an effective subject line'}

**Additional Context:**
{request.context or 'None provided'}

**Instructions:**
1. Create an attention-grabbing subject line that matches the {request.urgency_level} urgency level
2. Write a {request.tone_style} email body appropriate for {request.recipient_type}
3. Incorporate all key points naturally and cohesively
4. Match the {request.urgency_level} urgency level in language and structure
5. Include the specified call to action if provided
6. End with appropriate closure for {request.recipient_type}
7. Avoid spam triggers and excessive punctuation
8. Keep it concise, clear, and actionable
9. Ensure the email serves its purpose: {request.email_purpose}

Output format:
SUBJECT: [subject line]

BODY:
[email body]

Do not include signature block."""

    # Generate with AI
    if ai_service.service_type == "claude":
        content = await ai_service._generate_with_claude(prompt)
    elif ai_service.service_type == "openai":
        content = await ai_service._generate_with_openai(prompt)
    else:
        return _generate_demo_email(request)
    
    # Parse subject and body
    subject, body = _parse_email_response(content)
    return subject, body


def _generate_demo_email(request: EmailRequest) -> tuple:
    """Generate demo email without AI"""
    
    key_points = "\n\n".join(request.key_points)
    cta = request.call_to_action or "Let's schedule a time to discuss further."
    
    # Create subject based on purpose and urgency
    urgency_prefix = {
        "Urgent": "🔴 URGENT: ",
        "High": "⚡ ",
        "Normal": "",
        "Low": ""
    }.get(request.urgency_level, "")
    
    subject = f"{urgency_prefix}{request.subject_line_preference or request.email_purpose}"
    
    body = f"""Dear {request.recipient_type},

I hope this message finds you well.

{request.email_purpose}

{key_points}

{request.context or ''}

{cta}

Thank you for your time and consideration.

---
NOTE: This is a DEMO email. For AI-personalized emails, add your API key to backend/.env"""
    
    return subject, body


def _parse_email_response(content: str) -> tuple:
    """Parse subject and body from AI response"""
    lines = content.split('\n')
    subject = ""
    body_lines = []
    in_body = False
    
    for line in lines:
        if line.startswith("SUBJECT:"):
            subject = line.replace("SUBJECT:", "").strip()
        elif line.startswith("BODY:"):
            in_body = True
        elif in_body:
            body_lines.append(line)
    
    body = "\n".join(body_lines).strip()
    
    if not subject:
        subject = "Your Message"
    if not body:
        body = content
    
    return subject, body


def _generate_signature(request: EmailRequest = None) -> str:
    """Generate email signature"""
    if request and request.signature_details:
        return request.signature_details
    
    return """Best regards,
[Your Name]
[Your Title]
[Company]
[Contact Info]"""


def _generate_suggestions(request: EmailRequest, spam_score: float) -> list:
    """Generate email improvement suggestions"""
    suggestions = []
    
    if spam_score > 50:
        suggestions.append("High spam score detected. Remove excessive punctuation and promotional language")
    elif spam_score > 30:
        suggestions.append("Moderate spam risk. Consider toning down urgency or sales language")
    
    if request.urgency_level == "Urgent" and spam_score > 40:
        suggestions.append("Urgent emails may trigger spam filters. Ensure content justifies urgency")
    
    if not request.call_to_action:
        suggestions.append("Consider adding a clear call-to-action to improve response rates")
    
    if request.tone_style == "Formal" and request.urgency_level == "Urgent":
        suggestions.append("Formal tone with urgent priority may seem contradictory. Review tone choice")
    
    if not suggestions:
        suggestions.append("Email looks professional and ready to send!")
    
    return suggestions


@router.get("/health")
async def health_check():
    """Health check for email service"""
    return {
        "status": "healthy",
        "service": "email",
        "ai_service": ai_service.service_type
    }
