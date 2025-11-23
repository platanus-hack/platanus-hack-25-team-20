from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ApplicationCreate(BaseModel):
    user_id: int
    job_offering_id: str
    status: str = "draft"
    notes: str | None = None


class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    job_offering_id: str
    cv_id: int | None
    status: str
    notes: str | None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ApplicationUpdate(BaseModel):
    status: str | None = None
    notes: str | None = None
    cv_id: int | None = None

