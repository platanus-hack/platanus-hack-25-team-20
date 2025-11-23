from datetime import datetime
from pydantic import BaseModel


class UserSkillsServiceData(BaseModel):
    id: int
    user_id: int
    skills_data: dict
    raw_input: str | None
    created_at: datetime
    updated_at: datetime

