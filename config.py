from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    origin: List[str] = [
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        "http://35.232.235.246:3000"
    ]
    video_path: str = "./videos"
    image_path: str = "./images"
    chess_board_detector_model: str = "chessboard-detection-yqcnu/3"
    chess_piece_detector_model: str = "chess-pieces-new/19"
    hand_detector_model: str = "hand-detection-2r6df/1"

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
