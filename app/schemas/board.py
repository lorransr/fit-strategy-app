from typing import Optional

from pydantic import ConfigDict, BaseModel, Field


# Shared properties
class BoardBase(BaseModel):
    title: Optional[str] = Field(None, max_length=60)
    description: Optional[str] = Field(None, max_length=32000)


# Properties to receive on item creation
class BoardCreate(BoardBase):
    title: str


# Properties to receive on item update
class BoardUpdate(BoardBase):
    pass


# Properties shared by models stored in DB
class BoardInDBBase(BoardBase):
    id: int
    title: str
    owner_id: int
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class Board(BoardInDBBase):
    pass


# Properties properties stored in DB
class BoardInDB(BoardInDBBase):
    pass
