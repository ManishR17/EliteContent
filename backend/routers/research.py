from fastapi import APIRouter, HTTPException
from models.research import ResearchRequest, ResearchResponse, Source
from services.ai_service import AIService
from services.search_service import SearchService
from services.vector_store import VectorStore
from services.cache_service import CacheService
from services.mcp_integrations import MCPIntegrations
from datetime import datetime
import hashlib
import json

router = APIRouter()
ai_service = AIService()
search_service = SearchService()
vector_store = VectorStore()
cache_service = CacheService()
mcp_integrations = MCPIntegrations()


@router.post("/generate", response_model=ResearchResponse)
async def conduct_research(request: ResearchRequest):
    """
    Conduct web research on a topic with RAG, caching, and MCP
    
    Features:
    - Multi-source search (Wikipedia, Google, GitHub, arXiv, PubMed)
    - RAG with vector store for semantic search
    - Redis caching for performance
    - AI-powered synthesis
    - Citation tracking
    - Confidence scoring
    
    Depth levels:
    - quick: 3-5 sources, brief summary
    - standard: 5-10 sources, comprehensive analysis
    - comprehensive: 10-20 sources, in-depth research
    """
    try:
        # 1. Check cache first
        cache_key = cache_service._generate_key("research", request.dict())
        cached_result = cache_service.get(cache_key)
        if cached_result:
            print("✅ Returning cached research result")
            return ResearchResponse(**cached_result)
        
        # 2. Perform multi-source search
        print(f"🔍 Searching for: {request.topic}")
        
        # Web search (Wikipedia + Google)
        web_sources = await search_service.search(request.topic, request.sources_count)
        
        # MCP sources (GitHub + arXiv + PubMed)
        mcp_sources = await mcp_integrations.search_all(request.topic, max_per_source=2)
        
        # Combine all sources
        all_sources = web_sources + mcp_sources
        sources = all_sources[:request.sources_count]
        
        print(f"✅ Found {len(sources)} sources ({len(web_sources)} web, {len(mcp_sources)} MCP)")
        
        # 3. Store in vector database for RAG
        documents = [s.content for s in sources if s.content]
        metadatas = [
            {
                "title": s.title,
                "url": s.url,
                "source_type": s.source_type
            } 
            for s in sources if s.content
        ]
        ids = [f"doc_{hashlib.md5(s.url.encode()).hexdigest()}" for s in sources if s.content]
        
        if documents:
            vector_store.add_documents(documents, metadatas, ids)
            print(f"✅ Added {len(documents)} documents to vector store")
        
        # 4. Get relevant context from vector store (RAG)
        rag_context = vector_store.get_relevant_context(request.topic, max_tokens=2000)
        
        # 5. Generate research summary with RAG
        summary, key_findings = await _generate_research_summary_with_rag(
            request, sources, rag_context
        )
        
        # 6. Generate citations
        citations = _format_citations(sources) if request.include_citations else []
        
        # 7. Calculate confidence
        confidence = _calculate_confidence(sources, request.depth)
        
        # 8. Create response
        result = ResearchResponse(
            summary=summary,
            key_findings=key_findings,
            sources=sources,
            citations=citations,
            confidence_score=confidence,
            generated_at=datetime.now()
        )
        
        # 9. Cache the result
        cache_service.set(cache_key, result.dict(), ttl=3600)
        
        return result
        
    except Exception as e:
        print(f"❌ Research error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))



async def _generate_research_summary_with_rag(
    request: ResearchRequest, 
    sources: list,
    rag_context: str
) -> tuple:
    """Generate research summary using AI with RAG context"""
    
    if ai_service.service_type == "demo":
        return _generate_demo_research(request, sources)
    
    # Build enhanced prompt with RAG context and all request fields
    sources_text = "\n\n".join([
        f"Source {i+1}: {source.title}\n{source.snippet}"
        for i, source in enumerate(sources)
    ])
    
    focus_text = "\n".join(f"- {area}" for area in request.focus_areas) if request.focus_areas else "General overview"
    sections_text = "\n".join(f"- {section}" for section in request.sections_needed) if request.sections_needed else "Standard research structure"
    
    prompt = f"""Conduct comprehensive research on: {request.topic}

**Research Question:**
{request.research_question}

**Research Parameters:**
- Depth: {request.depth}
- Academic Level: {request.academic_level}
- Citation Style: {request.citation_style}
- Target Word Count: {request.word_count or 'Not specified'}
- Sources to Use: {request.sources_count}

**Required Sections:**
{sections_text}

**Focus Areas:**
{focus_text}

**RAG Context (Relevant Information from Vector Store):**
{rag_context if rag_context else "No additional context available"}

**Current Search Results:**
{sources_text}

**Instructions:**
1. Answer the research question: {request.research_question}
2. Synthesize information from RAG context and current sources
3. Structure the response with these sections: {', '.join(request.sections_needed) if request.sections_needed else 'introduction, analysis, conclusion'}
4. Focus specifically on: {', '.join(request.focus_areas) if request.focus_areas else 'general overview'}
5. Write at {request.academic_level} academic level
6. Target approximately {request.word_count or 1000} words
7. Identify key themes and findings
8. Provide comprehensive, well-structured analysis
9. Maintain objectivity and accuracy
10. Use {request.citation_style} citation style
11. Use the RAG context to provide deeper insights
12. Ensure all focus areas are adequately covered

Output format:
SUMMARY: [comprehensive research summary]

KEY_FINDINGS:
- [finding 1]
- [finding 2]
- [finding 3]
...

Generate only the summary and key findings, no meta-commentary."""

    # Generate with AI  
    if ai_service.service_type == "claude":
        result = await ai_service._generate_with_claude(prompt)
    elif ai_service.service_type == "openai":
        result = await ai_service._generate_with_openai(prompt)
    else:
        return _generate_demo_research(request, sources)
    
    # Parse summary and findings
    summary, findings = _parse_research_response(result)
    return summary, findings


async def _generate_research_summary(request: ResearchRequest, sources: list) -> tuple:
    """Generate research summary using AI"""
    
    if ai_service.service_type == "demo":
        return _generate_demo_research(request, sources)
    
    # Build context from sources
    sources_text = "\n\n".join([
        f"Source {i+1}: {source.title}\n{source.snippet}"
        for i, source in enumerate(sources)
    ])
    
    focus_text = "\n".join(f"- {area}" for area in request.focus_areas) if request.focus_areas else "General overview"
    
    prompt = f"""Conduct comprehensive research on: {request.topic}

**Research Depth:** {request.depth}

**Available Sources:**
{sources_text}

**Focus Areas:**
{focus_text}

**Instructions:**
1. Synthesize information from all sources
2. Identify key themes and findings
3. Provide comprehensive analysis
4. Maintain objectivity and accuracy
5. Cite sources appropriately
6. Focus on the specified areas

Output format:
SUMMARY:
[Comprehensive research summary, 3-5 paragraphs]

KEY_FINDINGS:
- [Finding 1]
- [Finding 2]
- [Finding 3]
- [Finding 4]
- [Finding 5]

Generate a well-researched, professional summary."""

    # Generate with AI
    if ai_service.service_type == "claude":
        result = await ai_service._generate_with_claude(prompt)
    elif ai_service.service_type == "openai":
        result = await ai_service._generate_with_openai(prompt)
    else:
        return _generate_demo_research(request, sources)
    
    # Parse summary and findings
    summary, findings = _parse_research_response(result)
    return summary, findings


def _generate_demo_research(request: ResearchRequest, sources: list) -> tuple:
    """Generate demo research without AI"""
    
    focus_text = ", ".join(request.focus_areas) if request.focus_areas else "various aspects"
    
    summary = f"""Research on {request.topic}

Based on analysis of {len(sources)} authoritative sources, this research explores {request.topic} with emphasis on {focus_text}.

Overview:
{request.topic} represents a significant area of study with implications across multiple domains. Current research indicates growing interest and development in this field, with numerous applications and opportunities for innovation.

Key Themes:
The research reveals several important themes including practical applications, theoretical frameworks, and emerging trends. Leading experts emphasize the importance of understanding both foundational concepts and cutting-edge developments.

Synthesis:
Integrating insights from multiple sources provides a comprehensive view of {request.topic}. The evidence suggests that continued research and application in this area will yield valuable outcomes for researchers and practitioners alike.

Implications:
This research has important implications for {focus_text}, suggesting pathways for future investigation and practical implementation.

---
NOTE: This is DEMO research. For AI-powered research synthesis with real web search, add your API key to backend/.env and configure search API."""

    key_findings = [
        f"{request.topic} is a growing area of interest with multiple applications",
        "Current research shows promising developments and opportunities",
        "Expert consensus indicates the importance of comprehensive understanding",
        f"Focus areas ({focus_text}) show particular relevance",
        "Future research directions include both theoretical and practical dimensions"
    ]
    
    return summary, key_findings


def _parse_research_response(content: str) -> tuple:
    """Parse summary and key findings from AI response"""
    summary = ""
    findings = []
    
    lines = content.split('\n')
    in_summary = False
    in_findings = False
    summary_lines = []
    
    for line in lines:
        if line.startswith("SUMMARY:"):
            in_summary = True
            in_findings = False
        elif line.startswith("KEY_FINDINGS:"):
            in_summary = False
            in_findings = True
        elif in_summary:
            summary_lines.append(line)
        elif in_findings and line.strip().startswith('-'):
            finding = line.strip().lstrip('- ')
            if finding:
                findings.append(finding)
    
    summary = "\n".join(summary_lines).strip()
    
    if not summary:
        summary = content
    
    return summary, findings


def _format_citations(sources: list) -> list:
    """Format sources as citations"""
    citations = []
    for i, source in enumerate(sources, 1):
        citation = f"[{i}] {source.title}. Retrieved from {source.url}"
        citations.append(citation)
    return citations


def _calculate_confidence(sources: list, depth: str) -> float:
    """Calculate research confidence score"""
    base_confidence = {
        "quick": 0.6,
        "standard": 0.75,
        "comprehensive": 0.9
    }.get(depth, 0.7)
    
    # Adjust based on source count and quality
    source_count_factor = min(len(sources) / 10, 1.0) * 0.2
    avg_relevance = sum(s.relevance_score for s in sources) / len(sources) if sources else 0
    
    confidence = base_confidence + source_count_factor + (avg_relevance * 0.1)
    
    return min(1.0, confidence)


@router.get("/health")
async def health_check():
    """Health check for research service"""
    return {
        "status": "healthy",
        "service": "research",
        "ai_service": ai_service.service_type,
        "search_service": search_service.mode
    }
