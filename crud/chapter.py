from typing import Optional
from bson import ObjectId

from db.init_db import mongo_database

chapter_collection = mongo_database.get_collection("chapters")


class CRUDChapter:
    async def get_chapters(self, story_id: ObjectId) -> list[dict]:
        chapters: list[dict] = []
        async for chapter in chapter_collection.find({"story_id": story_id.__str__()}):
            chapters.append(chapter)

        return chapters

    async def get_chapter(self, id: str) -> Optional[dict]:
        chapter = await chapter_collection.find_one({"_id": ObjectId(id)})
        return chapter

    async def add_chapter(self, chapter_data: dict):
        result = await chapter_collection.insert_one(chapter_data)
        return result.inserted_id

    async def update_chapter(self, update_data: dict) -> bool:
        chapter_id = ObjectId(update_data.get("id"))
        existing_chapter = await chapter_collection.find_one({"_id": chapter_id})
        if existing_chapter is None:
            return False

        filtered_update_data = {k: v for k, v in update_data.items() if v is not None}
        del filtered_update_data["id"]
        existing_chapter = dict(existing_chapter)
        existing_chapter.update(filtered_update_data)
        await chapter_collection.update_one(
            filter={"_id": chapter_id}, update={"$set": existing_chapter}
        )
        return True


crud_chapter = CRUDChapter()
