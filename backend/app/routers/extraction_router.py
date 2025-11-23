from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.setup import get_db
from app.schemas.extraction_schema import ExtractProfileRequest, ExtractProfileResponse
from app.services import extraction_service


router = APIRouter()


@router.post("/users/{user_id}/extract-profile", response_model=ExtractProfileResponse, status_code=status.HTTP_200_OK)
def extract_and_update_profile(
    user_id: int,
    request: ExtractProfileRequest,
    db: Session = Depends(get_db)
):
    """
    Extrae información de perfil y skills desde un texto usando LLM.
    
    - Analiza el texto y extrae información estructurada
    - Considera la información actual para evitar redundancias
    - Actualiza o crea UserProfile si encuentra datos relevantes
    - Agrega nuevos UserSkills sin duplicar los existentes
    
    **Ejemplos de texto válido:**
    - CV completo
    - Perfil de LinkedIn
    - Descripción libre del usuario
    - Combinación de experiencias y habilidades
    
    El LLM es inteligente y clasificará automáticamente:
    - Experiencias laborales → skill_type: "experience"
    - Tecnologías/herramientas → skill_type: "dev-skill"
    - Certificaciones → skill_type: "certificate"
    - Otros (idiomas, soft skills) → skill_type: "extra"
    """
    try:
        # Extraer datos con LLM
        extracted_data = extraction_service.extract_profile_data(db, user_id, request.text)
        
        # Aplicar los datos extraídos
        result = extraction_service.apply_extracted_data(db, user_id, extracted_data)
        
        # Construir mensaje de respuesta
        if result["skills_added"] == 0 and not result["profile_updated"] and not result["profile_created"]:
            message = "No se encontró información nueva para agregar"
        else:
            parts = []
            if result["profile_created"]:
                parts.append("perfil creado")
            elif result["profile_updated"]:
                parts.append("perfil actualizado")
            if result["skills_added"] > 0:
                parts.append(f"{result['skills_added']} skills agregados")
            message = "Éxito: " + ", ".join(parts)
        
        return ExtractProfileResponse(
            message=message,
            profile_updated=result["profile_updated"],
            profile_created=result["profile_created"],
            skills_added=result["skills_added"],
            details=result["details"]
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error extracting profile data: {str(e)}"
        )

