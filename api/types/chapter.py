from typing import Optional
import strawberry


@strawberry.type
class Chapter:
    chapter_index: int
    title: Optional[str]
    content: Optional[str]
    images: Optional[list[str]]


@strawberry.input
class AddChapterInput:
    story_id: str
    chapter_index: int
    title: Optional[str] = None
    content: Optional[str] = None
    images: Optional[list[str]] = None


@strawberry.input
class UpdateChapterInput:
    story_id: str
    chapter_index: int
    title: Optional[str] = None
    content: Optional[str] = None
    images: Optional[list[str]] = None
