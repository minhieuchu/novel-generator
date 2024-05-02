from bson import ObjectId
from crud.utils import get_story_from_json
from db.init_db import mongo_database
from schemas.story import Story, StoryCreate

story_collection = mongo_database.get_collection("stories")


async def get_stories() -> list[Story]:
    stories: list[Story] = []
    async for story in story_collection.find():
        stories.append(get_story_from_json(story=story))

    return stories


async def get_story(id: str) -> Story | None:
    story = await story_collection.find_one({"_id": ObjectId(id)})
    if story:
        return get_story_from_json(story=story)
    return None


async def add_story(story_data: StoryCreate):
    result = await story_collection.insert_one(story_data.__dict__)
    return result.inserted_id
