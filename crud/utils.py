from schemas.story import Story


def get_story_from_json(story: dict) -> Story:
    return Story(
        id=str(story.get("_id")),
        title=story.get("title"),
        genre=story.get("genre"),
        theme=story.get("theme"),
        content=story.get("content"),
    )
