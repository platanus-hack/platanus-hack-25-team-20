from pydantic import BaseModel, Field


class ExtractedProfile(BaseModel):
    """Información de perfil extraída del texto"""
    current_role: str | None = Field(None, description="Rol o cargo actual del usuario")
    years_of_experience: int | None = Field(None, description="Años totales de experiencia profesional")
    salary_range: str | None = Field(None, description="Rango salarial esperado o actual")
    spoken_languages: list[str] = Field(default_factory=list, description="Idiomas que habla el usuario")


class ExtractedSkill(BaseModel):
    """Skill individual extraído del texto"""
    skill_text: str = Field(..., description="Descripción del skill, experiencia, certificado, etc.")
    skill_type: str = Field(..., description="Tipo: 'experience', 'dev-skill', 'certificate', o 'extra'")
    source: str = Field(default="text_extraction", description="Fuente de donde se extrajo")


class ExtractedProfileData(BaseModel):
    """Resultado completo de la extracción"""
    profile: ExtractedProfile | None = Field(None, description="Información de perfil si se encontró")
    skills: list[ExtractedSkill] = Field(default_factory=list, description="Lista de skills extraídos")
    
    class Config:
        json_schema_extra = {
            "example": {
                "profile": {
                    "current_role": "Senior Software Engineer",
                    "years_of_experience": 5,
                    "salary_range": "$100k-$150k",
                    "spoken_languages": ["English", "Spanish"]
                },
                "skills": [
                    {
                        "skill_text": "Python - Expert level, 5+ años de experiencia",
                        "skill_type": "dev-skill",
                        "source": "text_extraction"
                    },
                    {
                        "skill_text": "Trabajé 3 años en Google como SWE",
                        "skill_type": "experience",
                        "source": "text_extraction"
                    }
                ]
            }
        }

