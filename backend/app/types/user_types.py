from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserServiceData(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime

