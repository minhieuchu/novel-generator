from typing import Optional
from pydantic import BaseModel


# ============== BASE SCHEMA TO INHERIT ===================
class StoryBase(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    genre: Optional[str] = None
    theme: Optional[str] = None
    content: Optional[str] = None


# ============== DATA SCHEMA FOR INTERACTING WITH DATABASE ===================
class StoryCreate(StoryBase):
    title: str
    genre: str
    theme: str
    content: str


class StoryUpdate(StoryBase):
    id: Optional[str] = None
    title: Optional[str] = None
    genre: Optional[str] = None
    theme: Optional[str] = None
    content: Optional[str] = None


class Story(StoryBase):
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
