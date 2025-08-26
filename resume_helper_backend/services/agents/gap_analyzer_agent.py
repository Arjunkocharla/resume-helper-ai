#!/usr/bin/env python3
"""Gap Analyzer Agent - Compares JD requirements vs resume experience and generates improvement plans."""

import json
import logging
from typing import Dict, List, Optional

import anthropic
from pydantic import ValidationError

from ..contracts import JDSummary, ResumeAST, Plan, validate_or_raise

logger = logging.getLogger(__name__)


class GapAnalyzerAgent:
    """Agent responsible for analyzing gaps between job requirements and resume content."""
    
    def __init__(self, client: anthropic.Anthropic):
        self.client = client
    
    def analyze_gaps(self, jd_summary: JDSummary, resume_ast: ResumeAST) -> Plan:
        """
        Analyze gaps between job requirements and resume content.
        
        Args:
            jd_summary: Parsed job description requirements
            resume_ast: Parsed resume structure and content
            
        Returns:
            Plan: Structured improvement recommendations with specific edits
            
        Raises:
            ValueError: If gap analysis cannot be completed
        """
        try:
            logger.info("Analyzing gaps between job requirements and resume")
            
            # Use LLM to perform intelligent gap analysis
            plan_data = self._analyze_gaps_with_llm(jd_summary, resume_ast)
            
            # Convert to Plan object
            plan = validate_or_raise(Plan, plan_data)
            
            logger.info(f"Successfully generated plan with {len(plan.edits)} recommendations")
            return plan
            
        except Exception as e:
            logger.error(f"Gap analysis failed: {e}")
            raise
    
    def _analyze_gaps_with_llm(self, jd_summary: JDSummary, resume_ast: ResumeAST) -> Dict:
        """Use LLM to perform intelligent gap analysis."""
        
        # Prepare context for the LLM
        jd_context = self._format_jd_context(jd_summary)
        resume_context = self._format_resume_context(resume_ast)
        
        system_prompt = """You are an expert career advisor and resume strategist. 
        
        Analyze the gap between job requirements and the candidate's resume, then generate comprehensive, actionable improvement recommendations.
        
        CRITICAL GUIDELINES:
        - Only suggest improvements based on EXISTING experience in the resume
        - DO NOT fabricate experiences that don't exist
        - Focus on highlighting, quantifying, and better positioning existing skills
        - Suggest specific bullet point improvements with concrete metrics
        - Prioritize high-impact changes that address key job requirements
        - BE AGGRESSIVE: Aim for 8-15 improvements to maximize keyword coverage
        - Cover multiple aspects: bullet improvements, new bullets, skills additions, formatting
        - Ensure every major job requirement has corresponding improvements"""
        
        user_prompt = f"""Analyze the gaps between this job description and resume, then generate specific improvement recommendations.

JOB REQUIREMENTS:
{jd_context}

CURRENT RESUME:
{resume_context}

Generate a comprehensive improvement plan with specific edits. Return ONLY a JSON object with this structure:

{{
  "edits": [
    {{
      "type": "modify_bullet",
      "bullet_id": "bullet_1", 
      "new_text": "• Enhanced bullet with specific metrics and relevant keywords",
      "reasoning": "Why this change addresses job requirements"
    }},
    {{
      "type": "insert_bullet",
      "role_id": "role_1",
      "after_bullet_id": "bullet_2",
      "text": "• New bullet highlighting relevant existing experience",
      "reasoning": "Why this addition strengthens the resume"
    }},
    {{
      "type": "upsert_skill", 
      "bucket": "Technical Skills",
      "value": "Relevant Technology",
      "reasoning": "Why this skill should be highlighted"
    }}
  ],
  "constraints": {{
    "max_bullets_per_role": 8,
    "forbid_fabrication": true,
    "preserve_style": true,
    "target_improvements": "8-15 total improvements"
  }}
}}

IMPORTANT: Generate 8-15 improvements to maximize keyword coverage and address all major job requirements.

ANALYSIS GUIDELINES:
1. **Skills Gap Analysis**: Compare required vs current skills, suggest highlighting existing relevant skills
2. **Experience Enhancement**: Improve existing bullets with better metrics, keywords, and positioning  
3. **Keyword Optimization**: Incorporate job-relevant terms from existing experience
4. **Quantification**: Add specific metrics to existing achievements where possible
5. **Prioritization**: Focus on changes that address the most critical job requirements
6. **Keyword Coverage**: Ensure that the resume covers atleast 60% of the keywords from the job description

EDIT TYPES:
- **modify_bullet**: Enhance existing bullets with better wording, metrics, keywords
- **insert_bullet**: Add new bullets that highlight existing but underemphasized experience
- **upsert_skill**: Add or emphasize relevant skills from existing experience (use "value" field for skill name)

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
                    max_tokens=3000,
                    temperature=0
                )
                response_text = response['content'].strip()
            else:
                # Legacy Anthropic client interface
                response = self.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=3000,
                    temperature=0,
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
                plan_data = json.loads(json_str)
            except json.JSONDecodeError as e:
                # Attempt code-only repair pass
                repaired = self._repair_json_string(json_str)
                try:
                    plan_data = json.loads(repaired)
                except Exception:
                    # One retry with stricter instruction asking for compact valid JSON only
                    retry_prompt = (
                        "Your previous response was not valid JSON. Return ONLY a valid, compact JSON object "
                        "that conforms to the required schema. Do not include code fences, comments, or prose."
                    )
                    
                    if hasattr(self.client, 'create_message'):
                        # New unified client interface
                        retry = self.client.create_message(
                            provider=None,  # Use default provider
                            quality='fast',
                            messages=[
                                {"role": "user", "content": user_prompt},
                                {"role": "assistant", "content": response_text},
                                {"role": "user", "content": retry_prompt}
                            ],
                            system=system_prompt,
                            max_tokens=1500,
                            temperature=0
                        )
                        retry_text = retry['content'].strip()
                    else:
                        # Legacy Anthropic client interface
                        retry = self.client.messages.create(
                            model="claude-3-haiku-20240307",
                            max_tokens=1500,
                            temperature=0,
                            system=system_prompt,
                            messages=[
                                {"role": "user", "content": user_prompt},
                                {"role": "assistant", "content": response_text},
                                {"role": "user", "content": retry_prompt}
                            ]
                        )
                        retry_text = retry.content[0].text.strip()
                    rs = retry_text[retry_text.find('{'):retry_text.rfind('}')+1]
                    rs = self._repair_json_string(rs)
                    try:
                        plan_data = json.loads(rs)
                    except Exception:
                        raise ValueError(f"Invalid JSON from LLM: {e}")
            
            return plan_data
            
        except Exception as e:
            logger.error(f"LLM gap analysis failed: {e}")
            raise

    def _repair_json_string(self, s: str) -> str:
        """Best-effort JSON repair: remove code fences, fix quotes, trailing commas, booleans/nulls."""
        import re
        # Strip code fences
        s = re.sub(r"^```(json)?", "", s.strip())
        s = re.sub(r"```$", "", s)
        # Normalize smart quotes to straight quotes
        s = s.replace('\u201c', '"').replace('\u201d', '"').replace('\u2019', "'")
        s = s.replace('“', '"').replace('”', '"').replace("’", "'")
        # Convert Python-style booleans/null if present
        s = re.sub(r"\bTrue\b", "true", s)
        s = re.sub(r"\bFalse\b", "false", s)
        s = re.sub(r"\bNone\b", "null", s)
        # Remove comments
        s = re.sub(r"//.*", "", s)
        s = re.sub(r"/\*.*?\*/", "", s, flags=re.DOTALL)
        # Remove trailing commas before ] or }
        s = re.sub(r",\s*([\]}])", r"\1", s)
        # Trim whitespace
        return s.strip()
    
    def _format_jd_context(self, jd_summary: JDSummary) -> str:
        """Format job description context for LLM analysis."""
        context = []
        
        if jd_summary.must_have:
            context.append(f"MUST-HAVE SKILLS: {', '.join(jd_summary.must_have)}")
        
        if jd_summary.nice_to_have:
            context.append(f"NICE-TO-HAVE SKILLS: {', '.join(jd_summary.nice_to_have)}")
        
        if jd_summary.responsibilities:
            context.append(f"KEY RESPONSIBILITIES: {'; '.join(jd_summary.responsibilities)}")
        
        if jd_summary.seniority:
            context.append(f"SENIORITY LEVEL: {jd_summary.seniority}")
        
        return "\n".join(context)
    
    def _format_resume_context(self, resume_ast: ResumeAST) -> str:
        """Format resume context for LLM analysis."""
        context = []
        
        # Add roles and their bullets
        context.append("WORK EXPERIENCE:")
        for role in resume_ast.roles:
            context.append(f"\n{role.title} at {role.company} ({role.date_range}) [ID: {role.id}]")
            
            # Add bullets for this role
            role_bullets = [b for b in resume_ast.bullets if b.role_id == role.id]
            for bullet in role_bullets:
                context.append(f"  {bullet.text} [ID: {bullet.id}]")
        
        # Add skills
        if resume_ast.skills_buckets:
            context.append("\nCURRENT SKILLS:")
            for category, skills in resume_ast.skills_buckets.items():
                context.append(f"  {category}: {', '.join(skills)}")
        
        return "\n".join(context)
