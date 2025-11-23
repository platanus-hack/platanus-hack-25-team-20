import re
import instructor
from anthropic import Anthropic
from sqlalchemy.orm import Session

from app.config import settings
from app.database.models import User, UserSkills, Project, CV
from app.types.cv_content_types import GeneratedCVContentSimple


client = instructor.from_anthropic(Anthropic(api_key=settings.anthropic_api_key))


def clean_html_text(text: str) -> str:
    """
    Limpia tags HTML de un texto, dejando solo el contenido legible.
    
    Args:
        text: Texto con posibles tags HTML
        
    Returns:
        Texto limpio sin tags HTML
    """
    if not text:
        return text
    
    # Eliminar tags HTML
    text = re.sub(r'<[^>]+>', '', text)
    
    # Decodificar entidades HTML comunes
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&amp;', '&')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    
    # Limpiar espacios múltiples y saltos de línea excesivos
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    return text.strip()


def generate_cv_content(
    db: Session,
    user: User,
    user_skills: list[UserSkills],
    project: Project,
    base_cv: CV | None = None,
    company_info: dict | None = None,
    conversation_history: list[dict] | None = None,
) -> GeneratedCVContentSimple:
    """
    Genera el contenido estructurado de un CV usando LLM (Anthropic + Instructor).
    
    Devuelve un objeto Pydantic con exactamente los campos que el template necesita.
    """
    
    prompt_parts = [
        "Eres un experto en la creación de CVs profesionales.",
        "Tu tarea es generar un CV completo y atractivo basado en la información proporcionada.",
        "",
        "INFORMACIÓN DEL USUARIO:",
        f"- Nombre: {user.full_name}",
        f"- Email: {user.email}",
    ]
    
    if user_skills:
        from app.database.models import SkillType
        
        experiences = [s for s in user_skills if s.skill_type == SkillType.EXPERIENCE]
        dev_skills = [s for s in user_skills if s.skill_type == SkillType.DEV_SKILL]
        certificates = [s for s in user_skills if s.skill_type == SkillType.CERTIFICATE]
        extras = [s for s in user_skills if s.skill_type == SkillType.EXTRA]
        
        prompt_parts.extend([
            "",
            "INFORMACIÓN DE HABILIDADES Y EXPERIENCIA:",
        ])
        
        if experiences:
            prompt_parts.append("\nEXPERIENCIA:")
            for exp in experiences:
                source_info = f" [Fuente: {exp.source}]" if exp.source else ""
                prompt_parts.append(f"  - {exp.skill_text}{source_info}")
        
        if dev_skills:
            prompt_parts.append("\nHABILIDADES TÉCNICAS:")
            for skill in dev_skills:
                source_info = f" [Fuente: {skill.source}]" if skill.source else ""
                prompt_parts.append(f"  - {skill.skill_text}{source_info}")
        
        if certificates:
            prompt_parts.append("\nCERTIFICADOS:")
            for cert in certificates:
                source_info = f" [Fuente: {cert.source}]" if cert.source else ""
                prompt_parts.append(f"  - {cert.skill_text}{source_info}")
        
        if extras:
            prompt_parts.append("\nINFORMACIÓN ADICIONAL:")
            for extra in extras:
                source_info = f" [Fuente: {extra.source}]" if extra.source else ""
                prompt_parts.append(f"  - {extra.skill_text}{source_info}")
    
    if project:
        prompt_parts.extend([
            "",
            "PREFERENCIAS DEL PROYECTO:",
            f"- Nombre del proyecto: {project.name}",
            f"- Rol objetivo: {project.target_role or 'No especificado'}",
            f"- Estilo deseado: {project.cv_style or 'Profesional'}",
        ])
        if project.preferences:
            prompt_parts.append(f"- Preferencias adicionales: {project.preferences}")
    
    if base_cv:
        prompt_parts.extend([
            "",
            "CV BASE (partir de aquí y mejorar):",
            f"{base_cv.content}",
            "",
            "IMPORTANTE: Usa el CV base como punto de partida y mejóralo/adáptalo según las nuevas instrucciones.",
        ])
    
    if company_info:
        # Limpiar HTML de la información de la empresa antes de enviarlo al LLM
        cleaned_info = company_info
        if isinstance(company_info, dict):
            cleaned_info = {
                key: clean_html_text(str(value)) if isinstance(value, str) else value
                for key, value in company_info.items()
            }
        elif isinstance(company_info, str):
            cleaned_info = clean_html_text(company_info)
        
        prompt_parts.extend([
            "",
            "INFORMACIÓN DE LA EMPRESA/OFERTA:",
            f"{cleaned_info}",
            "",
            "Adapta el CV específicamente para esta empresa y posición.",
        ])
    else:
        prompt_parts.extend([
            "",
            "NOTA: No hay información específica de empresa. Genera un CV genérico pero profesional.",
        ])
    
    if conversation_history:
        prompt_parts.extend([
            "",
            "CONVERSACIÓN CON EL USUARIO:",
        ])
        for msg in conversation_history:
            role_label = "Usuario" if msg["role"] == "user" else "Asistente"
            prompt_parts.append(f"{role_label}: {msg['content']}")
    
    prompt_parts.extend([
        "",
        "FORMATO REQUERIDO:",
        "- Genera experiencias laborales realistas y relevantes (al menos 2)",
        "- Incluye educación apropiada al perfil (al menos 1)",
        "- Organiza habilidades por categorías (al menos 3 categorías)",
        "- Escribe todo en ESPAÑOL",
        "- El resumen debe ser conciso (2-3 líneas)",
        "- Las descripciones deben ser claras y orientadas a resultados",
        f"- IMPORTANTE: Usa EXACTAMENTE el nombre '{user.full_name}' sin modificarlo. Divide en firstname y lastname según corresponda.",
        "- Si no tienes información específica de experiencia o educación, inventa datos profesionales coherentes",
        "",
        "RESPUESTA DEL CHAT:",
        "- Genera un campo 'chat_response' con una respuesta MUY CONCISA (máximo 2 líneas)",
        "- Solo menciona LO MÁS IMPORTANTE que se agregó/modificó en el CV",
        "- Formato ejemplo: 'He agregado experiencia en [empresa] y actualizado las habilidades técnicas.'",
        "- Si es la primera generación: 'He creado tu CV con [X] experiencias y [Y] habilidades.'",
        "- Sé específico pero breve. NO des explicaciones largas.",
    ])
    
    prompt = "\n".join(prompt_parts)
    
    response = client.chat.completions.create(
        model="claude-haiku-4-5",
        max_tokens=4000,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        response_model=GeneratedCVContentSimple,
    )
    
    return response
