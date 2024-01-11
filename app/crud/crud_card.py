from typing import Any, List, Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud import base
from app.models.card import Card
from app.schemas.card import CardCreate, CardUpdate


def create_in_board(db: Session, *, obj_in: CardCreate, board_id: int) -> Card:
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = Card(**obj_in_data, board_id=board_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
