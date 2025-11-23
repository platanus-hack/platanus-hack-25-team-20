from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.setup import get_db
from app.schemas.cv_schema import CVCreate, CVResponse, CVUpdate, CVRegenerateRequest
from app.services import cv_service


router = APIRouter()


@router.post("/projects/{project_id}/cvs", response_model=CVResponse, status_code=201)
def create_cv(project_id: int, cv: CVCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo CV con generación de LLM.
    
    - **messages**: Lista de mensajes del chat (role: "user" o "assistant", content: texto)
    - Si no se pasan mensajes, se usa un mensaje por defecto
    """
    if cv.project_id != project_id:
        raise HTTPException(status_code=400, detail="Project ID mismatch")
    
    try:
        db_cv = cv_service.create_cv(db, cv)
        return db_cv
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/cvs/{cv_id}", response_model=CVResponse)
def get_cv(cv_id: int, db: Session = Depends(get_db)):
    cv = cv_service.get_cv(db, cv_id)
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")
    return cv


@router.get("/projects/{project_id}/cvs", response_model=list[CVResponse])
def get_project_cvs(project_id: int, db: Session = Depends(get_db)):
    return cv_service.get_project_cvs(db, project_id)


@router.patch("/cvs/{cv_id}", response_model=CVResponse)
def update_cv(cv_id: int, cv: CVUpdate, db: Session = Depends(get_db)):
    """
    Actualiza un CV existente.
    
    - Puede actualizar content manualmente
    - Puede agregar nuevos mensajes al conversation_history sin regenerar
    """
    db_cv = cv_service.update_cv(db, cv_id, cv)
    if not db_cv:
        raise HTTPException(status_code=404, detail="CV not found")
    return db_cv


@router.delete("/cvs/{cv_id}", status_code=204)
def delete_cv(cv_id: int, db: Session = Depends(get_db)):
    success = cv_service.delete_cv(db, cv_id)
    if not success:
        raise HTTPException(status_code=404, detail="CV not found")


@router.post("/cvs/{cv_id}/regenerate", response_model=CVResponse)
def regenerate_cv(
    cv_id: int,
    request: CVRegenerateRequest,
    db: Session = Depends(get_db)
):
    """
    Regenera un CV con nuevos mensajes del chat.
    
    Los nuevos mensajes se agregan al historial existente y se regenera el CV completo
    con el LLM tomando en cuenta toda la conversación.
    """
    # Convertir ChatMessage a dict
    new_messages = []
    for msg in request.messages:
        new_messages.append({
            "role": msg.role,
            "content": msg.content,
            "timestamp": msg.timestamp or datetime.utcnow().isoformat(),
        })
    
    cv = cv_service.regenerate_cv(db, cv_id, new_messages)
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")
    return cv
