from datetime import datetime
from pydantic import BaseModel, ConfigDict


class JobOfferingCreate(BaseModel):
    id: str
    keyword: str
    company_name: str | None = None
    description: str | None = None
    url: str | None = None
    salary: str | None = None
    role_name: str | None = None
    location: str | None = None
    work_mode: str | None = None
    type: str | None = None
    post_date: datetime | None = None
    last_updated: datetime | None = None
    sectors: str | None = None
    extra_data: dict | None = None
    uid: str | None = None
    api_url: str | None = None


class JobOfferingResponse(BaseModel):
    id: str
    keyword: str
    company_name: str | None
    description: str | None
    url: str | None
    salary: str | None
    role_name: str | None
    location: str | None
    work_mode: str | None
    type: str | None
    post_date: datetime | None
    last_updated: datetime | None
    sectors: str | None
    extra_data: dict | None
    uid: str | None
    created_at: datetime
    updated_at: datetime
    api_url: str | None
    
    model_config = ConfigDict(from_attributes=True)


class JobOfferingUpdate(BaseModel):
    keyword: str | None = None
    company_name: str | None = None
    description: str | None = None
    url: str | None = None
    salary: str | None = None
    role_name: str | None = None
    location: str | None = None
    work_mode: str | None = None
    type: str | None = None
    post_date: datetime | None = None
    last_updated: datetime | None = None
    sectors: str | None = None
    extra_data: dict | None = None
    uid: str | None = None
    api_url: str | None = None

