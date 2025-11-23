from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.setup import get_db
from app.schemas.template_schema import TemplateResponse, TemplateDetail
from app.services import template_service


router = APIRouter()


@router.get("/templates", response_model=list[TemplateResponse])
def get_templates(db: Session = Depends(get_db)):
    templates = template_service.get_templates(db)
    return templates


@router.get("/templates/{template_id}", response_model=TemplateDetail)
def get_template(template_id: int, db: Session = Depends(get_db)):
    template = template_service.get_template(db, template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template with ID {template_id} not found"
        )
    return template

