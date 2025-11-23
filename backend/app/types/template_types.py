from datetime import datetime
from pydantic import BaseModel


class TemplateServiceData(BaseModel):
    id: int
    name: str
    description: str | None
    template_type: str
    template_content: str
    style: str | None
    created_at: datetime

