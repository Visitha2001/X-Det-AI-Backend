from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models.user import UserCreate, User
from controller.auth import (
    register_user,
    login_user,
    get_current_user,
    get_current_admin,
)

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate):
    return register_user(user)

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return login_user(form_data)

@router.get("/users/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/admin/dashboard")
async def admin_dashboard(current_admin: User = Depends(get_current_admin)):
    return {"message": f"Welcome admin: {current_admin.username}"}