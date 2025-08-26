from typing import List, Literal

from pydantic import BaseModel, Field

from .registry import SCHEMA_VERSION


class ModifiedBullet(BaseModel):
    before: str
    after: str


class Diff(BaseModel):
    schema_version: Literal["v1"] = SCHEMA_VERSION
    added_bullets: List[str] = Field(default_factory=list)
    modified_bullets: List[ModifiedBullet] = Field(default_factory=list)
    added_skills: List[str] = Field(default_factory=list)
    removed_skills: List[str] = Field(default_factory=list)


