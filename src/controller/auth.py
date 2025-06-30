from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from models.user import UserInDB, UserCreate
from config.security import verify_password, get_password_hash
from config.config import db 
from bson import ObjectId
from typing import List
from models.user import User
from mail.mailer import send_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "visitha2001"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

users_collection = db["users"]

def get_user(username: str):
    user_data = users_collection.find_one({"username": username})
    if user_data:
        user_data["id"] = str(user_data.get("_id"))
        return UserInDB(**user_data)

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def register_user(user: UserCreate):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]
    users_collection.insert_one(user_dict)
    send_email(
        to=user.email,
        subject="Thank you for registering!",
        body=f"Hello {user.username},\n\nThanks for registering to X-Det-Ai!\n\nWe're thrilled to have you on board!",
        html_body=html_content
    )
    return {"message": "User registered successfully"}

html_content = f"""
<html>
  <body style="font-family: Arial, sans-serif; line-height: 1.6;">
    <div style="max-width: 600px; margin: auto; padding: 20px; background: #f9f9f9; border-radius: 10px; border: 1px solid #ddd;">
      <div style="text-align: center; padding-bottom: 20px;">
        <img src="https://res.cloudinary.com/dqmeeveij/image/upload/v1751270006/Light_Logo_y1wauz.png" alt="X-Det-Ai Logo" style="width: 150px; max-width: 100%; border-radius: 5px;" />
      </div>
      <h2 style="color: #333; text-align: center;">Welcome to X-Det-Ai! Your Registration is Complete!</h2>
      <p style="color: #555;">Dear user,</p>
      <p style="color: #555;">Thank you for registering with X-Det-Ai. We're excited to have you join our community and start exploring the power of AI-powered diagnostics.</p>
      <p style="color: #555;">You can now log in to your account to access all our features and services.</p>
      <p style="color: #555;">If you have any questions or need assistance, feel free to contact our support team.</p>
      <div style="text-align: center; margin-top: 30px;">
        <a href="https://your-website.com/login" style="display: inline-block; padding: 12px 25px; background: #007BFF; color: white; text-decoration: none; border-radius: 5px; font-size: 16px;">Log In to Your Account</a>
      </div>
      <p style="color: #555; text-align: center; margin-top: 30px; font-size: 14px;">Best regards,<br/>The X-Det-Ai Team</p>
    </div>
  </body>
</html>
"""

def login_user(form_data: OAuth2PasswordRequestForm):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"sub": user.username}
    return {
        "access_token": create_access_token(token_data, access_token_expires),
        "token_type": "bearer",
        "is_admin": user.is_admin
    }

def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(username)
    if not user:
        raise credentials_exception
    return user

def get_current_admin(token: str = Depends(oauth2_scheme)) -> UserInDB:
    user = get_current_user(token)
    if not getattr(user, "is_admin", False):
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

def get_all_users(current_admin: UserInDB = Depends(get_current_admin)):
    users = []
    for user_data in users_collection.find():
        user_data["id"] = str(user_data.get("_id"))
        users.append(User(**user_data))
    return users

def get_user_count(current_admin: UserInDB = Depends(get_current_admin)):
    return {"count": users_collection.count_documents({})}