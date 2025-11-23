from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database.setup import get_db
from app.schemas.job_offering_schema import JobOfferingResponse
from app.services import job_offering_service


router = APIRouter()


@router.get("/job-offerings/{job_offering_id}", response_model=JobOfferingResponse)
def get_job_offering(job_offering_id: str, db: Session = Depends(get_db)):
    """Get a specific job offering by ID"""
    job_offering = job_offering_service.get_job_offering(db, job_offering_id)
    if not job_offering:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job offering {job_offering_id} not found"
        )
    return job_offering


@router.get("/job-offerings", response_model=list[JobOfferingResponse])
def list_job_offerings(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Max number of records to return"),
    keyword: str | None = Query(None, description="Exact match filter on keyword field"),
    search: str | None = Query(None, description="Search in company_name or role_name (case-insensitive)"),
    db: Session = Depends(get_db)
):
    """
    List job offerings with optional filters:
    
    - **keyword**: Exact match on the keyword field (e.g., "python-backend")
    - **search**: Fuzzy search in company_name or role_name (e.g., "Google" or "Engineer")
    
    Both filters can be combined for more precise results.
    
    Examples:
    - `/job-offerings?keyword=python-backend` → All offers with exact keyword "python-backend"
    - `/job-offerings?search=Google` → All offers from companies with "Google" in name or role
    - `/job-offerings?keyword=python&search=Senior` → Python offers with "Senior" in company/role
    """
    return job_offering_service.get_job_offerings(
        db=db,
        skip=skip,
        limit=limit,
        keyword=keyword,
        search=search
    )

