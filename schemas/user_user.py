from typing import Optional
from pydantic import BaseModel


# ============== BASE SCHEMA TO INHERIT ===================
class UserUserBase(BaseModel):
    id: Optional[str] = None
    follower_id: Optional[str] = None
    followee_id: Optional[str] = None


# ============== DATA SCHEMA FOR INTERACTING WITH DATABASE ===================
class UserUserCreate(UserUserBase):
    follower_id: str
    followee_id: str


class UserUserUpdate(UserUserBase):
    id: Optional[str] = None
    follower_id: Optional[str] = None
    followee_id: Optional[str] = None


class UserUser(UserUserBase):
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
