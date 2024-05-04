from typing import Optional
from bson import ObjectId
import logging
from sqlalchemy.orm import Session
import strawberry

from db.init_db import mongo_database
from models.comment import ORMCommentModel
from models.user_story import ORMUserStoryModel

story_collection = mongo_database.get_collection("stories")
logging.basicConfig(level=logging.ERROR)
_logger = logging.getLogger(__name__)


class CRUDStory:
    async def get_stories(self) -> list[dict]:
        stories: list[dict] = []
        async for story in story_collection.find():
            stories.append(story)

        return stories

    async def get_story(self, id: str) -> Optional[dict]:
        story = await story_collection.find_one({"_id": ObjectId(id)})
        return story

    async def get_stories_by_author(self, author_id: str) -> list[dict]:
        stories: list[dict] = []
        async for story in story_collection.find({"author_id": author_id}):
            stories.append(story)
        return stories

    async def get_stories_by_ids(self, ids: list[str]) -> list[dict]:
        stories: list[dict] = []
        async for story in story_collection.find(
            {"_id": {"$in": [ObjectId(id) for id in ids]}}
        ):
            stories.append(story)
        return stories

    async def add_story(self, story_data: dict):
        result = await story_collection.insert_one(story_data)
        return result.inserted_id

    def get_story_comments(self, db: Session, story_id: str) -> list[dict]:
        comment_list: list[dict] = []
        try:
            join_models = (
                db.query(ORMUserStoryModel, ORMCommentModel)
                .filter(
                    story_id == ORMUserStoryModel.story_id,
                    ORMUserStoryModel.id == ORMCommentModel.user_story_id,
                )
                .all()
            )
            for join_model in join_models:
                user_story_model, comment_model = join_model
                comment_list.append(
                    {
                        "id": strawberry.ID(comment_model.id),
                        "user_id": user_story_model.user_id,
                        "story_id": user_story_model.story_id,
                        "content": comment_model.content,
                    }
                )
        except Exception as e:
            _logger.error("Database Exception: %s", e.__repr__())

        return comment_list

    # For development only
    def delete_stories(self):
        story_collection.delete_many({})


crud_story = CRUDStory()
