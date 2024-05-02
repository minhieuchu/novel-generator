from typing import Optional
from pydantic import BaseModel, EmailStr


# ============== BASE SCHEMA TO INHERIT ===================
class UserBase(BaseModel):
    id: Optional[str] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None


# ============== DATA SCHEMA FOR INTERACTING WITH DATABASE ===================
class UserCreate(UserBase):
    email: EmailStr
    name: str
    password: str


class UserUpdate(UserBase):
    id: Optional[str] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None


class UserUpdatePassword(UserBase):
    old_password: str
    new_password: str


class User(UserBase):
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
