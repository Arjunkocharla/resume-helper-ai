import json
import logging
import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from docx import Document
from pydantic import ValidationError

from ..contracts import ResumeAST, Section, Role, Bullet, validate_or_raise
from .skills_categorization_agent import SkillsCategorizationAgent

logger = logging.getLogger(__name__)


class ResumeParserAgent:
    """Agent responsible for parsing resumes and building ResumeAST."""
    
    def __init__(self, skills_agent: SkillsCategorizationAgent):
        self.skills_agent = skills_agent
        
        self.section_patterns = {
            'header': r'^(?:name|contact|email|phone|address|linkedin|github)',
            'experience': r'^(?:work\s+experience|employment|professional\s+experience|career)',
            'education': r'^(?:education|academic|degree|university|college)',
            'skills': r'^(?:skills|technical\s+skills|technologies|tools|languages)',
            'projects': r'^(?:projects|project\s+experience|technical\s+projects)',
            'certifications': r'^(?:certifications|certificates|accreditations)',
            'summary': r'^(?:summary|profile|objective|professional\s+summary)'
        }
    
    def parse_resume(self, file_path: str) -> ResumeAST:
        """
        Parse resume file and build ResumeAST.
        
        Args:
            file_path: Path to DOCX or PDF file
            
        Returns:
            ResumeAST: Structured resume data
            
        Raises:
            ValueError: If file format is unsupported
            ValidationError: If AST construction fails
        """
        try:
            file_path = Path(file_path)
            
            if file_path.suffix.lower() == '.docx':
                return self._parse_docx(file_path)
            elif file_path.suffix.lower() == '.pdf':
                return self._parse_pdf(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_path.suffix}")
                
        except Exception as e:
            logger.error(f"Failed to parse resume: {e}")
            raise
    
    def _parse_docx(self, file_path: Path) -> ResumeAST:
        """Parse DOCX file and build ResumeAST."""
        logger.info(f"Parsing DOCX file: {file_path}")
        
        doc = Document(file_path)
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        
        # Build AST components
        sections = self._identify_sections(paragraphs)
        roles = self._extract_roles(paragraphs, sections)
        bullets = self._extract_bullets(paragraphs, roles)
        skills_buckets = self._extract_skills(paragraphs)
        
        # Construct and validate ResumeAST
        resume_ast = ResumeAST(
            sections=sections,
            roles=roles,
            bullets=bullets,
            skills_buckets=skills_buckets
        )
        
        logger.info(f"Successfully parsed resume into {len(sections)} sections, {len(roles)} roles, {len(bullets)} bullets")
        return resume_ast
    
    def _parse_pdf(self, file_path: Path) -> ResumeAST:
        """Parse PDF file and build ResumeAST."""
        logger.info(f"Parsing PDF file: {file_path}")
        
        try:
            import PyPDF2
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                paragraphs = []
                
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    # Split text into lines and clean them
                    lines = text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line:
                            paragraphs.append(line)
            
            logger.info(f"Extracted {len(paragraphs)} text lines from PDF")
            
            # Reconstruct fragmented text by merging broken lines
            reconstructed_paragraphs = self._reconstruct_fragmented_text(paragraphs)
            logger.info(f"Reconstructed into {len(reconstructed_paragraphs)} coherent paragraphs")
            
            # Build AST components (same logic as DOCX)
            sections = self._identify_sections(reconstructed_paragraphs)
            roles = self._extract_roles(reconstructed_paragraphs, sections)
            bullets = self._extract_bullets(reconstructed_paragraphs, roles)
            skills_buckets = self._extract_skills(reconstructed_paragraphs)
            
            # Construct and validate ResumeAST
            resume_ast = ResumeAST(
                sections=sections,
                roles=roles,
                bullets=bullets,
                skills_buckets=skills_buckets
            )
            
            logger.info(f"Successfully parsed PDF resume into {len(sections)} sections, {len(roles)} roles, {len(bullets)} bullets")
            return resume_ast
            
        except ImportError:
            raise ImportError("PyPDF2 is required for PDF parsing. Install with: pip install PyPDF2")
        except Exception as e:
            logger.error(f"PDF parsing failed: {e}")
            raise
    
    def _reconstruct_fragmented_text(self, lines: List[str]) -> List[str]:
        """Reconstruct fragmented text by merging broken lines."""
        if not lines:
            return []
        
        reconstructed = []
        current_paragraph = ""
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                if current_paragraph:
                    reconstructed.append(current_paragraph)
                    current_paragraph = ""
                continue
            
            # Check if this line should start a new paragraph
            should_start_new = (
                # Line starts with common section headers
                any(line.lower().startswith(header) for header in [
                    'work', 'education', 'skills', 'profile', 'experience', 'projects'
                ]) or
                # Line looks like a job title (contains common job words)
                any(job_word in line.lower() for job_word in [
                    'engineer', 'developer', 'manager', 'analyst', 'specialist', 'consultant', 'intern', 'tutor'
                ]) or
                # Line contains date patterns
                re.search(r'\d{4}', line) or
                # Line is very short and looks like a header
                (len(line) < 50 and line.isupper()) or
                # Line starts with bullet points
                line.startswith('•') or line.startswith('-') or line.startswith('*') or
                # Line contains company-like patterns (multiple words, no special chars)
                (len(line.split()) >= 2 and not re.search(r'[^\w\s\-\.]', line) and len(line) > 10)
            )
            
            if should_start_new and current_paragraph:
                reconstructed.append(current_paragraph)
                current_paragraph = line
            else:
                # Continue building current paragraph
                if current_paragraph:
                    # Check if we're continuing a job title or company name
                    if (len(current_paragraph.split()) <= 3 and 
                        any(job_word in current_paragraph.lower() for job_word in ['engineer', 'developer', 'manager', 'analyst', 'specialist', 'consultant', 'intern', 'tutor'])):
                        # This looks like a job title, add space and continue
                        current_paragraph += " " + line
                    elif (len(current_paragraph.split()) <= 4 and 
                          not re.search(r'[^\w\s\-\.]', current_paragraph) and
                          len(current_paragraph) < 50):
                        # This looks like a company name, add space and continue
                        current_paragraph += " " + line
                    else:
                        # Regular paragraph continuation
                        current_paragraph += " " + line
                else:
                    current_paragraph = line
        
        # Add the last paragraph
        if current_paragraph:
            reconstructed.append(current_paragraph)
        
        # Clean up reconstructed paragraphs
        cleaned_paragraphs = []
        for para in reconstructed:
            # Remove excessive whitespace
            cleaned = re.sub(r'\s+', ' ', para.strip())
            if cleaned and len(cleaned) > 3:
                cleaned_paragraphs.append(cleaned)
        
        return cleaned_paragraphs
    
    def _identify_sections(self, paragraphs: List[str]) -> List[Section]:
        """Identify resume sections using LLM with deterministic output."""
        resume_text = "\n".join(paragraphs)
        
        system_prompt = """You are a deterministic resume parser that outputs ONLY valid JSON.
Your task is to identify major sections in resumes.

CRITICAL RULES:
1. Output ONLY the requested JSON structure - no explanations, no markdown
2. Identify sections ONLY from explicit section headers in the text
3. Never infer or create sections that don't exist
4. Use exact section header text from the resume
5. Do not standardize or modify section names
6. If a section exists, use its exact text
7. Always return valid JSON even if extraction is partial"""
        
        user_prompt = f"""Identify all major sections in this resume.

Resume Text:
{resume_text}

Return ONLY a JSON object with this exact structure:
{{
  "sections": [
    {{
      "id": "section_1",
      "name": "exact section header from text",
      "start_index": paragraph_index_where_section_starts
    }}
  ]
}}

REQUIREMENTS:
1. Use exact section headers from text
2. Preserve original capitalization
3. Include paragraph index where section starts
4. Do not create missing sections
5. Do not include explanatory text
6. Return only the JSON object"""
        
        try:
            # Use the unified LLM client
            if hasattr(self.skills_agent.client, 'create_message'):
                # New unified client interface
                response = self.skills_agent.client.create_message(
                    provider=None,  # Use default provider
                    quality='fast',
                    messages=[{"role": "user", "content": user_prompt}],
                    system=system_prompt,
                    max_tokens=1000,
                    temperature=0.0
                )
                response_text = response['content'].strip()
            else:
                # Legacy Anthropic client interface
                response = self.skills_agent.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=1000,
                    temperature=0.0,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}]
                )
                response_text = response.content[0].text.strip()
            
            # Find JSON content
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in LLM response")
            
            json_str = response_text[json_start:json_end]
            
            # Parse JSON string to dict
            try:
                sections_data = json.loads(json_str)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON from LLM: {e}")
            
            # Convert to Section objects
            sections = []
            for section in sections_data.get("sections", []):
                sections.append(Section(
                    id=section.get("id", "section_1"),
                    name=section.get("name", "").strip()
                ))
            
            # Ensure we have at least one section
            if not sections:
                sections = [Section(id="section_1", name="MAIN")]
            
            return sections
            
        except Exception as e:
            logger.error(f"LLM section identification failed: {e}")
            # Fallback to minimal structure
            return [Section(id="section_1", name="MAIN")]
    
    def _extract_roles(self, paragraphs: List[str], sections: List[Section]) -> List[Role]:
        """Extract job roles using LLM intelligence."""
        roles = []
        
        # Find experience section
        experience_section = next((s for s in sections if 'experience' in s.name.lower()), None)
        if not experience_section:
            return roles
        
        # Get text from experience section
        experience_text = "\n".join(paragraphs)
        
        try:
            logger.info("Using LLM to extract job roles from resume")
            roles_data = self._extract_roles_with_llm(experience_text)
            
            # Convert to Role objects
            for i, role_data in enumerate(roles_data, 1):
                role = Role(
                    id=f"role_{i}",
                    section_id=experience_section.id,
                    title=role_data.get('title', 'Unknown Title'),
                    company=role_data.get('company', 'Unknown Company'),
                    date_range=role_data.get('dates', 'Unknown Dates')
                )
                roles.append(role)
            
            logger.info(f"Successfully extracted {len(roles)} roles using LLM")
            return roles
            
        except Exception as e:
            logger.error(f"LLM role extraction failed: {e}")
            return []
    
    def _extract_roles_with_llm(self, experience_text: str) -> List[Dict]:
        """Use LLM to extract roles from experience text with deterministic output."""
        system_prompt = """You are a deterministic resume parser that outputs ONLY valid JSON.
Your task is to extract job roles/positions from resumes.

CRITICAL RULES:
1. Output ONLY the requested JSON structure - no explanations, no markdown
2. Use ONLY information explicitly present in the text
3. Never add or infer missing information
4. Format dates exactly as they appear in the text
5. Preserve exact company names and job titles
6. If information is missing, use empty string ""
7. Always return valid JSON even if extraction is partial"""
        
        user_prompt = f"""Extract all job roles from this resume text.

Resume Text:
{experience_text}

Return ONLY a JSON array with this exact structure:
{{
  "roles": [
    {{
      "title": "exact job title from text",
      "company": "exact company name from text",
      "dates": "exact date range from text"
    }}
  ]
}}

REQUIREMENTS:
1. Use exact text matches only
2. Preserve original capitalization
3. Do not modify or standardize dates
4. Do not add missing information
5. Do not include explanatory text
6. Return only the JSON object"""
        
        try:
            # Use the unified LLM client
            if hasattr(self.skills_agent.client, 'create_message'):
                # New unified client interface
                response = self.skills_agent.client.create_message(
                    provider=None,  # Use default provider
                    quality='fast',
                    messages=[{"role": "user", "content": user_prompt}],
                    system=system_prompt,
                    max_tokens=1000,
                    temperature=0.1
                )
                response_text = response['content'].strip()
            else:
                # Legacy Anthropic client interface
                response = self.skills_agent.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=1000,
                    temperature=0.1,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": user_prompt}
                    ]
                )
                response_text = response.content[0].text.strip()
            
            # Find JSON content
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in LLM response")
            
            json_str = response_text[json_start:json_end]
            
            # Parse JSON string to list
            try:
                roles_data = json.loads(json_str)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON from LLM: {e}")
            
            return roles_data if isinstance(roles_data, list) else []
            
        except Exception as e:
            logger.error(f"LLM role extraction failed: {e}")
            raise
    
    def _extract_bullets(self, paragraphs: List[str], roles: List[Role]) -> List[Bullet]:
        """Extract bullet points using LLM intelligence."""
        bullets = []
        
        if not roles:
            return bullets
        
        # Get full resume text
        resume_text = "\n".join(paragraphs)
        
        try:
            logger.info("Using LLM to extract bullet points from resume")
            bullets_data = self._extract_bullets_with_llm(resume_text, roles)
            
            # Convert to Bullet objects and remove duplicates
            bullet_id_counter = 1
            seen_bullets = set()
            
            for bullet_data in bullets_data:
                bullet_text = bullet_data.get('text', '').strip()
                if not bullet_text:
                    continue
                
                # Create a normalized version for duplicate detection
                normalized_text = re.sub(r'\s+', ' ', bullet_text.lower()).strip()
                
                # Skip if we've seen this bullet before
                if normalized_text in seen_bullets:
                    logger.info(f"Skipping duplicate bullet: {bullet_text[:50]}...")
                    continue
                
                seen_bullets.add(normalized_text)
                
                bullet = Bullet(
                    id=f"bullet_{bullet_id_counter}",
                    role_id=bullet_data.get('role_id', roles[0].id),
                    text=bullet_text
                )
                bullets.append(bullet)
                bullet_id_counter += 1
            
            logger.info(f"Successfully extracted {len(bullets)} bullets using LLM")
            return bullets
            
        except Exception as e:
            logger.error(f"LLM bullet extraction failed: {e}")
            return []
    
    def _extract_bullets_with_llm(self, resume_text: str, roles: List[Role]) -> List[Dict]:
        """Use LLM to extract bullet points with deterministic output."""
        # Create role context for the LLM
        role_context = []
        for role in roles:
            role_context.append(f"Role ID: {role.id} - {role.title} at {role.company} ({role.date_range})")
        
        system_prompt = """You are a deterministic resume parser that outputs ONLY valid JSON.
Your task is to extract bullet points and achievements from resumes.

CRITICAL RULES:
1. Output ONLY the requested JSON structure - no explanations, no markdown
2. Extract ONLY bullet points that exist in the text
3. Never modify or rephrase bullet points
4. Preserve exact text, formatting, and punctuation
5. Do not add or enhance bullet points
6. If a bullet point exists, copy it exactly as is
7. Always return valid JSON even if extraction is partial"""
        
        user_prompt = f"""Extract bullet points from this resume text.

Resume Text:
{resume_text}

Available Roles:
{chr(10).join(role_context)}

Return ONLY a JSON object with this exact structure:
{{
  "bullets": [
    {{
      "role_id": "exact role_id from list above",
      "text": "exact bullet point text from resume"
    }}
  ]
}}

REQUIREMENTS:
1. Copy bullet points exactly as they appear
2. Preserve original formatting and symbols
3. Do not modify or enhance text
4. Do not add missing information
5. Do not include explanatory text
6. Return only the JSON object"""
        
        try:
            # Use the unified LLM client
            if hasattr(self.skills_agent.client, 'create_message'):
                # New unified client interface
                response = self.skills_agent.client.create_message(
                    provider=None,  # Use default provider
                    quality='fast',
                    messages=[{"role": "user", "content": user_prompt}],
                    system=system_prompt,
                    max_tokens=2000,
                    temperature=0.1
                )
                response_text = response['content'].strip()
            else:
                # Legacy Anthropic client interface
                response = self.skills_agent.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=2000,
                    temperature=0.1,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": user_prompt}
                    ]
                )
                response_text = response.content[0].text.strip()
            
            # Find JSON content
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in LLM response")
            
            json_str = response_text[json_start:json_end]
            
            # Parse JSON string to list
            try:
                bullets_data = json.loads(json_str)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON from LLM: {e}")
            
            return bullets_data if isinstance(bullets_data, list) else []
            
        except Exception as e:
            logger.error(f"LLM bullet extraction failed: {e}")
            raise
    
    def _extract_skills(self, paragraphs: List[str]) -> Dict[str, List[str]]:
        """Extract skills using comprehensive LLM analysis."""
        # Get full resume text for comprehensive skills extraction
        full_resume_text = "\n".join(paragraphs)
        
        try:
            logger.info("Using LLM to extract skills comprehensively from entire resume")
            skills_data = self._extract_skills_with_llm(full_resume_text)
            
            if skills_data:
                logger.info(f"Successfully extracted skills: {skills_data}")
                return skills_data
            else:
                logger.warning("LLM returned no skills, using fallback")
                return self._extract_skills_fallback(paragraphs)
                
        except Exception as e:
            logger.warning(f"LLM skills extraction failed: {e}, using fallback")
            return self._extract_skills_fallback(paragraphs)
    
    def _extract_skills_with_llm(self, resume_text: str) -> Dict[str, List[str]]:
        """Use LLM to comprehensively extract and categorize skills from resume."""
        system_prompt = """You are an expert resume parser specializing in skills extraction.
        
        Extract ALL skills, competencies, and abilities mentioned throughout the entire resume.
        Look in job descriptions, achievements, education, and any other sections.
        
        CRITICAL:
        - Extract ONLY skills that are EXPLICITLY mentioned in the text
        - Include technical skills, soft skills, industry-specific skills
        - Look in job bullets, achievements, and descriptions for implied skills
        - Do NOT hallucinate skills that aren't mentioned"""
        
        user_prompt = f"""Extract ALL skills from this resume text. Look everywhere - job descriptions, achievements, education, etc.

Resume Text:
{resume_text}

Extract and return ONLY a JSON object with skills categorized logically:
{{
    "category_name": ["skill1", "skill2", "skill3"],
    "another_category": ["skill4", "skill5"]
}}

Guidelines:
- Extract COMPREHENSIVE skills from the ENTIRE resume (not just skills section)
- Include technical skills, soft skills, industry-specific abilities
- Look in job bullet points for technologies, tools, processes used
- Extract skills from achievements (e.g., "managed teams" → "Team Management")
- Include certifications, software, methodologies mentioned
- Categorize appropriately for the industry/role type
- ONLY include skills EXPLICITLY mentioned or clearly demonstrated
- Return appropriate categories for the role (e.g., Customer Service, Technical, etc.)
- Return ONLY valid JSON, no explanations"""
        
        try:
            # Use the unified LLM client
            if hasattr(self.skills_agent.client, 'create_message'):
                # New unified client interface
                response = self.skills_agent.client.create_message(
                    provider=None,  # Use default provider
                    quality='fast',
                    messages=[{"role": "user", "content": user_prompt}],
                    system=system_prompt,
                    max_tokens=1500,
                    temperature=0.1
                )
                response_text = response['content'].strip()
            else:
                # Legacy Anthropic client interface
                response = self.skills_agent.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=1500,
                    temperature=0.1,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": user_prompt}
                    ]
                )
                response_text = response.content[0].text.strip()
            
            # Find JSON content
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in LLM response")
            
            json_str = response_text[json_start:json_end]
            
            # Parse JSON string to dictionary
            try:
                skills_data = json.loads(json_str)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON from LLM: {e}")
            
            return skills_data if isinstance(skills_data, dict) else {}
            
        except Exception as e:
            logger.error(f"LLM skills extraction failed: {e}")
            raise
    
    def _extract_skills_fallback(self, paragraphs: List[str]) -> Dict[str, List[str]]:
        """Fallback skills extraction using traditional text parsing."""
        skills_text = ""
        in_skills_section = False
        
        for para in paragraphs:
            para_lower = para.lower()
            
            # Check if we're entering a skills section
            if any(skill_word in para_lower for skill_word in ['skills', 'technologies', 'tools', 'languages']):
                in_skills_section = True
                skills_text += para + "\n"
                continue
            
            # If we're in skills section, collect text
            if in_skills_section:
                # Check if we've hit another major section
                if any(section_word in para_lower for section_word in ['experience', 'education', 'projects', 'certifications']):
                    in_skills_section = False
                    break
                else:
                    skills_text += para + "\n"
        
        if skills_text.strip():
            # Use Skills Categorization Agent for intelligent categorization
            return self.skills_agent.categorize_skills(skills_text.strip())
        
        return {}
