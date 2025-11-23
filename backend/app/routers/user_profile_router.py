from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.setup import get_db
from app.schemas.user_profile_schema import UserProfileCreate, UserProfileResponse, UserProfileUpdate
from app.services import user_profile_service


router = APIRouter()


@router.post("/users/{user_id}/profile", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
def create_user_profile(user_id: int, profile_data: UserProfileCreate, db: Session = Depends(get_db)):
    existing_profile = user_profile_service.get_user_profile_by_user(db, user_id)
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {user_id} already has a profile"
        )
    
    profile = user_profile_service.create_user_profile(db, user_id, profile_data)
    return profile


@router.get("/profiles/{profile_id}", response_model=UserProfileResponse)
def get_user_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = user_profile_service.get_user_profile(db, profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"UserProfile with ID {profile_id} not found"
        )
    return profile


@router.get("/users/{user_id}/profile", response_model=UserProfileResponse)
def get_user_profile_by_user(user_id: int, db: Session = Depends(get_db)):
    profile = user_profile_service.get_user_profile_by_user(db, user_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} does not have a profile"
        )
    return profile


@router.patch("/profiles/{profile_id}", response_model=UserProfileResponse)
def update_user_profile(profile_id: int, profile_data: UserProfileUpdate, db: Session = Depends(get_db)):
    profile = user_profile_service.update_user_profile(db, profile_id, profile_data)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"UserProfile with ID {profile_id} not found"
        )
    return profile


@router.delete("/profiles/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_profile(profile_id: int, db: Session = Depends(get_db)):
    deleted = user_profile_service.delete_user_profile(db, profile_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"UserProfile with ID {profile_id} not found"
        )

