from fastapi import FastAPI
from game import GameManager, GameModel

app = FastAPI()
game_manager = GameManager()


@app.get("/games")
async def get_games():
    return {"games": game_manager.get_games()}


@app.get("/games/{id}")
async def get_game(game_id: int):
    game = game_manager.get_game(game_id)
    return {"game": game}


@app.post("/games")
async def create_game(game_model: GameModel):
    game_manager.add_game(game_model)
    return {"message": f"create game: {game_model.id} SUCCESS"}


@app.delete("/games/{id}")
async def delete_game(game_id: int):
    game_manager.delete_game(game_id)
    return {"message": f"delete game: {game_id} SUCCESS"}
