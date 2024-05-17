from api.types.chapter import Chapter
from api.types.comment import Comment, CommentUserBase
from api.types.story import AuthorBase, Story, StoryStatusEnum, StoryTypeEnum


def get_chapter_from_json(chapter: dict) -> Chapter:
    return Chapter(
        chapter_index=int(chapter.get("chapter_index")),
        title=chapter.get("title"),
        content=chapter.get("content"),
        images=chapter.get("images"),
    )


def get_author_base_from_json(author: dict) -> AuthorBase:
    return AuthorBase(
        id=author.get("id"),
        name=author.get("name"),
        email=author.get("email"),
    )


def get_comment_user_base_from_json(user: dict) -> CommentUserBase:
    return CommentUserBase(
        id=user.get("id"), name=user.get("name"), email=user.get("email")
    )


def get_comment_from_json(comment: dict) -> Comment:
    return Comment(
        content=comment.get("content"),
        created_at=int(comment.get("created_at")),
        user=get_comment_user_base_from_json(comment.get("user")),
    )


def get_story_from_json(story: dict) -> Story:
    chapters = [
        get_chapter_from_json(chapter) for chapter in (story.get("chapters") or [])
    ]
    comments = [
        get_comment_from_json(comment) for comment in (story.get("comments") or [])
    ]
    return Story(
        id=str(story.get("_id")),
        title=story.get("title"),
        genre=story.get("genre"),
        theme=story.get("theme"),
        description=story.get("description"),
        view_count=int(story.get("view_count")),
        publish_date=int(story.get("publish_date")),
        ranking=int(story.get("ranking")),
        story_type=StoryTypeEnum[story.get("story_type")],
        status=StoryStatusEnum[story.get("status")],
        chapters=chapters,
        author=get_author_base_from_json(story.get("author")),
        comments=comments,
    )
