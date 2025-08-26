import json
import logging
from typing import Dict, List

import anthropic
from pydantic import ValidationError
import re

logger = logging.getLogger(__name__)


class SkillsCategorizationAgent:
    """Agent responsible for intelligently categorizing skills using LLM."""
    
    def __init__(self, client: anthropic.Anthropic):
        self.client = client
    
    def categorize_skills(self, raw_skills_text: str) -> Dict[str, List[str]]:
        """
        Categorize raw skills text into logical groups using LLM.
        
        Args:
            raw_skills_text: Raw text containing skills from resume
            
        Returns:
            Dict[str, List[str]]: Categorized skills by category
            
        Raises:
            ValueError: If LLM response cannot be parsed
        """
        try:
            logger.info("Categorizing skills using LLM")
            
            # Use LLM to intelligently categorize skills
            categorized_skills = self._extract_categories_with_llm(raw_skills_text)
            
            logger.info(f"Successfully categorized skills into {len(categorized_skills)} categories")
            return categorized_skills
            
        except Exception as e:
            logger.error(f"Failed to categorize skills: {e}")
            # Fallback to basic categorization
            return self._fallback_categorization(raw_skills_text)
    
    def _extract_categories_with_llm(self, raw_skills_text: str) -> Dict[str, List[str]]:
        """Use LLM to intelligently categorize skills."""
        system_prompt = """You are an expert HR analyst specializing in skills categorization. 
        Analyze the provided skills and organize them into logical, industry-appropriate categories.
        
        CRITICAL: Only categorize skills that are EXPLICITLY mentioned in the provided text.
        Do NOT add skills that are not present in the text.
        Do NOT infer technical skills for non-technical roles."""
        
        user_prompt = f"""Categorize these skills into logical groups. Consider the context and industry.

Skills Text:
{raw_skills_text}

Instructions:
- Create meaningful categories based on the skills provided
- Use industry-standard category names when possible
- Group related skills together
- Don't create categories for single skills unless necessary
- Focus on logical organization that would make sense to recruiters
- **ONLY include skills that are EXPLICITLY mentioned in the text above**
- **Do NOT add technical skills that don't appear in the text**
- **Do NOT infer programming languages or technical tools unless they're explicitly listed**

Return ONLY a JSON object with this structure:
{{
    "category_name": ["skill1", "skill2", "skill3"],
    "another_category": ["skill4", "skill5"]
}}

Examples of good categories:
- "Customer Service": ["Customer Service", "Guest Relations", "Problem Resolution"]
- "Food & Beverage": ["Wine Knowledge", "Food Safety", "Menu Knowledge"]
- "Teamwork": ["Collaboration", "Kitchen Coordination", "Front-of-House Teamwork"]
- "Technical Skills": ["POS Systems", "Inventory Management", "Cash Handling"]

Return ONLY valid JSON, no explanations."""
        
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
            
            # Find JSON content
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in LLM response")
            
            json_str = response_text[json_start:json_end]
            
            # Parse JSON string to dictionary
            try:
                categorized_skills = json.loads(json_str)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON from LLM: {e}")
            
            # Validate the structure
            if not isinstance(categorized_skills, dict):
                raise ValueError("LLM response is not a dictionary")
            
            # Clean and normalize the data
            cleaned_skills = {}
            for category, skills in categorized_skills.items():
                if isinstance(skills, list) and skills:
                    # Clean skill names and remove duplicates
                    cleaned_skill_list = []
                    seen_skills = set()
                    for skill in skills:
                        if isinstance(skill, str) and skill.strip():
                            clean_skill = skill.strip()
                            if clean_skill.lower() not in seen_skills:
                                seen_skills.add(clean_skill.lower())
                                cleaned_skill_list.append(clean_skill)
                    
                    if cleaned_skill_list:
                        cleaned_skills[category.strip()] = cleaned_skill_list
            
            return cleaned_skills
            
        except Exception as e:
            logger.error(f"LLM categorization failed: {e}")
            raise
    
    def _fallback_categorization(self, raw_skills_text: str) -> Dict[str, List[str]]:
        """Fallback categorization when LLM fails."""
        logger.warning("Using fallback skills categorization")
        
        # Basic fallback: put everything in a "Skills" category
        skills_list = []
        
        # Extract individual skills (simple approach)
        lines = raw_skills_text.split('\n')
        for line in lines:
            line = line.strip()
            if line:
                # Split by common separators
                for skill in re.split(r'[,;|]', line):
                    skill = skill.strip()
                    if skill and len(skill) > 1:  # Avoid single characters
                        # Filter out obvious non-skills
                        if not any(word in skill.lower() for word in ['phone', 'email', 'address', 'linkedin', 'github']):
                            skills_list.append(skill)
        
        # Remove duplicates while preserving order
        unique_skills = []
        seen = set()
        for skill in skills_list:
            if skill.lower() not in seen:
                seen.add(skill.lower())
                unique_skills.append(skill)
        
        return {"Skills": unique_skills}
