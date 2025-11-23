from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.models import User
from app.schemas.user_schema import UserCreate


def create_user(db: Session, user_data: UserCreate) -> User:
    # TODO: Add password hashing before production
    db_user = User(
        email=user_data.email,
        hashed_password=user_data.password,
        full_name=user_data.full_name,
    )
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise ValueError(f"User with email {user_data.email} already exists")


def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    # TODO: Use proper password verification before production
    if password != user.hashed_password:
        return None
    return user


def update_user(db: Session, user_id: int, full_name: Optional[str] = None, password: Optional[str] = None) -> Optional[User]:
    user = get_user(db, user_id)
    if not user:
        return None
    
    if full_name is not None:
        user.full_name = full_name
    if password is not None:
        # TODO: Hash password before production
        user.hashed_password = password
    
    db.commit()
    db.refresh(user)
    return user

