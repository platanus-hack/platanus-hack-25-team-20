import instructor
from anthropic import Anthropic
from sqlalchemy.orm import Session

from app.config import settings
from app.database.models import User, UserProfile, UserSkills, SkillType
from app.types.extraction_types import ExtractedProfileData
from app.services import user_profile_service, user_skills_service


client = instructor.from_anthropic(Anthropic(api_key=settings.anthropic_api_key))


def extract_profile_data(db: Session, user_id: int, text: str) -> ExtractedProfileData:
    """
    Extrae información de perfil y skills desde un texto usando LLM.
    Considera la información actual del usuario para evitar redundancias.
    """
    
    # Obtener info actual del usuario
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError(f"User {user_id} not found")
    
    current_profile = user_profile_service.get_user_profile_by_user(db, user_id)
    current_skills = user_skills_service.get_user_skills_by_user(db, user_id)
    
    # Construir prompt con contexto
    prompt_parts = [
        "Eres un experto en análisis de perfiles profesionales.",
        "Tu tarea es extraer información estructurada del siguiente texto.",
        "",
        "INFORMACIÓN ACTUAL DEL USUARIO:",
    ]
    
    if current_profile:
        prompt_parts.extend([
            f"- Rol actual: {current_profile.current_role or 'No especificado'}",
            f"- Años de experiencia: {current_profile.years_of_experience or 'No especificado'}",
            f"- Rango salarial: {current_profile.salary_range or 'No especificado'}",
            f"- Idiomas: {', '.join(current_profile.spoken_languages) if current_profile.spoken_languages else 'No especificados'}",
        ])
    else:
        prompt_parts.append("- No tiene perfil creado aún")
    
    if current_skills:
        prompt_parts.extend([
            "",
            "SKILLS ACTUALES QUE YA TIENE:",
        ])
        for skill in current_skills[:10]:  # Solo mostrar algunos para no saturar
            prompt_parts.append(f"  - [{skill.skill_type.value}] {skill.skill_text[:100]}")
        if len(current_skills) > 10:
            prompt_parts.append(f"  ... y {len(current_skills) - 10} más")
    else:
        prompt_parts.append("\nNo tiene skills registrados aún.")
    
    prompt_parts.extend([
        "",
        "TEXTO DEL USUARIO PARA ANALIZAR:",
        text,
        "",
        "INSTRUCCIONES:",
        "1. Extrae SOLO información NUEVA o que actualice/mejore la existente",
        "2. NO repitas skills que ya están registrados con la misma información",
        "3. Si encuentras información más completa sobre algo existente, puedes incluirla",
        "4. Clasifica los skills correctamente:",
        "   - 'experience': Experiencias laborales, años trabajados, empresas",
        "   - 'dev-skill': Tecnologías, lenguajes, frameworks, herramientas",
        "   - 'certificate': Certificaciones, títulos, cursos completados",
        "   - 'extra': Cualquier otra cosa relevante (idiomas, soft skills, etc.)",
        "5. Para el perfil, actualiza solo si encuentras información más precisa",
        "6. Los idiomas que extraigas para skills tipo 'extra' también agrégalos a spoken_languages del perfil",
        "7. Sé específico en las descripciones de skills (ej: 'Python - 5 años, Django y FastAPI')",
        "",
        "IMPORTANTE: Si no encuentras información nueva relevante, devuelve listas vacías.",
    ])
    
    prompt = "\n".join(prompt_parts)
    
    response = client.chat.completions.create(
        model="claude-haiku-4-5",
        max_tokens=3000,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        response_model=ExtractedProfileData,
    )
    
    return response


def apply_extracted_data(
    db: Session,
    user_id: int,
    extracted_data: ExtractedProfileData
) -> dict:
    """
    Aplica los datos extraídos al usuario:
    - Crea o actualiza UserProfile
    - Agrega nuevos UserSkills
    
    Retorna resumen de lo que se hizo.
    """
    result = {
        "profile_updated": False,
        "profile_created": False,
        "skills_added": 0,
        "details": []
    }
    
    # Aplicar perfil si hay datos
    if extracted_data.profile:
        profile = extracted_data.profile
        current_profile = user_profile_service.get_user_profile_by_user(db, user_id)
        
        if current_profile:
            # Actualizar solo campos que tengan valor nuevo
            update_data = {}
            if profile.current_role:
                update_data["current_role"] = profile.current_role
            if profile.years_of_experience is not None:
                update_data["years_of_experience"] = profile.years_of_experience
            if profile.salary_range:
                update_data["salary_range"] = profile.salary_range
            if profile.spoken_languages:
                # Combinar idiomas sin duplicados
                existing = set(current_profile.spoken_languages or [])
                new_langs = set(profile.spoken_languages)
                combined = list(existing | new_langs)
                update_data["spoken_languages"] = combined
            
            if update_data:
                from app.schemas.user_profile_schema import UserProfileUpdate
                user_profile_service.update_user_profile(
                    db, current_profile.id, UserProfileUpdate(**update_data)
                )
                result["profile_updated"] = True
                result["details"].append(f"Perfil actualizado con: {', '.join(update_data.keys())}")
        else:
            # Crear nuevo perfil
            from app.schemas.user_profile_schema import UserProfileCreate
            user_profile_service.create_user_profile(
                db, user_id, UserProfileCreate(
                    current_role=profile.current_role,
                    years_of_experience=profile.years_of_experience,
                    salary_range=profile.salary_range,
                    spoken_languages=profile.spoken_languages
                )
            )
            result["profile_created"] = True
            result["details"].append("Perfil creado")
    
    # Agregar skills
    if extracted_data.skills:
        from app.schemas.user_skills_schema import UserSkillsCreate
        
        for skill in extracted_data.skills:
            # Convertir string a SkillType
            skill_type_map = {
                "experience": SkillType.EXPERIENCE,
                "dev-skill": SkillType.DEV_SKILL,
                "certificate": SkillType.CERTIFICATE,
                "extra": SkillType.EXTRA
            }
            skill_type = skill_type_map.get(skill.skill_type, SkillType.EXTRA)
            
            user_skills_service.create_user_skills(
                db, user_id, UserSkillsCreate(
                    skill_text=skill.skill_text,
                    skill_type=skill_type,
                    source=skill.source
                )
            )
            result["skills_added"] += 1
        
        result["details"].append(f"{result['skills_added']} skills agregados")
    
    return result

