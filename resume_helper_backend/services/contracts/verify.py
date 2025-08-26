from typing import List, Literal

from pydantic import BaseModel, Field

from .registry import SCHEMA_VERSION


class VerifyReport(BaseModel):
    schema_version: Literal["v1"] = SCHEMA_VERSION
    applied: bool
    missing_targets: List[str] = Field(default_factory=list)
    duplicates: List[str] = Field(default_factory=list)
    limits_violations: List[str] = Field(default_factory=list)
    ats_score: float | None = None
    word_count: int | None = None
    suggestions: List[str] = Field(default_factory=list)


