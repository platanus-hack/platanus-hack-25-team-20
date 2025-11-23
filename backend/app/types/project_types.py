from datetime import datetime
from pydantic import BaseModel


class ProjectServiceData(BaseModel):
    id: int
    user_id: int
    name: str
    target_role: str | None
    cv_style: str | None
    preferences: dict | None
    created_at: datetime
    updated_at: datetime

