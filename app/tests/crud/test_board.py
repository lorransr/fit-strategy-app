from sqlalchemy.orm import Session

from app.crud import crud_board
from app.schemas.board import BoardCreate, BoardUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_board(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    board_in = BoardCreate(title=title, description=description)
    user = create_random_user(db)
    board = crud_board.create_with_owner(db=db, obj_in=board_in, owner_id=user.id)
    assert board.title == title
    assert board.description == description
    assert board.owner_id == user.id


def test_get_board(db: Session) -> None:
    user = create_random_user(db)
    expected = {"title": "test_title", "description": "lorem ipsum"}
    board_in = BoardCreate(**expected)
    board = crud_board.create_with_owner(db=db, obj_in=board_in, owner_id=user.id)
    stored_board = crud_board.get(db=db, id=board.id)
    result = stored_board.__dict__

    assert result
    assert expected["title"] == result["title"]
    assert expected["description"] == result["description"]


def test_update_board(db: Session) -> None:
    user = create_random_user(db)
    setup_dict = {"title": "test_title", "description": "lorem ipsum"}
    expected = {"title": "new_title", "description": "new lorem ipsum"}

    board_in = BoardCreate(**setup_dict)
    created_board = crud_board.create_with_owner(
        db=db, obj_in=board_in, owner_id=user.id
    )
    board_update = BoardUpdate(**expected)
    updated_board = crud_board.update(db=db, db_obj=created_board, obj_in=board_update)
    result = updated_board.__dict__

    assert result
    assert expected["title"] == result["title"]
    assert expected["description"] == result["description"]


def test_delete_board(db: Session) -> None:
    user = create_random_user(db)
    setup_dict = {"title": "test_title", "description": "lorem ipsum"}

    board_in = BoardCreate(**setup_dict)
    created_board = crud_board.create_with_owner(
        db=db, obj_in=board_in, owner_id=user.id
    )
    removed_board = crud_board.remove(db=db, id=created_board.id)
    received_board = crud_board.get(db=db, id=created_board.id)

    assert received_board is None
    assert removed_board.id == created_board.id
