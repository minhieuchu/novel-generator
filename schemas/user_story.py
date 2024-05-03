from typing import Optional
from pydantic import BaseModel


# ============== BASE SCHEMA TO INHERIT ===================
class UserStoryBase(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    story_id: Optional[str] = None
    relation_type: Optional[str] = None


# ============== DATA SCHEMA FOR INTERACTING WITH DATABASE ===================
class UserStoryCreate(UserStoryBase):
    user_id: str
    story_id: str
    relation_type: str


class UserStoryUpdate(UserStoryBase):
    id: Optional[str] = None
    user_id: Optional[str] = None
    story_id: Optional[str] = None
    relation_type: Optional[str] = None


class UserStory(UserStoryBase):
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
