from typing import Optional

from sqlalchemy.orm import Session

from app import models
from app.crud import crud_board
from app.schemas.board import BoardBase
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_board(db: Session, *, owner_id: Optional[int] = None) -> models.Board:
    if owner_id is None:
        user = create_random_user(db)
        owner_id = user.id
    title = random_lower_string()
    description = random_lower_string()
    board_in = BoardBase(title=title, description=description, id=id)
    return crud_board.create_with_owner(db=db, obj_in=board_in, owner_id=owner_id)
