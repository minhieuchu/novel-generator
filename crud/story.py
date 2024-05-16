from typing import Optional
from bson import ObjectId

from db.init_db import mongo_database

story_collection = mongo_database.get_collection("stories")


class CRUDStory:
    async def get_stories(self) -> list[dict]:
        stories = []
        async for story in story_collection.find({}):
            stories.append(story)
        return stories

    async def get_story(self, id: str) -> Optional[dict]:
        story = await story_collection.find_one({"_id": ObjectId(id)})
        return story

    async def get_stories_by_author(self, author_id: ObjectId) -> list[dict]:
        stories = await story_collection.find({"author_id": author_id.__str__()})
        return stories

    async def get_stories_by_ids(self, ids: list[str]) -> list[dict]:
        stories: list[dict] = []
        async for story in story_collection.find({"_id": {"$in": ids}}):
            stories.append(story)
        return stories

    async def add_story(self, story_data: dict):
        del story_data["author_id"]
        result = await story_collection.insert_one(story_data)
        return result.inserted_id

    async def update_story(self, existing_story: dict, update_data: dict) -> bool:
        filtered_update_data = {k: v for k, v in update_data.items() if v is not None}
        del filtered_update_data["id"]
        existing_story.update(filtered_update_data)
        await story_collection.update_one(
            filter={"_id": ObjectId(update_data.get("id"))},
            update={"$set": existing_story},
        )
        return True

    async def add_chapter(self, chapter_data: dict) -> bool:
        story_id = ObjectId(chapter_data.get("story_id"))
        del chapter_data["story_id"]
        await story_collection.update_one(
            filter={"_id": story_id}, update={"$push": {"chapters": chapter_data}}
        )
        return True

    async def update_chapter(self, chapter_data: dict) -> bool:
        story_id = ObjectId(chapter_data.get("story_id"))
        del chapter_data["story_id"]
        updated_data = {}
        if "title" in chapter_data:
            updated_data["chapters.$.title"] = chapter_data.get("title")
        if "content" in chapter_data:
            updated_data["chapters.$.content"] = chapter_data.get("content")

        await story_collection.update_one(
            filter={
                "_id": story_id,
                "chapters.chapter_index": int(chapter_data.get("chapter_index")),
            },
            update={"$set": updated_data},
        )
        return True

    async def add_comment(self, comment_data: dict) -> bool:
        story_id = ObjectId(comment_data.get("story_id"))
        del comment_data["user_id"]
        del comment_data["story_id"]
        await story_collection.update_one(
            filter={"_id": story_id}, update={"$push": {"comments": comment_data}}
        )
        return True


crud_story = CRUDStory()
