from fastapi import APIRouter, HTTPException
from models.creative import CreativeRequest, CreativeResponse
from services.ai_service import AIService
from services.utils import count_words, calculate_readability, generate_seo_score
import re

router = APIRouter()
ai_service = AIService()


@router.post("/generate", response_model=CreativeResponse)
async def generate_creative_content(request: CreativeRequest):
    """
    Generate creative content
    
    Supported content types:
    - blog: Blog posts and articles
    - story: Creative short stories
    - script: Video/podcast scripts
    - poem: Poetry
    - article: News-style articles
    """
    try:
        title, content = await _generate_creative_content(request)
        
        # Calculate metrics
        word_count = count_words(content)
        readability = calculate_readability(content)
        seo_score = generate_seo_score(content, request.keywords)
        
        # Generate tags
        tags = _generate_tags(request, content)
        
        return CreativeResponse(
            content=content,
            title=title,
            tags=tags,
            seo_score=seo_score,
            word_count=word_count,
            readability_score=readability
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def _generate_creative_content(request: CreativeRequest) -> tuple:
    """Generate creative content and title"""
    
    if ai_service.service_type == "demo":
        return _generate_demo_creative(request)
    
    # Build comprehensive AI prompt using all enhanced fields
    keywords_text = ", ".join(request.keywords) if request.keywords else "N/A"
    characters_text = ", ".join(request.main_characters) if request.main_characters else "N/A"
    
    length_guide = {
        "Short": "500-800 words",
        "Medium": "1000-1500 words",
        "Long": "2000-3000 words"
    }
    
    prompt = f"""Generate creative {request.content_type} content.

**Content Details:**
- Content Type: {request.content_type}
- Topic/Premise: {request.topic}
- Target Audience: {request.target_audience}
- Genre: {request.genre or 'Not specified'}

**Creative Elements:**
- Main Characters: {characters_text}
- Plot Idea: {request.plot_idea or 'Develop organically'}
- Setting: {request.setting or 'Choose appropriate setting'}

**Style & Tone:**
- Writing Style: {request.writing_style}
- Tone: {request.tone}
- Length: {length_guide.get(request.length, 'medium length')}
- Dialogue Heavy: {'Yes - include substantial dialogue' if request.dialogue_heavy else 'No - focus on narrative'}

**SEO & Keywords:**
- Keywords to incorporate: {keywords_text}

**Instructions:**
1. Create an engaging, attention-grabbing title
2. Write compelling {request.content_type} content in {request.writing_style} style
3. Use {request.tone} tone throughout
4. Target {request.target_audience} audience specifically
5. Incorporate the genre: {request.genre or 'appropriate genre'}
6. {'Include substantial dialogue between characters' if request.dialogue_heavy else 'Focus on narrative and description'}
7. Naturally weave in keywords: {keywords_text}
8. {'Develop these characters: ' + characters_text if request.main_characters else 'Create compelling characters'}
9. {'Follow this plot idea: ' + request.plot_idea if request.plot_idea else 'Develop an engaging plot'}
10. {'Set in: ' + request.setting if request.setting else 'Choose an appropriate setting'}
11. Make it creative, original, and captivating
12. Target length: {length_guide.get(request.length, '1000-1500 words')}

Output format:
TITLE: [creative title]

CONTENT:
[full content]

Generate only the title and content, no explanations or meta-commentary."""

    # Generate with AI
    if ai_service.service_type == "claude":
        result = await ai_service._generate_with_claude(prompt)
    elif ai_service.service_type == "openai":
        result = await ai_service._generate_with_openai(prompt)
    else:
        return _generate_demo_creative(request)
    
    # Parse title and content
    title, content = _parse_creative_response(result)
    return title, content


def _generate_demo_creative(request: CreativeRequest) -> tuple:
    """Generate demo creative content"""
    
    keywords_text = ", ".join(request.keywords[:5]) if request.keywords else "content creation, AI, creativity"
    
    templates = {
        "blog": (
            f"The Ultimate Guide to {request.topic}",
            f"""# Introduction

In today's fast-paced world, {request.topic} has become increasingly important. This guide will explore the key aspects of {request.topic} and provide actionable insights for {request.target_audience}.

## Why {request.topic} Matters

Understanding {request.topic} is crucial for success in our modern landscape. Key areas include {keywords_text}.

## Key Insights

1. **First Major Point**: Detailed exploration of the first concept
2. **Second Major Point**: In-depth analysis of another aspect
3. **Third Major Point**: Practical applications and best practices

## Practical Applications

Let's look at how you can apply these concepts in real-world scenarios.

## Conclusion

{request.topic} represents an opportunity for growth and innovation. By understanding these principles, {request.target_audience} can achieve meaningful results.

---
NOTE: This is DEMO content. For AI-created blog posts, add your API key to backend/.env"""
        ),
        
        "story": (
            f"The Tale of {request.topic}",
            f"""Once upon a time, in a world not so different from our own, there existed a fascinating story about {request.topic}.

The Beginning

Our journey starts with {keywords_text}, setting the stage for an adventure that would change everything.

The Conflict

Challenges arose, testing the limits of what was possible. The characters in our story faced obstacles that seemed insurmountable.

The Resolution

Through perseverance and creativity, solutions emerged. The story of {request.topic} reached its conclusion, leaving lasting impact on all involved.

The End

And so, the tale of {request.topic} becomes part of the larger narrative that shapes our understanding.

---
NOTE: This is DEMO content. For AI-crafted stories, add your API key to backend/.env"""
        ),
        
        "script": (
            f"Script: {request.topic}",
            f"""[OPENING SCENE]

HOST: Welcome everyone! Today we're diving deep into {request.topic}.

[CUT TO: Main Content]

HOST: Let's explore the key elements: {keywords_text}.

SEGMENT 1: Introduction
- Opening hook
- Context setting
- Preview of what's to come

SEGMENT 2: Main Content
- Deep dive into {request.topic}
- Expert insights
- Practical examples

SEGMENT 3: Conclusion
- Key takeaways
- Call to action
- Closing remarks

[END SCENE]

---
NOTE: This is DEMO content. For AI-generated scripts, add your API key to backend/.env"""
        ),
    }
    
    content_type = request.content_type.lower()
    return templates.get(content_type, templates["blog"])


def _parse_creative_response(content: str) -> tuple:
    """Parse title and content from AI response"""
    lines = content.split('\n')
    title = ""
    content_lines = []
    in_content = False
    
    for line in lines:
        if line.startswith("TITLE:"):
            title = line.replace("TITLE:", "").strip()
        elif line.startswith("CONTENT:"):
            in_content = True
        elif in_content:
            content_lines.append(line)
    
    content = "\n".join(content_lines).strip()
    
    if not title:
        # Try to extract first heading or use first line
        heading_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if heading_match:
            title = heading_match.group(1)
        else:
            title = content.split('\n')[0][:100]
    
    return title, content


def _generate_tags(request: CreativeRequest, content: str) -> list:
    """Generate content tags"""
    tags = []
    
    # Add content type
    tags.append(request.content_type)
    
    # Add style and tone
    tags.append(request.style)
    tags.append(request.tone)
    
    # Add keywords
    if request.keywords:
        tags.extend(request.keywords[:5])
    
    # Extract additional tags from topic
    topic_words = [word.lower() for word in request.topic.split() if len(word) > 4]
    tags.extend(topic_words[:3])
    
    return list(set(tags))[:10]  # Unique tags, max 10


@router.get("/health")
async def health_check():
    """Health check for creative content service"""
    return {
        "status": "healthy",
        "service": "creative",
        "ai_service": ai_service.service_type
    }
