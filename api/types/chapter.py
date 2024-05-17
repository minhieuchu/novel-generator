from typing import Optional
import strawberry


@strawberry.type
class Chapter:
    chapter_index: int
    title: str
    content: str


@strawberry.input
class AddChapterInput:
    story_id: str
    chapter_index: int
    title: str
    content: str


@strawberry.input
class UpdateChapterInput:
    story_id: str
    chapter_index: int
    title: Optional[str] = None
    content: Optional[str] = None
