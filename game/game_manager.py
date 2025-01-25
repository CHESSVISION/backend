from game.game_model import GameModel
from typing import List


class GameManager:
    def __init__(self):
        self.__games: List[GameModel] = []
        self.__setup()

    def __setup(self):
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
        fen_positions=["rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", "rnbqkbnr/1ppppppp/p7/8/8/8/PPPPPPPP/RNBQKBNR", "rnbqkbnr/1ppppppp/8/p7/8/8/PPPPPPPP/RNBQKBNR"]
    ),

    GameModel(
        id=2,
        title="Mock 2",
        description="This is a mock game 2",
        fen_positions=["8/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8 b"]
    ),

    GameModel(
        id=3,
        title="Mock 3",
        description="This is a mock game 3",
        fen_positions=["8/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8 b"]
    )
]

game_manager = GameManager()
