import logging
from typing import Dict, Generic, List, Optional, Type, TypeVar, Union
import uuid
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

logging.basicConfig(level=logging.ERROR)
_logger = logging.getLogger(__name__)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        Parameters
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: str) -> tuple[bool, Optional[ModelType]]:
        """Query to get a detailed record by its ID from the database"""

        query_model = None
        status = False
        try:
            query_model = db.query(self.model).get(id)
            status = True
        except Exception as e:
            _logger.error("Database Exception: %s", e.__repr__())
            status = False
        return status, query_model

    def filter_by(self, db: Session, filter_dict: dict) -> tuple[bool, List[ModelType]]:
        """Query to get a detailed record by its ID from the database"""

        query_model_list = None
        status = False
        try:
            query_model_list = db.query(self.model).filter_by(**filter_dict).all()
            status = True
        except Exception as e:
            _logger.error("Database Exception: %s", e.__repr__())
            status = False
        return status, query_model_list

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> tuple[bool, List[ModelType]]:
        """Query to get a list of records from the database"""

        query_model_list = []
        status = False
        try:
            query_model_list = db.query(self.model).offset(skip).limit(limit).all()
            status = True
        except Exception as e:
            _logger.error("Database Exception: %s", e.__repr__())
            status = False
        return status, query_model_list

    def create(
        self, db: Session, *, create_object: CreateSchemaType
    ) -> tuple[bool, str]:
        """Query to insert a new record to the database"""

        status = False
        create_object_dict = create_object.model_dump(exclude_none=True)
        db_create_model = self.model(**create_object_dict)  # type: ignore
        db_create_model.id = uuid.uuid4().__str__()
        try:
            db.add(db_create_model)
            db.commit()
            db.refresh(db_create_model)
            status = True
        except Exception as e:
            _logger.error("Database Exception: %s", e.__repr__())
            status = False
            db.rollback()
        return status, db_create_model.id

    def update(
        self,
        db: Session,
        *,
        db_exist_model: ModelType,
        update_object: Union[UpdateSchemaType, Dict[str, str]]
    ) -> bool:
        """Query to update data for an existing record in the database"""

        # Convert update_schema into dictionary without unset/null fields
        if isinstance(update_object, dict):
            update_object_dict = update_object
        else:
            update_object_dict = update_object.model_dump(
                exclude_unset=True, exclude_none=True
            )

        # Update latest data to db_exist_model
        db_model_fields = self.get_model_fields(db_exist_model)
        for field in db_model_fields:
            if field in update_object_dict:
                setattr(db_exist_model, field, update_object_dict[field])

        status = False
        try:
            # Execute to update model in database
            db.add(db_exist_model)
            db.commit()
            db.refresh(db_exist_model)
            status = True
        except Exception as e:
            _logger.error("Database Exception: %s", e.__repr__())
            status = False
            db.rollback()
        return status

    def delete(self, db: Session, *, id: str) -> bool:
        """Query to delete an existing record from the database"""
        status = False
        db_delete_model = db.query(self.model).get(id)
        if db_delete_model:
            try:
                db.delete(db_delete_model)
                db.commit()
                status = True
            except Exception as e:
                _logger.error("Database Exception: %s", e.__repr__())
                status = False
                db.rollback()
        return status

    @staticmethod
    def model_to_dict(sqlalchemy_model):
        # Create a dictionary from SQLAlchemy model attributes
        return {
            column.name: getattr(sqlalchemy_model, column.name)
            for column in sqlalchemy_model.__table__.columns
        }

    @staticmethod
    def get_model_fields(sqlalchemy_model):
        # Get list of fields from the SQLAlchemy model
        return [column.name for column in sqlalchemy_model.__table__.columns]
