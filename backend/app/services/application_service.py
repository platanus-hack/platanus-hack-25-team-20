from typing import Optional

from sqlalchemy.orm import Session

from app.database.models import Application
from app.schemas.application_schema import ApplicationCreate, ApplicationUpdate


def create_application(db: Session, application_data: ApplicationCreate) -> Application:
    db_application = Application(
        user_id=application_data.user_id,
        job_offering_id=application_data.job_offering_id,
        status=application_data.status,
        notes=application_data.notes,
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application


def get_application(db: Session, application_id: int) -> Optional[Application]:
    return db.query(Application).filter(Application.id == application_id).first()


def get_user_applications(db: Session, user_id: int) -> list[Application]:
    return db.query(Application).filter(Application.user_id == user_id).all()


def get_job_offering_applications(db: Session, job_offering_id: str) -> list[Application]:
    return db.query(Application).filter(Application.job_offering_id == job_offering_id).all()


def update_application(
    db: Session, application_id: int, application_data: ApplicationUpdate
) -> Optional[Application]:
    application = get_application(db, application_id)
    if not application:
        return None
    
    if application_data.status is not None:
        application.status = application_data.status
    if application_data.notes is not None:
        application.notes = application_data.notes
    if application_data.cv_id is not None:
        application.cv_id = application_data.cv_id
    
    db.commit()
    db.refresh(application)
    return application


def delete_application(db: Session, application_id: int) -> bool:
    application = get_application(db, application_id)
    if not application:
        return False
    
    db.delete(application)
    db.commit()
    return True

