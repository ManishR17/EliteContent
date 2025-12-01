"""Multi-agent system for high-quality content generation"""
import json
from typing import Dict, List, Optional
from services.ai_service import AIService


class PlannerAgent:
    """Plans content generation strategy"""
    
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service
    
    async def create_plan(self, request: Dict) -> Dict:
        """
        Create step-by-step plan for content generation
        
        Args:
            request: Content generation request
            
        Returns:
            Detailed plan with steps and strategy
        """
        task_type = request.get('type', 'content')
        topic = request.get('topic', '')
        requirements = request.get('requirements', [])
        
        prompt = f"""You are a planning agent. Create a detailed plan for generating {task_type}.

**Task:** {topic}
**Requirements:** {', '.join(requirements) if requirements else 'None specified'}

Create a JSON plan with:
1. "strategy": Overall approach (2-3 sentences)
2. "steps": List of specific steps to follow
3. "key_points": Important points to cover
4. "tone": Recommended tone
5. "structure": Recommended structure

Output ONLY valid JSON, no other text.
"""
        
        if self.ai_service.service_type == "demo":
            return self._demo_plan(task_type, topic)
        
        try:
            result = await self.ai_service.generate(prompt, max_tokens=1000)
            
            # Try to parse JSON
            # Find JSON in response
            start = result.find('{')
            end = result.rfind('}') + 1
            if start != -1 and end > start:
                json_str = result[start:end]
                plan = json.loads(json_str)
                return plan
            else:
                return self._demo_plan(task_type, topic)
        except:
            return self._demo_plan(task_type, topic)
    
    def _demo_plan(self, task_type: str, topic: str) -> Dict:
        """Generate demo plan"""
        return {
            "strategy": f"Create comprehensive {task_type} about {topic} with clear structure and engaging content",
            "steps": [
                "Research and gather information",
                "Outline main sections",
                "Write introduction",
                "Develop main content",
                "Add supporting details",
                "Write conclusion",
                "Review and refine"
            ],
            "key_points": [
                f"Focus on {topic}",
                "Maintain clarity and coherence",
                "Use appropriate examples",
                "Ensure factual accuracy"
            ],
            "tone": "professional and informative",
            "structure": "introduction, body paragraphs, conclusion"
        }


class WriterAgent:
    """Generates content following plan"""
    
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service
    
    async def write_content(
        self, 
        plan: Dict, 
        context: str,
        requirements: Dict
    ) -> str:
        """
        Write content based on plan
        
        Args:
            plan: Plan from PlannerAgent
            context: Additional context (RAG, templates, etc.)
            requirements: Specific requirements
            
        Returns:
            Generated content
        """
        strategy = plan.get('strategy', '')
        steps = plan.get('steps', [])
        key_points = plan.get('key_points', [])
        tone = plan.get('tone', 'professional')
        
        prompt = f"""You are a writer agent. Follow this plan to create high-quality content:

**Strategy:** {strategy}

**Steps to Follow:**
{chr(10).join(f'{i+1}. {step}' for i, step in enumerate(steps))}

**Key Points to Cover:**
{chr(10).join(f'- {point}' for point in key_points)}

**Tone:** {tone}

**Additional Context:**
{context}

**Requirements:**
{json.dumps(requirements, indent=2)}

Write comprehensive, well-structured content that:
- Follows ALL steps in order
- Covers ALL key points
- Maintains the specified tone
- Uses the context effectively
- Meets all requirements

Generate the content now:
"""
        
        if self.ai_service.service_type == "demo":
            return self._demo_content(plan, requirements)
        
        result = await self.ai_service.generate(prompt, max_tokens=2000)
        return result
    
    def _demo_content(self, plan: Dict, requirements: Dict) -> str:
        """Generate demo content"""
        topic = requirements.get('topic', 'the subject')
        return f"""# {topic.title()}

## Introduction
This comprehensive guide explores {topic} in detail, providing valuable insights and practical information.

## Main Content
Following the strategic approach outlined in our plan, we'll cover the key aspects of {topic}. Each section builds upon the previous one to create a cohesive understanding.

### Key Points
{chr(10).join(f'- {point}' for point in plan.get('key_points', ['Point 1', 'Point 2', 'Point 3']))}

## Conclusion
In summary, {topic} is an important subject that requires careful consideration and understanding. This guide has provided a structured approach to exploring the topic comprehensively.

---
*Note: This is a DEMO output. For AI-generated content, configure your API keys.*
"""


class CriticAgent:
    """Reviews and improves content"""
    
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service
    
    async def review_content(
        self, 
        content: str, 
        criteria: Dict
    ) -> Dict:
        """
        Review content and suggest improvements
        
        Args:
            content: Content to review
            criteria: Review criteria
            
        Returns:
            Review with score, strengths, weaknesses, improvements
        """
        prompt = f"""You are a critic agent. Review this content critically:

**Content:**
{content}

**Criteria:**
{json.dumps(criteria, indent=2)}

Evaluate based on:
1. Clarity and coherence
2. Completeness (covers all required points)
3. Accuracy and factual correctness
4. Tone and style appropriateness
5. Structure and organization
6. Grammar and language quality

Provide a JSON response with:
{{
    "score": <0-100>,
    "strengths": [<list of strengths>],
    "weaknesses": [<list of weaknesses>],
    "improvements": [<specific suggestions>],
    "missing_elements": [<what's missing>],
    "hallucinations": [<any factual errors or made-up info>]
}}

Output ONLY valid JSON.
"""
        
        if self.ai_service.service_type == "demo":
            return self._demo_review(content)
        
        try:
            result = await self.ai_service.generate(prompt, max_tokens=1000)
            
            # Parse JSON
            start = result.find('{')
            end = result.rfind('}') + 1
            if start != -1 and end > start:
                json_str = result[start:end]
                review = json.loads(json_str)
                return review
            else:
                return self._demo_review(content)
        except:
            return self._demo_review(content)
    
    async def improve_content(
        self, 
        content: str, 
        review: Dict
    ) -> str:
        """
        Apply improvements based on review
        
        Args:
            content: Original content
            review: Review from review_content
            
        Returns:
            Improved content
        """
        weaknesses = review.get('weaknesses', [])
        improvements = review.get('improvements', [])
        missing = review.get('missing_elements', [])
        
        prompt = f"""Improve this content based on the review:

**Original Content:**
{content}

**Weaknesses Found:**
{chr(10).join(f'- {w}' for w in weaknesses)}

**Specific Improvements Needed:**
{chr(10).join(f'- {i}' for i in improvements)}

**Missing Elements:**
{chr(10).join(f'- {m}' for m in missing)}

Generate an improved version that:
- Addresses ALL weaknesses
- Implements ALL suggested improvements
- Adds ALL missing elements
- Maintains the original intent and structure
- Improves overall quality

Improved content:
"""
        
        if self.ai_service.service_type == "demo":
            return content + "\n\n[IMPROVED VERSION - Demo mode]"
        
        result = await self.ai_service.generate(prompt, max_tokens=2000)
        return result
    
    def _demo_review(self, content: str) -> Dict:
        """Generate demo review"""
        word_count = len(content.split())
        
        return {
            "score": 75,
            "strengths": [
                "Clear structure and organization",
                "Covers main points effectively",
                "Appropriate tone for audience"
            ],
            "weaknesses": [
                "Could use more specific examples",
                "Some sections need more detail",
                "Conclusion could be stronger"
            ],
            "improvements": [
                "Add concrete examples in main sections",
                "Expand on key concepts with more detail",
                "Strengthen conclusion with actionable takeaways"
            ],
            "missing_elements": [
                "Specific examples or case studies",
                "Data or statistics to support claims"
            ],
            "hallucinations": []
        }


class MultiAgentOrchestrator:
    """Orchestrates multi-agent workflow for content generation"""
    
    def __init__(self):
        self.ai_service = AIService()
        self.planner = PlannerAgent(self.ai_service)
        self.writer = WriterAgent(self.ai_service)
        self.critic = CriticAgent(self.ai_service)
    
    async def generate_content(
        self, 
        request: Dict,
        context: str = "",
        quality_threshold: int = 80
    ) -> Dict:
        """
        Full multi-agent generation workflow
        
        Args:
            request: Content generation request
            context: Additional context (RAG, etc.)
            quality_threshold: Minimum quality score (0-100)
            
        Returns:
            Complete result with content, plan, review, iterations
        """
        print("🤖 Multi-Agent System: Starting generation...")
        
        # Step 1: Plan
        print("  📋 Planner Agent: Creating plan...")
        plan = await self.planner.create_plan(request)
        print(f"  ✅ Plan created with {len(plan.get('steps', []))} steps")
        
        # Step 2: Write
        print("  ✍️  Writer Agent: Generating content...")
        draft = await self.writer.write_content(plan, context, request)
        print(f"  ✅ Draft generated ({len(draft.split())} words)")
        
        # Step 3: Review
        print("  🔍 Critic Agent: Reviewing content...")
        review = await self.critic.review_content(draft, request.get('criteria', {}))
        score = review.get('score', 0)
        print(f"  ✅ Review complete (Score: {score}/100)")
        
        iterations = [
            {
                'iteration': 1,
                'content': draft,
                'score': score,
                'review': review
            }
        ]
        
        # Step 4: Improve (if needed)
        final_content = draft
        if score < quality_threshold:
            print(f"  🔄 Score below threshold ({quality_threshold}), improving...")
            improved = await self.critic.improve_content(draft, review)
            
            # Re-review
            final_review = await self.critic.review_content(improved, request.get('criteria', {}))
            final_score = final_review.get('score', score)
            
            iterations.append({
                'iteration': 2,
                'content': improved,
                'score': final_score,
                'review': final_review
            })
            
            final_content = improved
            print(f"  ✅ Improved (New score: {final_score}/100)")
        
        print("🎉 Multi-Agent System: Generation complete!")
        
        return {
            'content': final_content,
            'plan': plan,
            'review': iterations[-1]['review'],
            'iterations': iterations,
            'final_score': iterations[-1]['score'],
            'improvement': iterations[-1]['score'] - iterations[0]['score'] if len(iterations) > 1 else 0,
            'agent_system': 'multi-agent-v1'
        }
    
    async def generate_with_self_refinement(
        self,
        request: Dict,
        context: str = "",
        max_iterations: int = 3,
        target_score: int = 85
    ) -> Dict:
        """
        Generate with self-refinement loop
        
        Args:
            request: Content generation request
            context: Additional context
            max_iterations: Maximum refinement iterations
            target_score: Target quality score
            
        Returns:
            Result with refinement history
        """
        print(f"🔄 Starting self-refinement (max {max_iterations} iterations, target: {target_score})")
        
        # Initial generation
        result = await self.generate_content(request, context, quality_threshold=target_score)
        
        current_score = result['final_score']
        iteration_count = len(result['iterations'])
        
        # Continue refining if needed
        while current_score < target_score and iteration_count < max_iterations:
            print(f"  🔄 Refinement iteration {iteration_count + 1}...")
            
            # Use previous review to improve
            improved = await self.critic.improve_content(
                result['content'],
                result['review']
            )
            
            # Review again
            new_review = await self.critic.review_content(improved, request.get('criteria', {}))
            new_score = new_review.get('score', current_score)
            
            result['iterations'].append({
                'iteration': iteration_count + 1,
                'content': improved,
                'score': new_score,
                'review': new_review
            })
            
            result['content'] = improved
            result['review'] = new_review
            result['final_score'] = new_score
            result['improvement'] = new_score - result['iterations'][0]['score']
            
            current_score = new_score
            iteration_count += 1
            
            print(f"  ✅ Iteration {iteration_count} complete (Score: {new_score}/100)")
            
            # Stop if score decreased
            if new_score < current_score:
                print("  ⚠️  Score decreased, stopping refinement")
                break
        
        print(f"🎉 Self-refinement complete! Final score: {current_score}/100")
        
        return result
