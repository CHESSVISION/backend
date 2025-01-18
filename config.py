from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    origin: List[str] = [
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ]
    video_path: str = "/videos"
    chess_board_detector_model = "chessboard-detection-yqcnu/3"
    chess_piece_detector_model = "chess-pieces-new/19"
    hand_detector_model = "hand-detection-2r6df/1"
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
