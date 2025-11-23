from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    name: str
    target_role: str | None = None
    cv_style: str | None = None
    preferences: dict | None = None


class ProjectResponse(BaseModel):
    id: int
    user_id: int
    name: str
    target_role: str | None
    cv_style: str | None
    preferences: dict | None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ProjectUpdate(BaseModel):
    name: str | None = None
    target_role: str | None = None
    cv_style: str | None = None
    preferences: dict | None = None

