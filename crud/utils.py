from api.types.chapter import Chapter
from api.types.story import Story, StoryStatusEnum


def get_chapter_from_json(chapter: dict) -> Chapter:
    return Chapter(
        id=str(chapter.get("_id")),
        story_id=chapter.get("story_id"),
        chapter_index=int(chapter.get("chapter_index")),
        title=chapter.get("title"),
        content=chapter.get("content"),
    )


def get_story_from_json(story: dict) -> Story:
    chapters = [get_chapter_from_json(chapter) for chapter in story.get("chapters")]
    return Story(
        id=str(story.get("_id")),
        author_id=story.get("author_id"),
        title=story.get("title"),
        genre=story.get("genre"),
        theme=story.get("theme"),
        description=story.get("description"),
        view_count=int(str(story.get("view_count"))),
        publish_date=int(str(story.get("publish_date"))),
        ranking=int(str(story.get("ranking"))),
        status=StoryStatusEnum[str(story.get("status"))],
        chapters=chapters,
    )
