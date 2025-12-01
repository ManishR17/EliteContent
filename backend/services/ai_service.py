import os
from typing import Optional
from models.resume import ParsedResume, ResumeGenerationRequest

# AI Service can be configured to use different providers
AI_SERVICE_TYPE = os.getenv("AI_SERVICE", "demo")  # demo, claude, openai


class AIService:
    """Service for AI-powered resume generation"""
    
    def __init__(self):
        self.service_type = AI_SERVICE_TYPE
        self.client = self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the AI client based on configuration"""
        if self.service_type == "demo":
            print("🎭 Running in DEMO mode - generating sample resumes without AI API")
            return "demo"
        
        elif self.service_type == "claude":
            try:
                from anthropic import Anthropic
                api_key = os.getenv("ANTHROPIC_API_KEY")
                if not api_key or api_key == "placeholder-key-here":
                    print("⚠️  WARNING: ANTHROPIC_API_KEY not configured. Falling back to DEMO mode.")
                    print("📝 Please add your API key to backend/.env file")
                    self.service_type = "demo"
                    return "demo"
                return Anthropic(api_key=api_key)
            except ImportError:
                raise ImportError("Anthropic library not installed. Install with: pip install anthropic")
        
        elif self.service_type == "openai":
            try:
                from openai import OpenAI
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key or api_key == "placeholder-key-here":
                    print("⚠️  WARNING: OPENAI_API_KEY not configured. Falling back to DEMO mode.")
                    print("📝 Please add your API key to backend/.env file")
                    self.service_type = "demo"
                    return "demo"
                return OpenAI(api_key=api_key)
            except ImportError:
                raise ImportError("OpenAI library not installed. Install with: pip install openai")
        
        else:
            print(f"⚠️  Unknown AI service '{self.service_type}'. Falling back to DEMO mode.")
            self.service_type = "demo"
            return "demo"

    
    async def generate_tailored_resume(
        self,
        parsed_resume: ParsedResume,
        request: ResumeGenerationRequest
    ) -> str:
        """
        Generate a tailored, ATS-friendly resume using AI
        
        Args:
            parsed_resume: Parsed resume data
            request: Resume generation parameters
            
        Returns:
            Generated resume text
        """
        if self.service_type == "demo":
            return self._generate_demo_resume(parsed_resume, request)
        
        prompt = self._build_prompt(parsed_resume, request)
        
        if self.service_type == "claude":
            return await self._generate_with_claude(prompt)
        elif self.service_type == "openai":
            return await self._generate_with_openai(prompt)
        else:
            return self._generate_demo_resume(parsed_resume, request)

    
    def _generate_demo_resume(
        self,
        parsed_resume: ParsedResume,
        request: ResumeGenerationRequest
    ) -> str:
        """Generate a demo resume without API call"""
        
        skills_str = ", ".join(request.skills_to_highlight[:5]) if request.skills_to_highlight else "Python, JavaScript, React"
        
        demo_resume = f"""
{request.target_role.upper()}

PROFESSIONAL SUMMARY
Results-driven {request.experience_level} professional with expertise in {skills_str}. Proven track record of delivering high-impact solutions and driving business growth. Seeking to leverage technical skills and leadership experience in a {request.target_role} role.

CORE COMPETENCIES
• {" • ".join(request.skills_to_highlight[:8] if request.skills_to_highlight else ["Python", "JavaScript", "React", "Node.js", "AWS", "Docker", "Agile", "CI/CD"])}

PROFESSIONAL EXPERIENCE

Senior Software Engineer | TechCorp Inc.
January 2021 - Present
• Designed and implemented scalable microservices architecture serving 10M+ users
• Led cross-functional team of 5 engineers in developing cloud-native applications
• Reduced system latency by 40% through performance optimization and caching strategies
• Mentored junior developers and conducted code reviews to maintain code quality
{"• " + request.additional_achievements if request.additional_achievements else ""}

Software Engineer | Innovation Labs
June 2018 - December 2020
• Developed full-stack web applications using modern frameworks and best practices
• Collaborated with product team to deliver features aligned with business objectives
• Implemented CI/CD pipelines reducing deployment time by 60%
• Participated in agile ceremonies and contributed to sprint planning

Junior Developer | StartupXYZ
January 2016 - May 2018
• Built responsive web interfaces using HTML, CSS, and JavaScript
• Worked with REST APIs and integrated third-party services
• Participated in code reviews and learned industry best practices
• Contributed to open-source projects and technical documentation

EDUCATION

Bachelor of Science in Computer Science
University of Technology | 2015
GPA: 3.8/4.0

CERTIFICATIONS
• AWS Certified Solutions Architect
• Certified Kubernetes Administrator (CKA)
• Professional Scrum Master (PSM I)

TECHNICAL SKILLS
Languages: {skills_str}
Frameworks: React, Node.js, Django, Spring Boot
Cloud: AWS, Azure, Google Cloud Platform
Tools: Docker, Kubernetes, Git, Jenkins, Terraform

---
NOTE: This is a DEMO resume generated without AI. 
For personalized, AI-tailored resumes, add your API key to backend/.env
Get free trial credits at: https://console.anthropic.com/
"""
        return demo_resume.strip()
    
    def _build_prompt(
        self,
        parsed_resume: ParsedResume,
        request: ResumeGenerationRequest
    ) -> str:
        """Build the AI prompt for resume generation"""
        
        skills_str = ", ".join(request.skills_to_highlight) if request.skills_to_highlight else "N/A"
        achievements_str = request.additional_achievements or "N/A"
        
        prompt = f"""You are an expert ATS Resume Writer with deep knowledge of HR standards, job-market expectations, and keyword optimization.

**Your Task:**
Generate a tailored, ATS-friendly resume that aligns perfectly with the provided job description. The resume should highlight the candidate's strengths with correct structure, professional tone, and strategic keyword placement.

**Context:**

**Original Resume Content:**
{parsed_resume.raw_text}

**Job Description:**
{request.job_description}

**Target Role:** {request.target_role}
**Experience Level:** {request.experience_level}
**Skills to Highlight:** {skills_str}
**Tone Preference:** {request.tone_preference}
**Format Type:** {request.format_type}
**Additional Achievements:** {achievements_str}

**Requirements:**

1. **ATS Optimization:**
   - Use keywords from the job description naturally throughout the resume
   - Use standard section headings (Summary, Experience, Education, Skills)
   - Avoid tables, images, headers/footers, and complex formatting
   - Use simple bullet points and clear hierarchy

2. **Structure:**
   - Professional Summary (3-4 lines tailored to the role)
   - Work Experience (with quantified achievements)
   - Education
   - Skills (categorized if applicable)
   - Certifications (if applicable)

3. **Tone:**
   - Match the specified tone: {request.tone_preference}
   - Use action verbs and achievement-oriented language
   - Be specific and quantify results where possible

4. **Format:**
   - Follow the {request.format_type} style
   - Keep it clean, scannable, and professional
   - Use consistent formatting throughout

5. **Content Focus:**
   - Emphasize the skills: {skills_str}
   - Incorporate achievements: {achievements_str}
   - Align experience with job requirements
   - Show progression and growth

**Output:**
Provide ONLY the formatted resume content. Do not include any explanations, notes, or meta-commentary. The output should be ready to copy-paste into a document.
"""
        
        return prompt
    
    async def _generate_with_claude(self, prompt: str) -> str:
        """Generate resume using Claude API"""
        try:
            max_tokens = int(os.getenv("MAX_TOKENS", "4000"))
            temperature = float(os.getenv("TEMPERATURE", "0.7"))
            
            message = self.client.messages.create(
                model=os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022"),
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return message.content[0].text
        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")
    
    async def _generate_with_openai(self, prompt: str) -> str:
        """Generate resume using OpenAI API"""
        try:
            max_tokens = int(os.getenv("MAX_TOKENS", "4000"))
            temperature = float(os.getenv("TEMPERATURE", "0.7"))
            
            response = self.client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4"),
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": "You are an expert ATS Resume Writer."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
