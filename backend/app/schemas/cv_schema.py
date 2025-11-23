from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ChatMessage(BaseModel):
    """Mensaje individual del chat"""
    role: str  # "user" o "assistant"
    content: str
    timestamp: str | None = None


class CVCreate(BaseModel):
    project_id: int
    template_id: int
    base_cv_id: int | None = None
    messages: list[ChatMessage] = []  # Lista de mensajes del chat


class CVResponse(BaseModel):
    id: int
    project_id: int
    template_id: int
    base_cv_id: int | None
    content: dict
    rendered_content: str | None
    compiled_path: str | None
    conversation_history: list | None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class CVUpdate(BaseModel):
    content: dict | None = None
    messages: list[ChatMessage] | None = None  # Agregar nuevos mensajes


class CVRegenerateRequest(BaseModel):
    """Request para regenerar un CV con nuevos mensajes"""
    messages: list[ChatMessage]  # Nuevos mensajes para iterar
