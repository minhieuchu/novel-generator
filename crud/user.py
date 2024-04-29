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


crud_user = CRUDUser(ORMUserModel)
