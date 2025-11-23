from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TemplateResponse(BaseModel):
    id: int
    name: str
    description: str | None
    template_type: str
    style: str | None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class TemplateDetail(TemplateResponse):
    template_content: str

