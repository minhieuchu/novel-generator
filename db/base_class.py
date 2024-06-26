from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: str
    __name__: str

    @declared_attr
    def __tablename__(self, cls) -> str:
        return cls.__name__.lower()
