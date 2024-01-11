from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


def get(db: Session, id: Any, model: Type[ModelType]) -> Optional[ModelType]:
    return db.query(model).filter(model.id == id).first()


def get_multi(
    db: Session, *, skip: int = 0, model: Type[ModelType], limit: int = 100
) -> List[ModelType]:
    return db.query(model).offset(skip).limit(limit).all()


def create(
    db: Session, *, obj_in: CreateSchemaType, model: Type[ModelType]
) -> ModelType:
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = model(**obj_in_data)  # type: ignore
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(
    db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
) -> ModelType:
    obj_data = jsonable_encoder(db_obj)
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.model_dump(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, *, model: Type[ModelType], id: int) -> ModelType:
    obj = db.query(model).get(id)
    db.delete(obj)
    db.commit()
    return obj
