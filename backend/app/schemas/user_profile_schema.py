from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UserProfileCreate(BaseModel):
    current_role: str | None = None
    years_of_experience: int | None = None
    salary_range: str | None = None
    spoken_languages: list[str] = []


class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    current_role: str | None
    years_of_experience: int | None
    salary_range: str | None
    spoken_languages: list[str]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserProfileUpdate(BaseModel):
    current_role: str | None = None
    years_of_experience: int | None = None
    salary_range: str | None = None
    spoken_languages: list[str] | None = None

