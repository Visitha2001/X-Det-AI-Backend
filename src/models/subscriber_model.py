from pydantic import BaseModel, EmailStr

class Subscriber(BaseModel):
    username: str
    email: EmailStr

class EmailRequest(BaseModel):
    subject: str
    body: str