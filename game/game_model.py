from pydantic import BaseModel
from typing import List


class GameModel(BaseModel):
    id: int
    title: str
    description: str
    position: str
    moves: List[str]
