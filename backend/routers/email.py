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
        
        signature = _generate_signature()
        
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
    
    # Build AI prompt
    key_points_text = "\n".join(f'- {point}' for point in request.key_points) if request.key_points else 'N/A'
    
    prompt = f"""Generate a {request.email_type} email.

**Details:**
- Recipient: {request.recipient}
- Purpose: {request.purpose}
- Tone: {request.tone}

**Key Points:**
{key_points_text}

**Call to Action:**
{request.call_to_action or 'None specified'}

**Context:**
{request.context or 'N/A'}

**Instructions:**
1. Create an attention-grabbing subject line
2. Write a professional email body matching the {request.tone} tone
3. Include all key points naturally
4. End with appropriate closure
5. Avoid spam triggers
6. Keep it concise and actionable

Output format:
SUBJECT: [subject line]

BODY:
[email body]

Do not include signature."""

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
    
    key_points = "\n\n".join(request.key_points) if request.key_points else "We have exciting opportunities to discuss."
    cta = request.call_to_action or "Let's schedule a time to discuss further."
    
    templates = {
        "professional": (
            f"Re: {request.purpose}",
            f"""Dear {request.recipient},

I hope this message finds you well.

{request.purpose}

{key_points}

{cta}

Thank you for your time and consideration.

---
NOTE: This is a DEMO email. For AI-personalized emails, add your API key to backend/.env"""
        ),
        
        "marketing": (
            f"🎯 {request.purpose}",
            f"""Hi {request.recipient},

We're excited to share something special with you!

{key_points}

{cta}

We look forward to serving you!

---
NOTE: This is a DEMO email. For AI-optimized marketing emails, add your API key to backend/.env"""
        ),
        
        "follow_up": (
            f"Following up: {request.purpose}",
            f"""Hi {request.recipient},

I wanted to follow up on our previous conversation regarding {request.purpose}.

{key_points}

{cta}

Looking forward to hearing from you.

---
NOTE: This is a DEMO email. For AI-crafted follow-ups, add your API key to backend/.env"""
        ),
        
        "cold_outreach": (
            f"Quick question about {request.purpose}",
            f"""Hi {request.recipient},

I came across your profile and was impressed by your work.

{key_points}

{cta}

Thanks for your time!

---
NOTE: This is a DEMO email. For AI-personalized outreach, add your API key to backend/.env"""
        ),
        
        "thank_you": (
            f"Thank you - {request.purpose}",
            f"""Dear {request.recipient},

Thank you so much for {request.purpose}.

{key_points}

I truly appreciate your support.

Warmly,

---
NOTE: This is a DEMO email. For AI-heartfelt messages, add your API key to backend/.env"""
        ),
    }
    
    return templates.get(request.email_type, templates["professional"])


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


def _generate_signature() -> str:
    """Generate email signature"""
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
    
    if request.email_type == "marketing" and not request.call_to_action:
        suggestions.append("Marketing emails should include a clear call-to-action")
    
    if request.tone == "formal" and request.email_type == "marketing":
        suggestions.append("Consider a more engaging tone for marketing emails")
    
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
