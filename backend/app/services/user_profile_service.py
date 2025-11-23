from typing import Optional

from sqlalchemy.orm import Session

from app.database.models import UserProfile
from app.schemas.user_profile_schema import UserProfileCreate, UserProfileUpdate


def create_user_profile(db: Session, user_id: int, profile_data: UserProfileCreate) -> UserProfile:
    """Crea un perfil de usuario (1:1 con User)"""
    db_profile = UserProfile(
        user_id=user_id,
        current_role=profile_data.current_role,
        years_of_experience=profile_data.years_of_experience,
        salary_range=profile_data.salary_range,
        spoken_languages=profile_data.spoken_languages,
    )
    
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def get_user_profile(db: Session, profile_id: int) -> Optional[UserProfile]:
    """Obtiene un perfil por ID"""
    return db.query(UserProfile).filter(UserProfile.id == profile_id).first()


def get_user_profile_by_user(db: Session, user_id: int) -> Optional[UserProfile]:
    """Obtiene el perfil de un usuario específico"""
    return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()


def update_user_profile(
    db: Session,
    profile_id: int,
    profile_data: UserProfileUpdate
) -> Optional[UserProfile]:
    """Actualiza un perfil existente"""
    profile = get_user_profile(db, profile_id)
    if not profile:
        return None
    
    if profile_data.current_role is not None:
        profile.current_role = profile_data.current_role
    if profile_data.years_of_experience is not None:
        profile.years_of_experience = profile_data.years_of_experience
    if profile_data.salary_range is not None:
        profile.salary_range = profile_data.salary_range
    if profile_data.spoken_languages is not None:
        profile.spoken_languages = profile_data.spoken_languages
    
    db.commit()
    db.refresh(profile)
    return profile


def delete_user_profile(db: Session, profile_id: int) -> bool:
    """Elimina un perfil"""
    profile = get_user_profile(db, profile_id)
    if not profile:
        return False
    
    db.delete(profile)
    db.commit()
    return True

