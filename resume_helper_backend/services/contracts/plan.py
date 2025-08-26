from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

from .registry import SCHEMA_VERSION


class PlanConstraints(BaseModel):
    max_bullets_per_role: int = 8
    forbid_fabrication: bool = True


class InsertBullet(BaseModel):
    type: Literal["insert_bullet"] = "insert_bullet"
    role_id: str
    after_bullet_id: Optional[str] = None
    text: str


class ModifyBullet(BaseModel):
    type: Literal["modify_bullet"] = "modify_bullet"
    bullet_id: str
    new_text: str


class UpsertSkill(BaseModel):
    type: Literal["upsert_skill"] = "upsert_skill"
    bucket: str
    value: str


# For now, use a simple union without discriminator
Edit = Union[InsertBullet, ModifyBullet, UpsertSkill]


class Plan(BaseModel):
    schema_version: Literal["v1"] = SCHEMA_VERSION
    edits: List[Edit] = Field(default_factory=list)
    constraints: PlanConstraints = Field(default_factory=PlanConstraints)


