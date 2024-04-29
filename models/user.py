from sqlalchemy import Column, String, BigInteger, func
import uuid

from db.base_class import Base


class ORMUserModel(Base):
    __tablename__ = "user"

    id = Column(String(100), primary_key=True, default=uuid.uuid4().__str__())
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(BigInteger, server_default=func.extract("epoch", func.now()))
    updated_at = Column(
        BigInteger,
        server_default=func.extract("epoch", func.now()),
        onupdate=func.extract("epoch", func.now()),
    )
