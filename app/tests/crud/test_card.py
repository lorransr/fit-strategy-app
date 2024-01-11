from sqlalchemy.orm import Session

from app.crud import crud_card
from app.schemas.card import CardCreate, CardUpdate
from app.tests.utils.board import create_random_board
from app.tests.utils.utils import random_lower_string


def test_create_card(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    card_in = CardCreate(title=title, description=description)
    board = create_random_board(db)
    card = crud_card.create_in_board(db=db, obj_in=card_in, board_id=board.id)
    assert card.title == title
    assert card.description == description
    assert card.board_id == board.id
