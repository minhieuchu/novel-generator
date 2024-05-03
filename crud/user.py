import logging
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.user import ORMUserModel

logging.basicConfig(level=logging.ERROR)
_logger = logging.getLogger(__name__)


class CRUDUser(CRUDBase[ORMUserModel]):
    def get_user_by_email(self, db: Session, email: str) -> tuple[bool, ORMUserModel]:
        status = True
        user = None
        try:
            user = db.query(self.model).filter(self.model.email == email).first()
        except Exception as e:
            _logger.error("Database Exception: %s", e.__repr__())
            status = False

        return status, user

    def get_users_from_ids(self, db: Session, ids: list[str]) -> list[ORMUserModel]:
        users: list[ORMUserModel] = []
        try:
            users = db.query(self.model).filter(self.model.id.in_(ids)).all()
        except Exception as e:
            _logger.error("Database Exception: %s", e.__repr__())

        return users


crud_user = CRUDUser(ORMUserModel)
