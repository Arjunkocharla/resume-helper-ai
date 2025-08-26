from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from .registry import SCHEMA_VERSION


class Section(BaseModel):
    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)


class Role(BaseModel):
    id: str = Field(..., min_length=1)
    section_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    company: str = Field(..., min_length=1)
    date_range: Optional[str] = None


class Bullet(BaseModel):
    id: str = Field(..., min_length=1)
    role_id: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1)

    @field_validator("text")
    @classmethod
    def text_not_blank(cls, v: str) -> str:
        v_stripped = v.strip()
        if not v_stripped:
            raise ValueError("bullet text cannot be blank")
        return v_stripped


class ResumeAST(BaseModel):
    schema_version: Literal["v1"] = SCHEMA_VERSION  # pin per artifact
    sections: List[Section]
    roles: List[Role]
    bullets: List[Bullet]
    skills_buckets: Dict[str, List[str]] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_referential_integrity(self) -> "ResumeAST":
        section_ids = {s.id for s in self.sections}
        if len(section_ids) != len(self.sections):
            raise ValueError("duplicate section ids")

        role_ids = {r.id for r in self.roles}
        if len(role_ids) != len(self.roles):
            raise ValueError("duplicate role ids")

        for r in self.roles:
            if r.section_id not in section_ids:
                raise ValueError(f"role.section_id not found: {r.section_id}")

        bullet_ids = {b.id for b in self.bullets}
        if len(bullet_ids) != len(self.bullets):
            raise ValueError("duplicate bullet ids")

        for b in self.bullets:
            if b.role_id not in role_ids:
                raise ValueError(f"bullet.role_id not found: {b.role_id}")

        # normalize skills buckets: strip, drop empties, dedupe
        normalized: Dict[str, List[str]] = {}
        for bucket_name, values in self.skills_buckets.items():
            bucket_name_clean = bucket_name.strip()
            if not bucket_name_clean:
                continue
            seen: set[str] = set()
            cleaned_values: List[str] = []
            for val in values:
                v = val.strip()
                if not v or v.lower() in seen:
                    continue
                seen.add(v.lower())
                cleaned_values.append(v)
            if cleaned_values:
                normalized[bucket_name_clean] = cleaned_values
        self.skills_buckets = normalized
        return self


