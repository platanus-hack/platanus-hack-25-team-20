from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified

from app.database.models import CV, User, UserSkills, Project, Template
from app.schemas.cv_schema import CVCreate, CVUpdate
from app.services import llm_service, template_service


def create_cv(db: Session, cv_data: CVCreate) -> CV:
    """
    Crea un nuevo CV con generación automática de contenido usando LLM.
    """
    template = db.query(Template).filter(Template.id == cv_data.template_id).first()
    if not template:
        raise ValueError(f"Template {cv_data.template_id} not found")
    
    project = db.query(Project).filter(Project.id == cv_data.project_id).first()
    if not project:
        raise ValueError(f"Project {cv_data.project_id} not found")
    
    user = db.query(User).filter(User.id == project.user_id).first()
    if not user:
        raise ValueError(f"User {project.user_id} not found")
    
    user_skills = db.query(UserSkills).filter(UserSkills.user_id == user.id).all()
    
    base_cv = None
    if cv_data.base_cv_id:
        base_cv = db.query(CV).filter(CV.id == cv_data.base_cv_id).first()
    
    # TODO: Obtener company_info cuando tengamos las tablas Empresa/JobOffer
    company_info = None
    
    # Convertir messages a formato interno
    conversation_history = []
    for msg in cv_data.messages:
        conversation_history.append({
            "role": msg.role,
            "content": msg.content,
            "timestamp": msg.timestamp or datetime.utcnow().isoformat(),
        })
    
    # Si no hay mensajes, agregar uno por defecto
    if not conversation_history:
        conversation_history.append({
            "role": "user",
            "content": "Generar CV profesional",
            "timestamp": datetime.utcnow().isoformat(),
        })
    
    generated_content = llm_service.generate_cv_content(
        db=db,
        user=user,
        user_skills=user_skills,
        project=project,
        base_cv=base_cv,
        company_info=company_info,
        conversation_history=conversation_history,
    )
    
    content_dict = generated_content.model_dump()
    
    rendered_content = template_service.render_template(template, content_dict)
    
    db_cv = CV(
        project_id=cv_data.project_id,
        template_id=cv_data.template_id,
        base_cv_id=cv_data.base_cv_id,
        content=content_dict,
        rendered_content=rendered_content,
        conversation_history=conversation_history,
    )
    
    db.add(db_cv)
    db.commit()
    db.refresh(db_cv)
    return db_cv


def get_cv(db: Session, cv_id: int) -> Optional[CV]:
    return db.query(CV).filter(CV.id == cv_id).first()


def get_project_cvs(db: Session, project_id: int) -> list[CV]:
    return db.query(CV).filter(CV.project_id == project_id).all()


def update_cv(db: Session, cv_id: int, cv_data: CVUpdate) -> Optional[CV]:
    cv = get_cv(db, cv_id)
    if not cv:
        return None
    
    content_changed = False
    
    if cv_data.content is not None:
        cv.content = cv_data.content
        content_changed = True
    
    if cv_data.messages is not None and len(cv_data.messages) > 0:
        if cv.conversation_history is None:
            cv.conversation_history = []
        
        # Agregar nuevos mensajes al historial
        for msg in cv_data.messages:
            cv.conversation_history.append({
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp or datetime.utcnow().isoformat(),
            })
        flag_modified(cv, "conversation_history")
    
    if content_changed:
        template = db.query(Template).filter(Template.id == cv.template_id).first()
        if template:
            cv.rendered_content = template_service.render_template(template, cv.content)
    
    db.commit()
    db.refresh(cv)
    return cv


def delete_cv(db: Session, cv_id: int) -> bool:
    cv = get_cv(db, cv_id)
    if not cv:
        return False
    
    db.delete(cv)
    db.commit()
    return True


def regenerate_cv(
    db: Session,
    cv_id: int,
    new_messages: list[dict]
) -> Optional[CV]:
    """
    Regenera un CV existente con nuevos mensajes del chat.
    """
    cv = get_cv(db, cv_id)
    if not cv:
        return None
    
    project = db.query(Project).filter(Project.id == cv.project_id).first()
    if not project:
        return None
    
    user = db.query(User).filter(User.id == project.user_id).first()
    if not user:
        return None
    
    user_skills = db.query(UserSkills).filter(UserSkills.user_id == user.id).all()
    template = db.query(Template).filter(Template.id == cv.template_id).first()
    
    company_info = None
    
    # Agregar nuevos mensajes al historial existente
    if cv.conversation_history is None:
        cv.conversation_history = []
    
    updated_history = cv.conversation_history.copy()
    updated_history.extend(new_messages)
    
    generated_content = llm_service.generate_cv_content(
        db=db,
        user=user,
        user_skills=user_skills,
        project=project,
        base_cv=cv,
        company_info=company_info,
        conversation_history=updated_history,
    )
    
    content_dict = generated_content.model_dump()
    cv.content = content_dict
    
    if template:
        cv.rendered_content = template_service.render_template(template, content_dict)
    
    # Actualizar historial con los nuevos mensajes
    cv.conversation_history = updated_history
    flag_modified(cv, "conversation_history")
    
    db.commit()
    db.refresh(cv)
    return cv
