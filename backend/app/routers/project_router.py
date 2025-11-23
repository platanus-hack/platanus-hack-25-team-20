from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.setup import get_db
from app.schemas.project_schema import ProjectCreate, ProjectResponse, ProjectUpdate
from app.services import project_service


router = APIRouter()


@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project_data: ProjectCreate, user_id: int, db: Session = Depends(get_db)):
    project = project_service.create_project(db, user_id, project_data)
    return project


@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    return project


@router.get("/users/{user_id}/projects", response_model=list[ProjectResponse])
def get_user_projects(user_id: int, db: Session = Depends(get_db)):
    projects = project_service.get_user_projects(db, user_id)
    return projects


@router.patch("/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project_data: ProjectUpdate, db: Session = Depends(get_db)):
    project = project_service.update_project(db, project_id, project_data)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    return project


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    deleted = project_service.delete_project(db, project_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )

