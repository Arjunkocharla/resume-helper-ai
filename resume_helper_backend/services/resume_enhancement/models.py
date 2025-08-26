from pydantic import BaseModel, Field, RootModel
from typing import List, Dict, Optional

class ResumeSection(BaseModel):
    """Model for a resume section"""
    name: str = Field(description="Section name (e.g., EXPERIENCE, SKILLS)")
    content: List[str] = Field(description="Content within the section")
    type: str = Field(description="Section type")

class EnhancementSuggestion(BaseModel):
    """Model for a single enhancement suggestion"""
    role: Optional[str] = None
    suggestion: str

class SectionSuggestions(RootModel):
    """Model for suggestions in a section"""
    root: List[EnhancementSuggestion]

class EnhancementResponse(BaseModel):
    """Model for the complete enhancement response"""
    sections: Dict[str, List[EnhancementSuggestion]]
