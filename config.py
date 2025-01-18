from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    origin: List[str] = [
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ]
    video_path: str = "/videos",

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
