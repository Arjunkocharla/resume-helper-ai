from typing import List, Literal

from pydantic import BaseModel, Field, field_validator

from .registry import SCHEMA_VERSION


SeniorityLevel = Literal[
    "intern",
    "junior",
    "mid",
    "senior",
    "staff",
    "principal",
    "lead",
    "manager",
]


class JDSummary(BaseModel):
    schema_version: Literal["v1"] = SCHEMA_VERSION
    must_have: List[str] = Field(default_factory=list)
    nice_to_have: List[str] = Field(default_factory=list)
    responsibilities: List[str] = Field(default_factory=list)
    seniority: SeniorityLevel | None = None

    @field_validator("must_have", "nice_to_have", "responsibilities")
    @classmethod
    def normalize_list(cls, values: List[str]) -> List[str]:
        seen: set[str] = set()
        out: List[str] = []
        for v in values:
            s = v.strip()
            if not s:
                continue
            key = s.lower()
            if key in seen:
                continue
            seen.add(key)
            out.append(s)
        return out


