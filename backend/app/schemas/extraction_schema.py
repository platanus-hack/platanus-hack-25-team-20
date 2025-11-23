from pydantic import BaseModel, Field


class ExtractProfileRequest(BaseModel):
    """Request para extraer información de un texto"""
    text: str = Field(..., description="Texto con información del usuario (CV, LinkedIn, etc.)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": """Soy un desarrollador full-stack con 5 años de experiencia. 
                Trabajé 3 años en Google como Software Engineer donde desarrollé microservicios en Python y Go.
                Tengo certificación AWS Solutions Architect. 
                Manejo Python (expert), JavaScript/TypeScript, React, Django, FastAPI.
                Hablo inglés fluido y español nativo.
                Busco posiciones Senior con salario entre $120k-$150k."""
            }
        }


class ExtractProfileResponse(BaseModel):
    """Response con resultados de la extracción"""
    message: str
    profile_updated: bool
    profile_created: bool
    skills_added: int
    details: list[str]

