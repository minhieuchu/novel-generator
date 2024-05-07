from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    BigInteger,
    func,
)
import uuid

from db.base_class import Base


class ORMChatModel(Base):
    __tablename__ = "chat"

    id = Column(String(100), primary_key=True, default=uuid.uuid4().__str__())
    chat_relationship_id = Column(
        String(255),
        ForeignKey("chat_relationship.id", ondelete="CASCADE"),
        nullable=False,
    )
    content = Column(String(255), nullable=False)
    created_at = Column(BigInteger, server_default=func.extract("epoch", func.now()))
    updated_at = Column(
        BigInteger,
        server_default=func.extract("epoch", func.now()),
        onupdate=func.extract("epoch", func.now()),
    )
