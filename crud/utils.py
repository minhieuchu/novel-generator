from api.types.story import Story, StoryStatusEnum


def get_story_from_json(story: dict) -> Story:
    return Story(
        id=str(story.get("_id")),
        author_id=story.get("author_id"),
        title=story.get("title"),
        genre=story.get("genre"),
        theme=story.get("theme"),
        content=story.get("content"),
        description=story.get("description"),
        view_count=int(str(story.get("view_count"))),
        publish_date=int(str(story.get("publish_date"))),
        ranking=int(str(story.get("ranking"))),
        status=StoryStatusEnum[str(story.get("status"))],
    )
