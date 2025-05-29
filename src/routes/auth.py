from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.user import User, UserCreate
from controller.auth import (
    register_user,
    login_user,
    get_current_user,
)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register")
async def register(user: UserCreate):
    return register_user(user)

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return login_user(form_data)

@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user