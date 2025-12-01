import re
from typing import List, Dict, Tuple
from collections import Counter


class ATSOptimizer:
    """Service for ATS (Applicant Tracking System) optimization"""
    
    @staticmethod
    def analyze_job_description(job_description: str) -> Dict[str, any]:
        """
        Analyze job description to extract keywords and requirements
        
        Args:
            job_description: Job description text
            
        Returns:
            Dictionary with keywords, skills, and requirements
        """
        keywords = ATSOptimizer._extract_keywords(job_description)
        required_skills = ATSOptimizer._extract_skills(job_description)
        
        return {
            'keywords': keywords,
            'required_skills': required_skills,
            'keyword_frequency': Counter(keywords)
        }
    
    @staticmethod
    def calculate_ats_score(resume_text: str, job_description: str) -> Tuple[int, Dict]:
        """
        Calculate ATS compatibility score
        
        Args:
            resume_text: Full resume text
            job_description: Job description text
            
        Returns:
            Tuple of (score, analysis_details)
        """
        # Extract keywords from job description
        job_analysis = ATSOptimizer.analyze_job_description(job_description)
        job_keywords = job_analysis['keywords']
        required_skills = job_analysis['required_skills']
        
        # Extract keywords from resume
        resume_keywords = ATSOptimizer._extract_keywords(resume_text)
        resume_skills = ATSOptimizer._extract_skills(resume_text)
        
        # Calculate keyword match percentage
        matched_keywords = set(job_keywords) & set(resume_keywords)
        keyword_match_rate = len(matched_keywords) / len(set(job_keywords)) if job_keywords else 0
        
        # Calculate skill match percentage
        matched_skills = set(required_skills) & set(resume_skills)
        missing_skills = set(required_skills) - set(resume_skills)
        skill_match_rate = len(matched_skills) / len(set(required_skills)) if required_skills else 0
        
        # Calculate overall ATS score (weighted average)
        ats_score = int((keyword_match_rate * 0.4 + skill_match_rate * 0.6) * 100)
        
        analysis = {
            'matched_keywords': list(matched_keywords),
            'matched_skills': list(matched_skills),
            'missing_skills': list(missing_skills),
            'keyword_match_rate': keyword_match_rate,
            'skill_match_rate': skill_match_rate,
            'keyword_density': ATSOptimizer._calculate_keyword_density(resume_text, job_keywords)
        }
        
        return ats_score, analysis
    
    @staticmethod
    def generate_suggestions(analysis: Dict) -> List[str]:
        """
        Generate improvement suggestions based on ATS analysis
        
        Args:
            analysis: ATS analysis results
            
        Returns:
            List of suggestion strings
        """
        suggestions = []
        
        if analysis['missing_skills']:
            suggestions.append(
                f"Add these missing skills if applicable: {', '.join(analysis['missing_skills'][:5])}"
            )
        
        if analysis['keyword_match_rate'] < 0.5:
            suggestions.append(
                "Increase keyword density by incorporating more job-specific terms naturally throughout your resume"
            )
        
        if analysis['skill_match_rate'] < 0.6:
            suggestions.append(
                "Highlight more relevant skills from the job description in your skills section"
            )
        
        suggestions.append(
            "Use exact keywords from the job description to improve ATS scanning"
        )
        
        suggestions.append(
            "Avoid tables, images, and complex formatting that ATS systems may not parse correctly"
        )
        
        return suggestions
    
    @staticmethod
    def _extract_keywords(text: str) -> List[str]:
        """Extract important keywords from text"""
        # Remove common stop words
        stop_words = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at'
        }
        
        # Extract words (alphanumeric and hyphens)
        words = re.findall(r'\b[\w-]+\b', text.lower())
        
        # Filter out stop words and short words
        keywords = [
            word for word in words
            if len(word) > 2 and word not in stop_words
        ]
        
        return keywords
    
    @staticmethod
    def _extract_skills(text: str) -> List[str]:
        """Extract technical and professional skills"""
        # Expanded skills database
        common_skills = [
            # Programming Languages
            'Python', 'JavaScript', 'Java', 'C++', 'C#', 'Ruby', 'PHP', 'Swift',
            'Kotlin', 'Go', 'Rust', 'TypeScript', 'R', 'MATLAB', 'Scala',
            
            # Frameworks & Libraries
            'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'FastAPI',
            'Spring', 'Express', '.NET', 'Laravel', 'Rails',
            
            # Databases
            'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Cassandra',
            'Oracle', 'DynamoDB', 'Elasticsearch',
            
            # Cloud & DevOps
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'CI/CD',
            'Terraform', 'Ansible', 'Git', 'GitHub', 'GitLab',
            
            # Data & AI
            'Machine Learning', 'Deep Learning', 'AI', 'Data Analysis',
            'Data Science', 'TensorFlow', 'PyTorch', 'Pandas', 'NumPy',
            'Scikit-learn', 'NLP', 'Computer Vision',
            
            # Soft Skills
            'Leadership', 'Project Management', 'Agile', 'Scrum', 'Communication',
            'Problem Solving', 'Team Collaboration', 'Critical Thinking',
            'Time Management', 'Adaptability'
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in common_skills:
            # Use word boundary to avoid partial matches
            pattern = rf'\b{re.escape(skill.lower())}\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)
        
        return found_skills
    
    @staticmethod
    def _calculate_keyword_density(text: str, keywords: List[str]) -> Dict[str, float]:
        """Calculate keyword density for important terms"""
        text_lower = text.lower()
        total_words = len(text_lower.split())
        
        keyword_density = {}
        for keyword in set(keywords[:20]):  # Top 20 keywords
            count = text_lower.count(keyword.lower())
            density = (count / total_words * 100) if total_words > 0 else 0
            keyword_density[keyword] = round(density, 2)
        
        return keyword_density
