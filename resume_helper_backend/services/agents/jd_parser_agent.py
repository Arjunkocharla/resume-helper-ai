import json
import logging
import re
from typing import List, Optional

import anthropic
from pydantic import ValidationError

from ..contracts import JDSummary, SeniorityLevel, validate_or_raise

logger = logging.getLogger(__name__)


class JDParserAgent:
    """Agent responsible for parsing and structuring job descriptions."""
    
    def __init__(self, client: anthropic.Anthropic):
        self.client = client
        
    def parse_jd(self, raw_jd_text: str) -> JDSummary:
        """
        Parse raw job description text into structured JDSummary.
        
        Args:
            raw_jd_text: Raw, potentially messy job description text
            
        Returns:
            JDSummary: Structured job description data
            
        Raises:
            ValidationError: If LLM response cannot be parsed into JDSummary
        """
        try:
            # Clean the input text
            cleaned_text = self._clean_jd_text(raw_jd_text)
            
            # Extract structured data using LLM
            jd_summary = self._extract_jd_summary(cleaned_text)
            
            logger.info(f"Successfully parsed JD into {len(jd_summary.must_have)} must-have skills")
            return jd_summary
            
        except Exception as e:
            logger.error(f"Failed to parse JD: {e}")
            raise
    
    def _clean_jd_text(self, raw_text: str) -> str:
        """Clean and normalize raw job description text."""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', raw_text)
        
        # Remove extra whitespace and normalize line breaks
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n', text)
        
        # Remove common boilerplate
        boilerplate_patterns = [
            r'Apply now',
            r'Submit your application',
            r'Equal opportunity employer',
            r'We are an equal opportunity employer',
            r'Benefits include',
            r'Compensation',
            r'Salary range',
        ]
        
        for pattern in boilerplate_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def _extract_jd_summary(self, cleaned_text: str) -> JDSummary:
        """Use LLM to extract structured JD data."""
        system_prompt = """You are an expert HR analyst. Parse job descriptions and extract key information in structured JSON format."""
        
        user_prompt = f"""Parse this job description and extract key information.

Job Description:
{cleaned_text}

Extract and return ONLY a JSON object with this exact structure:
{{
    "must_have": ["skill1", "skill2", "skill3"],
    "nice_to_have": ["skill1", "skill2"],
    "responsibilities": ["responsibility1", "responsibility2"],
    "seniority": "intern" | "junior" | "mid" | "senior" | "staff" | "principal" | "lead" | "manager" | null
}}

Guidelines:
- must_have: Essential skills/requirements (max 8)
- nice_to_have: Desired but not required skills (max 6)
- responsibilities: Key job duties (max 5)
- seniority: Infer from experience requirements and role level
- Use specific skill names, not generic terms
- Return ONLY valid JSON, no explanations"""

        try:
            # Use the unified LLM client
            if hasattr(self.client, 'create_message'):
                # New unified client interface
                response = self.client.create_message(
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
                response = self.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=1000,
                    temperature=0.1,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": user_prompt}
                    ]
                )
                response_text = response.content[0].text.strip()
            
            # Find JSON content (handle potential markdown formatting)
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in LLM response")
            
            json_str = response_text[json_start:json_end]
            
            # Parse JSON string to dictionary first
            try:
                json_dict = json.loads(json_str)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON from LLM: {e}")
            
            # Parse and validate into JDSummary
            jd_summary = validate_or_raise(JDSummary, json_dict)
            return jd_summary
            
        except Exception as e:
            logger.error(f"LLM extraction failed: {e}")
            # Fallback to basic parsing
            return self._fallback_parse(cleaned_text)
    
    def _fallback_parse(self, text: str) -> JDSummary:
        """Fallback parsing when LLM fails."""
        logger.warning("Using fallback JD parsing")
        
        # Extract skills using regex patterns
        skill_patterns = [
            r'\b(?:Python|Java|JavaScript|React|Node\.js|AWS|Docker|Kubernetes|SQL|MongoDB|PostgreSQL|Git|Linux|Agile|Scrum)\b',
            r'\b(?:Machine Learning|AI|Data Science|DevOps|Full Stack|Frontend|Backend|Mobile|Cloud|Microservices)\b',
        ]
        
        skills = []
        for pattern in skill_patterns:
            skills.extend(re.findall(pattern, text, re.IGNORECASE))
        
        # Deduplicate and normalize
        skills = list(set([skill.lower() for skill in skills]))
        
        # Infer seniority from text
        seniority = self._infer_seniority(text)
        
        return JDSummary(
            must_have=skills[:5],  # Top 5 as must-have
            nice_to_have=skills[5:8],  # Next 3 as nice-to-have
            responsibilities=["Lead development projects", "Collaborate with cross-functional teams"],
            seniority=seniority
        )
    
    def _infer_seniority(self, text: str) -> Optional[SeniorityLevel]:
        """Infer seniority level from job description text."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['intern', 'internship', 'entry level']):
            return 'intern'
        elif any(word in text_lower for word in ['junior', 'entry', '0-2 years', '1-3 years']):
            return 'junior'
        elif any(word in text_lower for word in ['mid', 'mid-level', '3-5 years', '4-6 years']):
            return 'mid'
        elif any(word in text_lower for word in ['senior', '5+ years', '6+ years', '7+ years']):
            return 'senior'
        elif any(word in text_lower for word in ['staff', 'principal', 'lead', 'manager', 'director']):
            return 'staff'
        else:
            return None
