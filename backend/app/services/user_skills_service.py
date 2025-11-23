from typing import Optional

from sqlalchemy.orm import Session

from app.database.models import UserSkills, SkillType
from app.schemas.user_skills_schema import UserSkillsCreate, UserSkillsUpdate, UserSkillsGroupedResponse


def create_user_skills(db: Session, user_id: int, skills_data: UserSkillsCreate) -> UserSkills:
    db_skills = UserSkills(
        user_id=user_id,
        skill_text=skills_data.skill_text,
        skill_type=skills_data.skill_type,
        raw_input=skills_data.raw_input,
        source=skills_data.source,
    )
    
    db.add(db_skills)
    db.commit()
    db.refresh(db_skills)
    return db_skills


def get_user_skills(db: Session, skills_id: int) -> Optional[UserSkills]:
    return db.query(UserSkills).filter(UserSkills.id == skills_id).first()


def get_user_skills_by_user(db: Session, user_id: int) -> list[UserSkills]:
    return db.query(UserSkills).filter(UserSkills.user_id == user_id).all()


def get_user_skills_by_user_grouped(db: Session, user_id: int) -> UserSkillsGroupedResponse:
    """Obtiene los skills de un usuario agrupados por tipo"""
    skills = get_user_skills_by_user(db, user_id)
    
    grouped = UserSkillsGroupedResponse()
    
    for skill in skills:
        if skill.skill_type == SkillType.EXPERIENCE:
            grouped.experience.append(skill)
        elif skill.skill_type == SkillType.DEV_SKILL:
            grouped.dev_skills.append(skill)
        elif skill.skill_type == SkillType.CERTIFICATE:
            grouped.certificates.append(skill)
        elif skill.skill_type == SkillType.EXTRA:
            grouped.extra.append(skill)
    
    return grouped


def update_user_skills(
    db: Session,
    skills_id: int,
    skills_data: UserSkillsUpdate
) -> Optional[UserSkills]:
    skills = get_user_skills(db, skills_id)
    if not skills:
        return None
    
    if skills_data.skill_text is not None:
        skills.skill_text = skills_data.skill_text
    if skills_data.skill_type is not None:
        skills.skill_type = skills_data.skill_type
    if skills_data.raw_input is not None:
        skills.raw_input = skills_data.raw_input
    if skills_data.source is not None:
        skills.source = skills_data.source
    
    db.commit()
    db.refresh(skills)
    return skills


def delete_user_skills(db: Session, skills_id: int) -> bool:
    skills = get_user_skills(db, skills_id)
    if not skills:
        return False
    
    db.delete(skills)
    db.commit()
    return True

