from pydantic import BaseModel
from typing import List


class GameModel(BaseModel):
    id: int
    title: str
    description: str
    fen_positions: List[str]


class GameDTO(BaseModel):
    id: int
    title: str
    description: str
    fen_positions: List[str]
    moves: List[str]
