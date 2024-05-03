import enum
from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    String,
    BigInteger,
    UniqueConstraint,
    func,
)
import uuid

from db.base_class import Base


class UserStoryRelationEnum(enum.Enum):
    READ = "READ"
    FOLLOW = "FOLLOW"
    COMMENT = "COMMENT"
    PURCHASE = "PURCHASE"


class ORMUserStoryModel(Base):
    # This table is for storing many-to-many relationships when users follow stories
    __tablename__ = "user_story"
    __table_args__ = (UniqueConstraint("user_id", "story_id"),)

    id = Column(String(100), primary_key=True, default=uuid.uuid4().__str__())
    user_id = Column(
        String(255),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    story_id = Column(String(255), nullable=False)
    relation_type = Column(Enum(UserStoryRelationEnum), nullable=False)
    created_at = Column(BigInteger, server_default=func.extract("epoch", func.now()))
    updated_at = Column(
        BigInteger,
        server_default=func.extract("epoch", func.now()),
        onupdate=func.extract("epoch", func.now()),
    )
