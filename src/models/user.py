from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserInDB(User):
    hashed_password: str
    is_admin: Optional[bool] = False

class UserCreate(User):
    password: str
    is_admin: Optional[bool] = False