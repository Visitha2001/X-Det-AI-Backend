from pydantic import BaseModel, EmailStr

class User(BaseModel):
    username: str
    email: EmailStr
    full_name: str = None

class UserInDB(User):
    hashed_password: str

class UserCreate(User):
    password: str