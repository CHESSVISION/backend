import os
import shutil

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from ChessDetection_v2.ArtificialIntelligenceAgent import artificial_intelligence_agent
from game.game_manager import game_manager
from game.game_model import GameModel, GameDTO
from Chess.Chess import *

from config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origin,  # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/games")
async def get_games():
    response = []
    for game in game_manager.get_games():
        game_dto = GameDTO(
            id=game.id,
            title=game.title,
            description=game.description,
            fen_positions=game.fen_positions,
        )
        response.append(game_dto)
    return response


@app.get("/games/{game_id}")
async def get_game(game_id: int):
    game = game_manager.get_game(game_id)
    game_dto = GameDTO(
        id=game.id,
        title=game.title,
        description=game.description,
        fen_positions=[partial_to_full_fen(x) for x in game.fen_positions],
    )
    return game_dto


@app.post("/games")
async def upload_video(video: UploadFile = File(...)):
    os.makedirs(settings.video_path, exist_ok=True)

    file_location = os.path.join(settings.video_path, video.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    fen_positions = artificial_intelligence_agent.video_to_fen(file_location)
    game_id = len(game_manager.get_games()) + 1
    game = GameModel(
        id=game_id,
        title="Untitled",
        description="None",
        fen_positions=fen_positions,
    )
    game_manager.add_game(game)

    return {
        "message": "Video uploaded successfully.",
        "id": game_id
    }


@app.delete("/games/{id}")
async def delete_game(game_id: int):
    game_manager.delete_game(game_id)
    return {"message": f"delete game: {game_id} SUCCESS"}
