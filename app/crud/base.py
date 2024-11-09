from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy import func
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[Base]:
        query = db.query(self.model).filter(self.model.id == id)
        if hasattr(self.model, 'status'):
            query = query.filter(self.model.status == 'active')
        return query.first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Base]:
        query = db.query(self.model)
        if hasattr(self.model, 'status'):
            query = query.filter(self.model.status == 'active')
        query = query.offset(skip).limit(limit)
        return query.all()


    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Any:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj


    def search(self, db: Session, column: str, search_query: str) -> List[Base]:
        query = db.query(self.model)
        if hasattr(self.model, column):
            column_obj = getattr(self.model, column)
            search_query_lower = search_query.lower()
            query = query.filter(func.lower(column_obj).ilike(f"%{search_query_lower}%"))
        return query.all()
 