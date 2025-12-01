from fastapi import APIRouter, HTTPException
from models.social import SocialMediaRequest, SocialMediaResponse
from services.ai_service import AIService
from services.utils import count_characters, get_platform_character_limit
import re

router = APIRouter()
ai_service = AIService()


@router.post("/generate", response_model=SocialMediaResponse)
async def generate_social_media(request: SocialMediaRequest):
    """
    Generate platform-specific social media content
    
    Supported platforms:
    - twitter: Short, engaging tweets
    - linkedin: Professional posts
    - instagram: Visual-focused captions
    - facebook: Casual, community-focused posts
    """
    try:
        content = await _generate_social_content(request)
        
        # Extract or generate hashtags
        hashtags = _extract_or_generate_hashtags(content, request)
        
        # Calculate character count
        char_count = count_characters(content, include_spaces=True)
        
        # Check platform optimization
        limit = get_platform_character_limit(request.platform)
        platform_optimized = char_count <= limit
        
        # Generate engagement tips
        tips = _generate_engagement_tips(request)
        
        # Generate alternative versions
        alternatives = await _generate_alternatives(request) if request.content_type == "post" else None
        
        return SocialMediaResponse(
            content=content,
            hashtags=hashtags,
            character_count=char_count,
            platform_optimized=platform_optimized,
            engagement_tips=tips,
            alternative_versions=alternatives
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def _generate_social_content(request: SocialMediaRequest) -> str:
    """Generate social media content"""
    
    if ai_service.service_type == "demo":
        return _generate_demo_social(request)
    
    # Build AI prompt
    emoji_instruction = "Include relevant emojis" if request.include_emoji else "Do not use emojis"
    hashtag_instruction = "Include relevant hashtags" if request.include_hashtags else "Do not use hashtags"
    
    prompt = f"""Generate {request.platform} {request.content_type} content.

**Details:**
- Topic: {request.topic}
- Tone: {request.tone}
- Target Audience: {request.target_audience or 'General audience'}

**Platform:** {request.platform}
**Character Limit:** {get_platform_character_limit(request.platform)} characters

**Requirements:**
1. {emoji_instruction}
2. {hashtag_instruction}
3. Match {request.tone} tone
4. Optimize for {request.platform} best practices
5. Include call-to-action: {request.call_to_action or 'Engage with the content'}
6. Stay within character limit
7. Make it engaging and shareable

Generate ONLY the post content, no explanations."""

    # Generate with AI  
    if ai_service.service_type == "claude":
        return await ai_service._generate_with_claude(prompt)
    elif ai_service.service_type == "openai":
        return await ai_service._generate_with_openai(prompt)
    else:
        return _generate_demo_social(request)


def _generate_demo_social(request: SocialMediaRequest) -> str:
    """Generate demo social media content"""
    
    emoji_prefix = {
        "professional": "💼",
        "casual": "✨",
        "humorous": "😄",
        "inspirational": "🌟"
    }.get(request.tone, "📢")
    
    hashtag_suffix = "\n\n#DemoMode #SocialMedia #AIContent" if request.include_hashtags else ""
    
    templates = {
        "twitter": f"""{emoji_prefix if request.include_emoji else ''} Exploring {request.topic}!

{request.call_to_action or 'What are your thoughts?'}

{hashtag_suffix}

---
DEMO: For AI-optimized tweets, add API key to backend/.env""",

        "linkedin": f"""🎯 {request.topic}

Today, I want to share insights about {request.topic} that have been transformative in my work.

Key takeaways:
• Insight #1
• Insight #2
• Insight #3

{request.call_to_action or 'What has been your experience?'}

{hashtag_suffix}

---
NOTE: This is DEMO content. For AI-personalized LinkedIn posts, add your API key.""",

        "instagram": f"""✨ {request.topic}

{emoji_prefix if request.include_emoji else ''} Sharing this moment with you all!

{request.call_to_action or 'Double tap if you agree! 💙'}

{hashtag_suffix}

---
DEMO: For AI-crafted captions, configure your API key""",

        "facebook": f"""{request.topic}

Hey everyone! 👋

I wanted to share thoughts on {request.topic}.

{request.call_to_action or 'Let me know what you think in the comments!'}

{hashtag_suffix}

---
NOTE: DEMO content. Add API key for AI-generated posts"""
    }
    
    return templates.get(request.platform.lower(), templates["twitter"])


def _extract_or_generate_hashtags(content: str, request: SocialMediaRequest) -> list:
    """Extract hashtags from content or generate them"""
    # Extract existing hashtags
    hashtags = re.findall(r'#\w+', content)
    
    if not hashtags and request.include_hashtags:
        # Generate default hashtags
        topic_words = request.topic.split()[:3]
        hashtags = [f"#{word.capitalize()}" for word in topic_words if len(word) > 3]
        hashtags.append(f"#{request.platform.capitalize()}")
    
    return hashtags[:10]  # Limit to 10 hashtags


async def _generate_alternatives(request: SocialMediaRequest) -> list:
    """Generate alternative versions of the post"""
    if ai_service.service_type == "demo":
        return [
            "Alternative version 1 (DEMO)",
            "Alternative version 2 (DEMO)",
        ]
    return None  # Can be implemented with additional AI calls


def _generate_engagement_tips(request: SocialMediaRequest) -> list:
    """Generate platform-specific engagement tips"""
    general_tips = [
        "Post during peak engagement hours for your audience",
        "Respond to comments within the first hour",
        "Use eye-catching visuals to increase engagement"
    ]
    
    platform_tips = {
        "twitter": [
            "Tweet during business hours (9 AM - 3 PM) for max engagement",
            "Use 1-2 hashtags max (more reduces engagement)",
            "Include images or GIFs to boost retweets by 150%"
        ],
        "linkedin": [
            "Post Tuesday-Thursday for best visibility",
            "Write in first person for more authentic connection",
            "Ask questions to encourage discussion in comments"
        ],
        "instagram": [
            "Post 1-2 times daily for optimal reach",
            "Use 11-30 hashtags for maximum discoverability",
            "Include location tags to increase local engagement"
        ],
        "facebook": [
            "Post in late morning or early afternoon",
            "Engage with commenters to boost post visibility",
            "Use native video for 10x more reach than links"
        ]
    }
    
    return platform_tips.get(request.platform.lower(), general_tips)


@router.get("/health")
async def health_check():
    """Health check for social media service"""
    return {
        "status": "healthy",
        "service": "social_media",
        "ai_service": ai_service.service_type
    }
