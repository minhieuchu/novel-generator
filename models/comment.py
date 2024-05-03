from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    BigInteger,
    func,
)
import uuid

from db.base_class import Base


class ORMCommentModel(Base):
    __tablename__ = "comment"

    id = Column(String(100), primary_key=True, default=uuid.uuid4().__str__())
    user_story_id = Column(
        String(255),
        ForeignKey("user_story.id", ondelete="CASCADE"),
        nullable=False,
    )
    content = Column(String(255), nullable=False)
    created_at = Column(BigInteger, server_default=func.extract("epoch", func.now()))
    updated_at = Column(
        BigInteger,
        server_default=func.extract("epoch", func.now()),
        onupdate=func.extract("epoch", func.now()),
    )
