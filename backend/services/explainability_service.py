"""Explainability service for AI outputs - builds user trust"""
from typing import Dict, List, Optional
from services.ai_service import AIService
import json


class ExplainabilityService:
    """Explains why AI generated specific content"""
    
    def __init__(self):
        self.ai_service = AIService()
    
    async def explain_output(
        self,
        content: str,
        input_data: Dict,
        content_type: str
    ) -> Dict:
        """
        Generate comprehensive explanation for AI output
        
        Args:
            content: Generated content
            input_data: Original input/request
            content_type: Type of content (resume, email, etc.)
            
        Returns:
            Detailed explanation with reasoning
        """
        prompt = f"""You are an explainability agent. Explain why you generated this {content_type}:

**User Input:**
{json.dumps(input_data, indent=2)}

**Generated Output:**
{content[:500]}... (truncated)

Provide a clear, educational explanation covering:

1. **Key Decisions**: What major choices did you make and why?
2. **Word Choices**: Why did you use specific words or phrases?
3. **Structure**: Why did you organize it this way?
4. **Input Influence**: How did the user's input shape the output?
5. **Effectiveness**: What makes this output effective for its purpose?
6. **Alternatives**: What other approaches were considered?

Be specific, cite examples from the output, and help the user understand your reasoning.

Output as JSON:
{{
    "summary": "Brief overview of approach",
    "key_decisions": [
        {{"decision": "...", "reasoning": "..."}}
    ],
    "word_choices": [
        {{"phrase": "...", "reason": "..."}}
    ],
    "structure_rationale": "...",
    "input_influence": "...",
    "effectiveness_factors": [...],
    "alternatives_considered": [...]
}}
"""
        
        if self.ai_service.service_type == "demo":
            return self._demo_explanation(content_type, input_data)
        
        try:
            result = await self.ai_service.generate(prompt, max_tokens=1500)
            
            # Parse JSON
            start = result.find('{')
            end = result.rfind('}') + 1
            if start != -1 and end > start:
                json_str = result[start:end]
                explanation = json.loads(json_str)
                
                # Add confidence score
                explanation['confidence'] = self._calculate_confidence(content, input_data)
                explanation['reasoning_chain'] = self._extract_reasoning_chain(explanation)
                
                return explanation
            else:
                return self._demo_explanation(content_type, input_data)
        except Exception as e:
            print(f"Explanation error: {str(e)}")
            return self._demo_explanation(content_type, input_data)
    
    async def explain_resume_choices(
        self, 
        resume: str, 
        job_description: str,
        original_resume: Optional[str] = None
    ) -> Dict:
        """
        Explain resume generation/optimization choices
        
        Args:
            resume: Generated/optimized resume
            job_description: Target job description
            original_resume: Original resume (if optimization)
            
        Returns:
            Resume-specific explanation
        """
        prompt = f"""Explain the resume optimization choices:

**Job Description:**
{job_description[:300]}...

**Generated Resume:**
{resume[:400]}...

{"**Original Resume:**" + original_resume[:300] + "..." if original_resume else ""}

Explain:
1. How resume was tailored to job requirements
2. Which keywords were emphasized and why
3. How experience was highlighted
4. What sections were prioritized
5. ATS optimization strategies used
6. Why specific achievements were featured

Provide actionable insights the user can learn from.
"""
        
        if self.ai_service.service_type == "demo":
            return {
                "summary": "Resume optimized for ATS and job requirements",
                "keyword_strategy": [
                    "Emphasized technical skills matching job description",
                    "Included industry-specific terminology",
                    "Highlighted relevant experience first"
                ],
                "ats_optimizations": [
                    "Used standard section headers",
                    "Avoided graphics and tables",
                    "Included keywords naturally in context"
                ],
                "experience_highlighting": [
                    "Quantified achievements with metrics",
                    "Used action verbs",
                    "Focused on relevant projects"
                ],
                "confidence": 0.85
            }
        
        result = await self.ai_service.generate(prompt, max_tokens=1000)
        return self._parse_explanation(result)
    
    async def explain_social_media_strategy(
        self, 
        post: str, 
        platform: str,
        topic: str
    ) -> Dict:
        """
        Explain social media post strategy
        
        Args:
            post: Generated post
            platform: Social media platform
            topic: Post topic
            
        Returns:
            Social media strategy explanation
        """
        prompt = f"""Explain the social media strategy for this {platform} post:

**Topic:** {topic}
**Platform:** {platform}
**Post:**
{post}

Explain:
1. Why this tone/style for {platform}
2. Hashtag selection strategy
3. Engagement optimization techniques
4. Character limit considerations
5. Call-to-action placement
6. Best posting time recommendation

Help user understand social media best practices.
"""
        
        if self.ai_service.service_type == "demo":
            return {
                "summary": f"Post optimized for {platform} engagement",
                "tone_choice": f"Conversational and engaging, appropriate for {platform} audience",
                "hashtag_strategy": [
                    "Mix of popular and niche hashtags",
                    "Relevant to topic and trending",
                    "Platform-appropriate count"
                ],
                "engagement_tactics": [
                    "Question to encourage comments",
                    "Clear call-to-action",
                    "Emoji usage for visual appeal"
                ],
                "platform_optimization": [
                    f"Optimized for {platform} character limits",
                    "Format suitable for mobile viewing",
                    "Timing aligned with peak engagement hours"
                ],
                "confidence": 0.82
            }
        
        result = await self.ai_service.generate(prompt, max_tokens=1000)
        return self._parse_explanation(result)
    
    async def explain_document_structure(
        self, 
        document: str, 
        doc_type: str,
        purpose: str
    ) -> Dict:
        """
        Explain document structure and organization choices
        
        Args:
            document: Generated document
            doc_type: Type of document
            purpose: Document purpose
            
        Returns:
            Document structure explanation
        """
        prompt = f"""Explain the structure and organization of this {doc_type}:

**Purpose:** {purpose}
**Document Type:** {doc_type}
**Content:**
{document[:500]}...

Explain:
1. Why this structure was chosen
2. Section ordering rationale
3. Tone and formality level
4. Paragraph organization
5. Introduction/conclusion strategy
6. How structure serves the purpose

Provide insights on effective document writing.
"""
        
        if self.ai_service.service_type == "demo":
            return {
                "summary": f"{doc_type} structured for maximum impact",
                "structure_rationale": f"Organized to clearly communicate {purpose}",
                "section_ordering": [
                    "Introduction sets context",
                    "Body presents main points logically",
                    "Conclusion reinforces key messages"
                ],
                "tone_choice": "Professional and authoritative, appropriate for business context",
                "effectiveness_factors": [
                    "Clear hierarchy of information",
                    "Logical flow between sections",
                    "Concise yet comprehensive coverage"
                ],
                "confidence": 0.88
            }
        
        result = await self.ai_service.generate(prompt, max_tokens=1000)
        return self._parse_explanation(result)
    
    def _calculate_confidence(self, content: str, input_data: Dict) -> float:
        """
        Calculate confidence score for explanation
        
        Args:
            content: Generated content
            input_data: Input data
            
        Returns:
            Confidence score (0-1)
        """
        # Simplified confidence calculation
        # In production, use more sophisticated metrics
        
        factors = []
        
        # Content length factor
        word_count = len(content.split())
        if word_count > 100:
            factors.append(0.9)
        elif word_count > 50:
            factors.append(0.7)
        else:
            factors.append(0.5)
        
        # Input completeness factor
        input_fields = len(input_data)
        if input_fields > 5:
            factors.append(0.9)
        elif input_fields > 3:
            factors.append(0.7)
        else:
            factors.append(0.6)
        
        # AI service factor
        if self.ai_service.service_type != "demo":
            factors.append(0.95)
        else:
            factors.append(0.6)
        
        # Average confidence
        return round(sum(factors) / len(factors), 2)
    
    def _extract_reasoning_chain(self, explanation: Dict) -> List[str]:
        """Extract reasoning chain from explanation"""
        chain = []
        
        if 'key_decisions' in explanation:
            for decision in explanation['key_decisions']:
                if isinstance(decision, dict):
                    chain.append(f"{decision.get('decision', '')}: {decision.get('reasoning', '')}")
                else:
                    chain.append(str(decision))
        
        return chain
    
    def _parse_explanation(self, text: str) -> Dict:
        """Parse explanation text into structured format"""
        try:
            # Try to find JSON
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
        except:
            pass
        
        # Fallback to text explanation
        return {
            "summary": text[:200],
            "full_explanation": text,
            "confidence": 0.7
        }
    
    def _demo_explanation(self, content_type: str, input_data: Dict) -> Dict:
        """Generate demo explanation"""
        return {
            "summary": f"Generated {content_type} based on your requirements using AI best practices",
            "key_decisions": [
                {
                    "decision": "Content structure",
                    "reasoning": "Organized logically to maximize clarity and impact"
                },
                {
                    "decision": "Tone and style",
                    "reasoning": "Matched to target audience and purpose"
                },
                {
                    "decision": "Key points emphasis",
                    "reasoning": "Highlighted most important information first"
                }
            ],
            "word_choices": [
                {
                    "phrase": "Professional terminology",
                    "reason": "Establishes credibility and expertise"
                },
                {
                    "phrase": "Action-oriented language",
                    "reason": "Creates engagement and drives results"
                }
            ],
            "structure_rationale": "Clear beginning, middle, and end for easy comprehension",
            "input_influence": "Your input directly shaped the content focus and direction",
            "effectiveness_factors": [
                "Clear and concise communication",
                "Appropriate tone for context",
                "Well-organized information flow",
                "Engaging and actionable content"
            ],
            "alternatives_considered": [
                "Different structural approaches",
                "Various tone options",
                "Alternative emphasis points"
            ],
            "confidence": self._calculate_confidence("demo content", input_data),
            "reasoning_chain": [
                "Analyzed input requirements",
                "Determined optimal structure",
                "Selected appropriate tone",
                "Generated content following best practices"
            ]
        }
