from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_admin: Optional[bool] = False

class UserInDB(User):
    hashed_password: str

class UserCreate(User):
    password: str