from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    origin: List[str] = [
        "http://127.0.0.1:3000",  # React default port
        "http://localhost:3000",  # React default port
    ]
    video_path: str = "/videos",


settings = Settings()
