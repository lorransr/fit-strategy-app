from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.crud import crud_board, crud_user
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Board])
def read_boards(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve Boards.
    """
    if crud_user.is_superuser(current_user):
        items = crud_board.get_multi(db, skip=skip, limit=limit)
    else:
        items = crud_board.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return items


@router.post("/", response_model=schemas.Board)
def create_board(
    *,
    db: Session = Depends(deps.get_db),
    board_in: schemas.BoardCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new Board.
    """
    board = crud_board.create_with_owner(
        db=db, obj_in=board_in, owner_id=current_user.id
    )
    return board


@router.put("/{id}", response_model=schemas.Board)
def update_board(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    board_in: schemas.BoardUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an board.
    """
    board = crud_board.get(db=db, id=id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    if not crud_user.is_superuser(current_user) and (board.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    board = crud_board.update(db=db, db_obj=board, obj_in=board_in)
    return board


@router.get("/{id}", response_model=schemas.Board)
def read_board(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get board by ID.
    """
    board = crud_board.get(db=db, id=id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    if not crud_user.is_superuser(current_user) and (board.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return board


@router.delete("/{id}", response_model=schemas.Board)
def delete_board(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an board.
    """
    board = crud_board.get(db=db, id=id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    if not crud_user.is_superuser(current_user) and (board.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    board = crud_board.remove(db=db, id=id)
    return board
