from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models.user import UserCreate, User
from typing import List
from controller.auth import (
    register_user,
    login_user,
    get_current_user,
    get_current_admin,
    get_all_users,
    get_user_count,
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

@router.get("/users/all", response_model=List[User])
async def get_all_users_route(users: List[User] = Depends(get_all_users)):
    return users

@router.get("/users/count")
async def get_user_count_route(count: dict = Depends(get_user_count)):
    return count