from game.game_model import GameModel
from typing import List


class GameManager:
    def __init__(self):
        self.__games: List[GameModel] = []
        self.__setup_in_memory()

    def __setup_in_memory(self):
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
        fen_positions=["rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", "rnbqkbnr/1ppppppp/p7/8/8/8/PPPPPPPP/RNBQKBNR",
                       "rnbqkbnr/1ppppppp/8/p7/8/8/PPPPPPPP/RNBQKBNR"]
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
    ),
    GameModel(
        id=4,
        title="Immortal Game",
        description="This is the Immortal Game (Adolf Anderssen vs Lionel Kieseritzky, 1851)",
        fen_positions=[
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",
            "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR",
            "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR",
            "rnbqkbnr/pppp1ppp/8/4p3/4PP2/8/PPPP2PP/RNBQKBNR",
            "rnbqkbnr/pppp1ppp/8/8/4Pp2/8/PPPP2PP/RNBQKBNR",
            "rnbqkbnr/pppp1ppp/8/8/2B1Pp2/8/PPPP2PP/RNBQK1NR",
            "rnb1kbnr/pppp1ppp/8/8/2B1Pp1q/8/PPPP2PP/RNBQK1NR",
            "rnb1kbnr/pppp1ppp/8/8/2B1Pp1q/8/PPPP2PP/RNBQ1KNR",
            "rnb1kbnr/p1pp1ppp/8/1p6/2B1Pp1q/8/PPPP2PP/RNBQ1KNR",
            "rnb1kbnr/p1pp1ppp/8/1B6/4Pp1q/8/PPPP2PP/RNBQ1KNR",
            "rnb1kb1r/p1pp1ppp/5n2/1B6/4Pp1q/8/PPPP2PP/RNBQ1KNR",
            "rnb1kb1r/p1pp1ppp/5n2/1B6/4Pp1q/5N2/PPPP2PP/RNBQ1K1R",
            "rnb1kb1r/p1pp1ppp/5n1q/1B6/4Pp2/5N2/PPPP2PP/RNBQ1K1R",
            "rnb1kb1r/p1pp1ppp/5n1q/1B6/4Pp2/3P1N2/PPP3PP/RNBQ1K1R",
            "rnb1kb1r/p1pp1ppp/7q/1B5n/4Pp2/3P1N2/PPP3PP/RNBQ1K1R",
            "rnb1kb1r/p1pp1ppp/7q/1B5n/4Pp1N/3P4/PPP3PP/RNBQ1K1R",
            "rnb1kb1r/p1pp1ppp/8/1B4qn/4Pp1N/3P4/PPP3PP/RNBQ1K1R",
            "rnb1kb1r/p1pp1ppp/8/1B3Nqn/4Pp2/3P4/PPP3PP/RNBQ1K1R",
            "rnb1kb1r/p2p1ppp/2p5/1B3Nqn/4Pp2/3P4/PPP3PP/RNBQ1K1R",
            "rnb1kb1r/p2p1ppp/2p5/1B3Nqn/4PpP1/3P4/PPP4P/RNBQ1K1R",
            "rnb1kb1r/p2p1ppp/2p2n2/1B3Nq1/4PpP1/3P4/PPP4P/RNBQ1K1R",
            "rnb1kb1r/p2p1ppp/2p2n2/1B3Nq1/4PpP1/3P4/PPP4P/RNBQ1KR1",
            "rnb1kb1r/p2p1ppp/5n2/1p3Nq1/4PpP1/3P4/PPP4P/RNBQ1KR1",
            "rnb1kb1r/p2p1ppp/5n2/1p3Nq1/4PpPP/3P4/PPP5/RNBQ1KR1",
            "rnb1kb1r/p2p1ppp/5nq1/1p3N2/4PpPP/3P4/PPP5/RNBQ1KR1",
            "rnb1kb1r/p2p1ppp/5nq1/1p3N1P/4PpP1/3P4/PPP5/RNBQ1KR1",
            "rnb1kb1r/p2p1ppp/5n2/1p3NqP/4PpP1/3P4/PPP5/RNBQ1KR1",
            "rnb1kb1r/p2p1ppp/5n2/1p3NqP/4PpP1/3P1Q2/PPP5/RNB2KR1",
            "rnb1kbnr/p2p1ppp/8/1p3NqP/4PpP1/3P1Q2/PPP5/RNB2KR1",
            "rnb1kbnr/p2p1ppp/8/1p3NqP/4PBP1/3P1Q2/PPP5/RN3KR1",
            "rnb1kbnr/p2p1ppp/5q2/1p3N1P/4PBP1/3P1Q2/PPP5/RN3KR1",
            "rnb1kbnr/p2p1ppp/5q2/1p3N1P/4PBP1/2NP1Q2/PPP5/R4KR1"
        ])
]

game_manager = GameManager()
