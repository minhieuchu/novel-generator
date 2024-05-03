import logging
from typing import Optional
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.user_story import ORMUserStoryModel

logging.basicConfig(level=logging.ERROR)
_logger = logging.getLogger(__name__)


class CRUDUserStory(CRUDBase[ORMUserStoryModel]):
    def get_record(
        self, db: Session, user_id: str, story_id: str
    ) -> Optional[ORMUserStoryModel]:
        try:
            record = (
                db.query(self.model)
                .filter(self.model.user_id == user_id)
                .filter(self.model.story_id == story_id)
                .first()
            )
        except Exception as e:
            _logger.error("Database Exception: %s", e.__repr__())
            return None
        return record

    def get_user_followed_stories(self, db: Session, user_id: str) -> list[str]:
        try:
            records = db.query(self.model).filter(self.model.user_id == user_id).all()
        except Exception as e:
            _logger.error("Database Exception: %s", e.__repr__())
            return []
        return [record.story_id for record in records]


crud_user_story = CRUDUserStory(ORMUserStoryModel)
