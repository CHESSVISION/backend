import os
import shutil

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from ChessDetection_v2.ArtificialIntelligenceAgent import ArtificialIntelligenceAgent
from game.game_manager import game_manager

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
    return game_manager.get_games()


@app.get("/games/{game_id}")
async def get_game(game_id: int):
    return game_manager.get_game(game_id)


@app.post("/games")
async def upload_video(video: UploadFile = File(...)):
    os.makedirs(settings.video_path, exist_ok=True)

    file_location = os.path.join(settings.video_path, video.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    agent = ArtificialIntelligenceAgent()
    fen_positions = agent.video_to_fen(file_location)

    return {
        "message": "Video uploaded successfully.",
        "filename": video.filename,
        "fen_positions": fen_positions
    }


@app.delete("/games/{id}")
async def delete_game(game_id: int):
    game_manager.delete_game(game_id)
    return {"message": f"delete game: {game_id} SUCCESS"}
