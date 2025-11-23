from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.database.models import SkillType


class UserSkillsCreate(BaseModel):
    skill_text: str
    skill_type: SkillType
    raw_input: str | None = None
    source: str | None = None


class UserSkillsResponse(BaseModel):
    id: int
    user_id: int
    skill_text: str
    skill_type: SkillType
    raw_input: str | None
    source: str | None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserSkillsUpdate(BaseModel):
    skill_text: str | None = None
    skill_type: SkillType | None = None
    raw_input: str | None = None
    source: str | None = None


class UserSkillsGroupedResponse(BaseModel):
    """Response con skills agrupados por tipo"""
    experience: list[UserSkillsResponse] = []
    dev_skills: list[UserSkillsResponse] = []
    certificates: list[UserSkillsResponse] = []
    extra: list[UserSkillsResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

