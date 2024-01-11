from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .board import Board  # noqa: F401


class Card(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    tile = Column(String)
    board_id = Column(Integer, ForeignKey("board.id"))
    board = relationship("Board", back_populates="cards")
