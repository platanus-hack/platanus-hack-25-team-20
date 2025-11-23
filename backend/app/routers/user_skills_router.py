from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.setup import get_db
from app.schemas.user_skills_schema import (
    UserSkillsCreate, 
    UserSkillsResponse, 
    UserSkillsUpdate,
    UserSkillsGroupedResponse
)
from app.services import user_skills_service


router = APIRouter()


@router.post("/users/{user_id}/skills", response_model=UserSkillsResponse, status_code=status.HTTP_201_CREATED)
def create_user_skills(user_id: int, skills_data: UserSkillsCreate, db: Session = Depends(get_db)):
    skills = user_skills_service.create_user_skills(db, user_id, skills_data)
    return skills


@router.get("/skills/{skills_id}", response_model=UserSkillsResponse)
def get_user_skills(skills_id: int, db: Session = Depends(get_db)):
    skills = user_skills_service.get_user_skills(db, skills_id)
    if not skills:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"UserSkills with ID {skills_id} not found"
        )
    return skills


@router.get("/users/{user_id}/skills", response_model=UserSkillsGroupedResponse)
def get_user_skills_by_user(user_id: int, db: Session = Depends(get_db)):
    """Obtiene los skills del usuario agrupados por tipo (experience, dev-skills, certificates, extra)"""
    grouped_skills = user_skills_service.get_user_skills_by_user_grouped(db, user_id)
    return grouped_skills


@router.patch("/skills/{skills_id}", response_model=UserSkillsResponse)
def update_user_skills(skills_id: int, skills_data: UserSkillsUpdate, db: Session = Depends(get_db)):
    skills = user_skills_service.update_user_skills(db, skills_id, skills_data)
    if not skills:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"UserSkills with ID {skills_id} not found"
        )
    return skills


@router.delete("/skills/{skills_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_skills(skills_id: int, db: Session = Depends(get_db)):
    deleted = user_skills_service.delete_user_skills(db, skills_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"UserSkills with ID {skills_id} not found"
        )

