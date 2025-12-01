import io
import re
from typing import List
from models.resume import ParsedResume

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    from docx import Document
except ImportError:
    Document = None


class ResumeParser:
    """Service for parsing resume files (PDF, DOCX)"""
    
    @staticmethod
    async def parse_resume(file_content: bytes, filename: str) -> ParsedResume:
        """
        Parse resume from file content
        
        Args:
            file_content: Raw file bytes
            filename: Original filename
            
        Returns:
            ParsedResume object with extracted data
        """
        if filename.lower().endswith('.pdf'):
            raw_text = ResumeParser._parse_pdf(file_content)
        elif filename.lower().endswith('.docx'):
            raw_text = ResumeParser._parse_docx(file_content)
        else:
            raise ValueError(f"Unsupported file format: {filename}")
        
        # Extract skills and sections
        skills = ResumeParser._extract_skills(raw_text)
        sections = ResumeParser._extract_sections(raw_text)
        
        return ParsedResume(
            raw_text=raw_text,
            sections=sections,
            skills=skills
        )
    
    @staticmethod
    def _parse_pdf(file_content: bytes) -> str:
        """Extract text from PDF file"""
        if PyPDF2 is None:
            raise ImportError("PyPDF2 is not installed. Install with: pip install PyPDF2")
        
        try:
            pdf_file = io.BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {str(e)}")
    
    @staticmethod
    def _parse_docx(file_content: bytes) -> str:
        """Extract text from DOCX file"""
        if Document is None:
            raise ImportError("python-docx is not installed. Install with: pip install python-docx")
        
        try:
            docx_file = io.BytesIO(file_content)
            doc = Document(docx_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
        except Exception as e:
            raise ValueError(f"Failed to parse DOCX: {str(e)}")
    
    @staticmethod
    def _extract_skills(text: str) -> List[str]:
        """Extract skills from resume text (basic implementation)"""
        # Common technical skills keywords
        common_skills = [
            'Python', 'JavaScript', 'Java', 'C++', 'React', 'Angular', 'Vue',
            'Node.js', 'SQL', 'MongoDB', 'AWS', 'Azure', 'Docker', 'Kubernetes',
            'Git', 'Agile', 'Scrum', 'Machine Learning', 'AI', 'Data Analysis',
            'Project Management', 'Communication', 'Leadership', 'Problem Solving'
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in common_skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    @staticmethod
    def _extract_sections(text: str) -> dict:
        """Extract resume sections (basic implementation)"""
        sections = {}
        
        # Common section headers
        section_headers = [
            'experience', 'education', 'skills', 'projects',
            'certifications', 'summary', 'objective'
        ]
        
        for header in section_headers:
            pattern = rf'\b{header}\b.*?(?=\n\n|\Z)'
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                sections[header] = match.group(0)
        
        return sections
