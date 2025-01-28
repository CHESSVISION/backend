import os
import shutil

from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from Chess.Chess import *
from ChessDetection_v2.ArtificialIntelligenceAgent import artificial_intelligence_agent
from Streaming.BackgroundTasks import BackgroundTasks
from Streaming.ConnectionManager import manager
from config import settings
from game.game_manager import game_manager
from game.game_model import GameModel, GameDTO

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origin,  # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def root():
    return {"Hello": "World"}


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
        fen_positions=[partial_to_full_fen(x) for x in game.fen_positions],
        moves=find_moves(game.fen_positions)
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


backgroundTask = BackgroundTasks()
import io
import av
rawData = io.BytesIO()
container = av.open(rawData, format="h264", mode='r')
import cv2
@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    cur_pos = 0
    source = "https://stackoverflow.com/questions/62759863/how-to-use-pyav-or-opencv-to-decode-a-live-stream-of-raw-h-264-data"

    print("Attempting WebSocket connection")
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_bytes()
            rawData.write(data)
            rawData.seek(cur_pos)

            for packet in container.demux():
                if packet.size == 0:
                    continue
                cur_pos += packet.size
                for frame in packet.decode():
                    display_frame(frame)
            # Detect and store SPS/PPS
            nal_unit_type = data[0] & 0x1F
            if nal_unit_type in [7, 8]:  # SPS and PPS
                manager.set_sps_pps(data)
            print(f"Received data of length: {len(data)} bytes, NAL unit type: {nal_unit_type}")
            # Broadcast to other clients
            await manager.broadcast(data)
    except WebSocketDisconnect:
        print("WebSocket disconnected")
        await manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket connection error: {e}")
        await manager.disconnect(websocket)


def display_frame(self, frame):
    # Convert AV Frame to OpenCV image
    img = frame.to_ndarray(format='bgr24')
    print(img)
    cv2.imshow('H264 Stream', img)
