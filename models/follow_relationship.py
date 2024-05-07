from sqlalchemy import Column, ForeignKey, String, BigInteger, UniqueConstraint, func
import uuid

from db.base_class import Base


class ORMFollowRelationshipModel(Base):
    # This table is for storing many-to-many relationships when users follow users
    __tablename__ = "follow_relationship"
    __table_args__ = (UniqueConstraint("follower_id", "followee_id"),)

    id = Column(String(100), primary_key=True, default=uuid.uuid4().__str__())
    follower_id = Column(
        String(255),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    followee_id = Column(
        String(255),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = Column(BigInteger, server_default=func.extract("epoch", func.now()))
    updated_at = Column(
        BigInteger,
        server_default=func.extract("epoch", func.now()),
        onupdate=func.extract("epoch", func.now()),
    )
