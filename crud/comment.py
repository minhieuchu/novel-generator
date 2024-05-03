from crud.base import CRUDBase
from models.comment import ORMCommentModel


class CRUDComment(CRUDBase[ORMCommentModel]):
    pass


crud_comment = CRUDComment(ORMCommentModel)
