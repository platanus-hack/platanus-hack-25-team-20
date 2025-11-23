from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.setup import get_db
from app.schemas.application_schema import ApplicationCreate, ApplicationResponse, ApplicationUpdate
from app.services import application_service


router = APIRouter()


@router.post("/applications", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(application_data: ApplicationCreate, db: Session = Depends(get_db)):
    application = application_service.create_application(db, application_data)
    return application


@router.get("/applications/{application_id}", response_model=ApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db)):
    application = application_service.get_application(db, application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application {application_id} not found"
        )
    return application


@router.get("/users/{user_id}/applications", response_model=list[ApplicationResponse])
def get_user_applications(user_id: int, db: Session = Depends(get_db)):
    return application_service.get_user_applications(db, user_id)


@router.get("/job-offerings/{job_offering_id}/applications", response_model=list[ApplicationResponse])
def get_job_offering_applications(job_offering_id: str, db: Session = Depends(get_db)):
    return application_service.get_job_offering_applications(db, job_offering_id)


@router.patch("/applications/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: int,
    application_data: ApplicationUpdate,
    db: Session = Depends(get_db)
):
    application = application_service.update_application(db, application_id, application_data)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application {application_id} not found"
        )
    return application


@router.delete("/applications/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(application_id: int, db: Session = Depends(get_db)):
    success = application_service.delete_application(db, application_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application {application_id} not found"
        )

