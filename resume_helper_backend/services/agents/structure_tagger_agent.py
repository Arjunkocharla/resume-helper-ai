#!/usr/bin/env python3
"""StructureTaggerAgent - LLM-assisted paragraph-level structure tagging.

Classifies DOCX paragraphs by index without rewriting content. Output references paragraph
indices only so the editor can make deterministic edits aligned with actual DOCX structure.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Literal, Optional, TypedDict

import anthropic

logger = logging.getLogger(__name__)


class ParagraphTag(TypedDict, total=False):
    paragraph_index: int
    label: Literal[
        "header_profile",
        "section_header",
        "role_header",
        "company_line",
        "date_line",
        "bullet",
        "skills_header",
        "education_header",
        "other",
    ]
    role_span_id: Optional[str]


class RoleSpan(TypedDict):
    span_id: str
    start_index: int
    end_index: int


class StructureTags(TypedDict, total=False):
    paragraph_tags: List[ParagraphTag]
    role_spans: List[RoleSpan]


class StructureTaggerAgent:
    """LLM-assisted agent that tags paragraph structure by index only."""

    def __init__(self, anthropic_client: anthropic.Anthropic):
        self.client = anthropic_client
        self.logger = logging.getLogger(__name__)

    def tag_paragraphs(self, paragraphs: List[Dict]) -> StructureTags:
        """Classify paragraph roles.
        
        paragraphs: list of dicts with keys: paragraph_index, text, style_name, has_numpr, outline_level
        Returns JSON-compatible dict with paragraph_tags and role_spans.
        """
        system = (
            "You are a JSON-native document classifier for resumes. You will receive an array of paragraphs with metadata.\n"
            "You MUST respond with ONLY a valid JSON object - no prose, no explanation, no code blocks.\n\n"
            "Your output must be a JSON object with these keys:\n"
            "- paragraph_tags: array of {paragraph_index: number, label: string, role_span_id?: string}\n"
            "- role_spans: array of {span_id: string, start_index: number, end_index: number}\n\n"
            "Valid labels are:\n"
            "- header_profile: Profile/summary section at top\n"
            "- section_header: Major sections like SKILLS, EXPERIENCE, INTERNSHIPS, EDUCATION\n"
            "- role_header: Job titles like 'Software Engineer'\n"
            "- company_line: Company name and location\n"
            "- date_line: Employment dates\n"
            "- bullet: Achievement/responsibility bullet points\n"
            "- skills_header: Skills section header\n"
            "- education_header: Education section header\n"
            "- other: Any other content\n\n"
            "Rules:\n"
            "1. Major sections (SKILLS, EXPERIENCE, INTERNSHIPS) must be tagged as section_header\n"
            "2. Role spans must not cross major section boundaries\n"
            "3. Each role span should include:\n"
            "   - Role header (job title)\n"
            "   - Company line\n"
            "   - Date line\n"
            "   - All bullets until next role or section\n"
            "4. Never rewrite text, only classify\n"
            "5. Return ONLY valid JSON with proper commas between array items and object properties\n"
            "6. Use paragraph_index to reference content\n"
            "7. Spans must be non-overlapping and within bounds\n"
            "\nExample JSON format:\n"
            '{\n'
            '  "paragraph_tags": [\n'
            '    {"paragraph_index": 0, "label": "section_header"},\n'
            '    {"paragraph_index": 1, "label": "role_header", "role_span_id": "role1"}\n'
            '  ],\n'
            '  "role_spans": [\n'
            '    {"span_id": "role1", "start_index": 1, "end_index": 5}\n'
            '  ]\n'
            '}\n'
            "\nOutput must be ONLY valid JSON with no additional text, no code blocks, no explanation."
        )
        
        # Compact the paragraphs for LLM
        example = {
            "paragraphs": [
                {
                    "paragraph_index": p.get("paragraph_index"),
                    "text": (p.get("text") or "").strip()[:200],  # Shorter text to avoid token limits
                    "style_name": p.get("style_name") or "",
                    "has_numpr": bool(p.get("has_numpr")),
                    "outline_level": p.get("outline_level"),
                }
                for p in paragraphs
            ]
        }
        
        user = (
            "Analyze this resume and output a JSON object that classifies each paragraph.\n\n"
            "Example output format:\n"
            "{\n"
            '  "paragraph_tags": [\n'
            '    {"paragraph_index": 0, "label": "section_header"},\n'
            '    {"paragraph_index": 1, "label": "role_header", "role_span_id": "role1"},\n'
            '    {"paragraph_index": 2, "label": "company_line"},\n'
            '    {"paragraph_index": 3, "label": "bullet"}\n'
            "  ],\n"
            '  "role_spans": [\n'
            '    {"span_id": "role1", "start_index": 1, "end_index": 5}\n'
            "  ]\n"
            "}\n\n"
            f"Input document:\n{example}"
        )
        
        try:
            # Use the unified LLM client
            if hasattr(self.client, 'create_message'):
                # New unified client interface
                resp = self.client.create_message(
                    provider=None,  # Use default provider
                    quality='fast',
                    messages=[{"role": "user", "content": user}],
                    system=system,
                    max_tokens=1000,
                    temperature=0.0
                )
                # Get raw response text
                text = resp['content'].strip()
            else:
                # Legacy Anthropic client interface
                resp = self.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=1000,  # Reduced to avoid complex responses
                    temperature=0.0,
                    system=system,
                    messages=[{"role": "user", "content": user}],
                )
                # Get raw response text
                text = resp.content[0].text.strip()
            
            # Remove any non-JSON content
            json_start = text.find("{")
            json_end = text.rfind("}") + 1
            if json_start == -1 or json_end <= json_start:
                self.logger.error("No JSON object found in response")
                return {"paragraph_tags": [], "role_spans": []}
            
            # Parse the JSON
            import json as _json
            try:
                data = _json.loads(text[json_start:json_end])
            except Exception as e:
                self.logger.error(f"JSON parsing failed: {e}")
                return {"paragraph_tags": [], "role_spans": []}
            
            # Basic validation
            if not isinstance(data, dict):
                raise ValueError("Tagger output is not a dict")
            
            data.setdefault("paragraph_tags", [])
            data.setdefault("role_spans", [])
            
            # Filter invalid entries
            tags: List[ParagraphTag] = []
            for t in data.get("paragraph_tags", []):
                if (
                    isinstance(t, dict)
                    and isinstance(t.get("paragraph_index"), int)
                    and isinstance(t.get("label"), str)
                ):
                    tags.append(t)  # type: ignore
            
            spans: List[RoleSpan] = []
            for s in data.get("role_spans", []):
                if (
                    isinstance(s, dict)
                    and isinstance(s.get("start_index"), int)
                    and isinstance(s.get("end_index"), int)
                    and isinstance(s.get("span_id"), str)
                ):
                    spans.append(s)  # type: ignore
            
            return {"paragraph_tags": tags, "role_spans": spans}
            
        except Exception as e:
            self.logger.error(f"Structure tagging failed: {e}")
            # Fail safe: return empty tags
            return {"paragraph_tags": [], "role_spans": []}
