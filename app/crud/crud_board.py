from typing import Any, List, Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud import base
from app.models.board import Board
from app.schemas.board import BoardCreate, BoardUpdate


def create_with_owner(db: Session, *, obj_in: BoardCreate, owner_id: int) -> Board:
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = Board(**obj_in_data, owner_id=owner_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, db_obj: Board, obj_in: BoardUpdate):
    return base.update(db, db_obj=db_obj, obj_in=obj_in)


def remove(db: Session, id: int, model=Board):
    return base.remove(db, model=model, id=id)


def get(db: Session, id: Any) -> Optional[Board]:
    return base.get(db=db, model=Board, id=id)


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Board]:
    return base.get_multi(db=db, skip=skip, limit=limit, model=Board)


def get_multi_by_owner(
    db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
) -> List[Board]:
    return (
        db.query(Board)
        .filter(Board.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
