from typing import Optional
from pydantic import BaseModel


# ============== BASE SCHEMA TO INHERIT ===================
class CommentBase(BaseModel):
    id: Optional[str] = None
    user_story_id: Optional[str] = None
    content: Optional[str] = None


# ============== DATA SCHEMA FOR INTERACTING WITH DATABASE ===================
class CommentCreate(CommentBase):
    user_story_id: str
    content: str


class CommentUpdate(CommentBase):
    id: Optional[str] = None
    user_story_id: Optional[str] = None
    content: Optional[str] = None


class Comment(CommentBase):
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
