from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database.models import JobOffering
from app.schemas.job_offering_schema import JobOfferingCreate, JobOfferingUpdate


def create_job_offering(db: Session, job_offering_data: JobOfferingCreate) -> JobOffering:
    """Create a new job offering"""
    db_job_offering = JobOffering(**job_offering_data.model_dump())
    db.add(db_job_offering)
    db.commit()
    db.refresh(db_job_offering)
    return db_job_offering


def get_job_offering(db: Session, job_offering_id: str) -> Optional[JobOffering]:
    """Get a job offering by ID"""
    return db.query(JobOffering).filter(JobOffering.id == job_offering_id).first()


def get_job_offerings(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    keyword: str | None = None,
    search: str | None = None
) -> list[JobOffering]:
    """
    Get job offerings with optional filters:
    - keyword: exact match on keyword field
    - search: LIKE search on company_name or role_name
    """
    query = db.query(JobOffering)
    
    # Filtro exacto por keyword
    if keyword:
        query = query.filter(JobOffering.keyword == keyword)
    
    # Filtro tipo LIKE para company_name o role_name
    if search:
        # Sanitize input: SQLAlchemy parameters previenen SQL injection automáticamente
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                JobOffering.company_name.ilike(search_pattern),
                JobOffering.role_name.ilike(search_pattern)
            )
        )
    
    return query.offset(skip).limit(limit).all()


def update_job_offering(
    db: Session, 
    job_offering_id: str, 
    job_offering_data: JobOfferingUpdate
) -> Optional[JobOffering]:
    """Update a job offering"""
    db_job_offering = get_job_offering(db, job_offering_id)
    if not db_job_offering:
        return None
    
    update_data = job_offering_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_job_offering, key, value)
    
    db.commit()
    db.refresh(db_job_offering)
    return db_job_offering


def delete_job_offering(db: Session, job_offering_id: str) -> bool:
    """Delete a job offering"""
    db_job_offering = get_job_offering(db, job_offering_id)
    if not db_job_offering:
        return False
    
    db.delete(db_job_offering)
    db.commit()
    return True

