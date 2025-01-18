import os
import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ChessDetection_v2.ArtificialIntelligenceAgent import ArtificialIntelligenceAgent
from game import GameManager

app = FastAPI()
game_manager = GameManager()

# Define allowed origins
origins = [
    "http://127.0.0.1:3000",  # React default port
    "http://localhost:3000",  # React default port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
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
    # Check if a file was uploaded
    if not video:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    # Check if the uploaded file is a video
    if not video.content_type.startswith("video/"):  # Correct MIME type check
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type for '{video.filename}'. Only video files are allowed."
        )

    # Ensure the 'videos' directory exists
    os.makedirs("./videos", exist_ok=True)

    # Save the uploaded video to disk
    file_location = os.path.join("./videos", video.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    # Initialize the AI agent and process the video
    agent = ArtificialIntelligenceAgent()
    try:
        fen_positions = agent.video_to_fen(file_location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")

    # Return response with FEN positions
    return {
        "message": "Video uploaded successfully.",
        "filename": video.filename,
        "fen_positions": fen_positions
    }


@app.delete("/games/{id}")
async def delete_game(game_id: int):
    game_manager.delete_game(game_id)
    return {"message": f"delete game: {game_id} SUCCESS"}
