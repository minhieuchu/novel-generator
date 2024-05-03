import logging
from typing import Optional
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.user_user import ORMUserUserModel

logging.basicConfig(level=logging.ERROR)
_logger = logging.getLogger(__name__)


class CRUDUserUser(CRUDBase[ORMUserUserModel]):
    def get_record(
        self, db: Session, follower_id: str, followee_id: str
    ) -> Optional[ORMUserUserModel]:
        try:
            record = (
                db.query(self.model)
                .filter(self.model.follower_id == follower_id)
                .filter(self.model.followee_id == followee_id)
                .first()
            )
        except Exception as e:
            _logger.error("Database Exception: %s", e.__repr__())
            return None
        return record

    def get_follower_ids_from_user_id(self, db: Session, user_id: str) -> list[str]:
        records: list[ORMUserUserModel] = []
        try:
            records = (
                db.query(self.model).filter(self.model.followee_id == user_id).all()
            )
        except Exception as e:
            _logger.error("Database Exception: %s", e.__repr__())
            return []
        return [record.follower_id for record in records]


crud_user_user = CRUDUserUser(ORMUserUserModel)
