import os
import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ChessDetection_v2.ArtificialIntelligenceAgent import artificial_intelligence_agent
from game.game_manager import game_manager
from game.game_model import GameModel, GameDTO, GameUpdate
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
            moves=["df"]
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
        fen_positions=fill_full_fens(game.fen_positions),
        moves=find_moves(game.fen_positions)
    )
    return game_dto


@app.post("/games")
async def upload_video(video: UploadFile = File(...)):
    file = video
    os.makedirs(settings.video_path, exist_ok=True)
    os.makedirs(settings.image_path, exist_ok=True)
    print(file.content_type)
    if file.content_type.startswith("video"):
        file_path = os.path.join(settings.video_path, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        fen_positions = artificial_intelligence_agent.video_to_fen(file_path)

    elif file.content_type.startswith("image"):
        file_path = os.path.join(settings.image_path, file.filename)
        fen_positions = artificial_intelligence_agent.image_to_fen(file_path)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

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


@app.post("/games/{id}")
async def edit_game(id: int, game_update: GameUpdate):
    game = game_manager.get_game(id)
    game.title = game_update.title
    game.description = game_update.description
    return game

