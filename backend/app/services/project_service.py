from typing import Optional

from sqlalchemy.orm import Session

from app.database.models import Project
from app.schemas.project_schema import ProjectCreate, ProjectUpdate


def create_project(db: Session, user_id: int, project_data: ProjectCreate) -> Project:
    db_project = Project(
        user_id=user_id,
        name=project_data.name,
        target_role=project_data.target_role,
        cv_style=project_data.cv_style,
        preferences=project_data.preferences,
    )
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_project(db: Session, project_id: int) -> Optional[Project]:
    return db.query(Project).filter(Project.id == project_id).first()


def get_user_projects(db: Session, user_id: int) -> list[Project]:
    return db.query(Project).filter(Project.user_id == user_id).all()


def update_project(
    db: Session,
    project_id: int,
    project_data: ProjectUpdate
) -> Optional[Project]:
    project = get_project(db, project_id)
    if not project:
        return None
    
    if project_data.name is not None:
        project.name = project_data.name
    if project_data.target_role is not None:
        project.target_role = project_data.target_role
    if project_data.cv_style is not None:
        project.cv_style = project_data.cv_style
    if project_data.preferences is not None:
        project.preferences = project_data.preferences
    
    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project_id: int) -> bool:
    project = get_project(db, project_id)
    if not project:
        return False
    
    db.delete(project)
    db.commit()
    return True

