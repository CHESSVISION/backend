from game_model import GameModel
from typing import List


class GameManager:
    def __init__(self):
        self.__games: List[GameModel] = []
        self.setup()

    def setup(self):
        self.__games = games

    def get_game(self, game_id: int) -> GameModel:
        for game in self.__games:
            if game.id == game_id:
                return game

    def get_games(self) -> List[GameModel]:
        return self.__games

    def add_game(self, game: GameModel):
        self.__games.append(game)

    def delete_game(self, game_id: int):
        for game in self.__games:
            if game.id == game_id:
                self.__games.remove(game)


games = [

    GameModel(
        id=1,
        title="Mock 1",
        description="This is a mock game 1",
        position="rkrnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",
        moves=["e2e4", "e7e5", "g1f3", "b8c6"]
    ),

    GameModel(
        id=2,
        title="Mock 2",
        description="This is a mock game 2",
        position="8/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8 b",
        moves=["e7e5", "g1f3", "b8c6"]
    ),

    GameModel(
        id=3,
        title="Mock 3",
        description="This is a mock game 3",
        position="8/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8 b",
        moves=["e2a5", "g7f7", "c9h6"]
    )
]

game_manager = GameManager()
