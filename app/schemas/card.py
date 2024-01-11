from typing import Optional
from enum import Enum
from pydantic import ConfigDict, BaseModel, Field


class TileEnum(str, Enum):
    to_do = "to_do"
    in_progress = "in_progress"
    done = "done"


# Shared properties
class CardBase(BaseModel):
    title: Optional[str] = Field(None, max_length=60)
    description: Optional[str] = Field(None, max_length=32000)
    tile: TileEnum


# Properties to receive on item creation
class CardCreate(CardBase):
    title: str
    tile: TileEnum = TileEnum.to_do


# Properties to receive on item update
class CardUpdate(CardBase):
    pass


# Properties shared by models stored in DB
class CardInDBBase(CardBase):
    id: int
    title: str
    board_id: int
    tile: str
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class Card(CardInDBBase):
    pass


# Properties properties stored in DB
class CardInDB(CardInDBBase):
    pass
