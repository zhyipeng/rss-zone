from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False
    TEMPLATE_PATH: Path = Path("templates")


settings = Settings()

if not settings.TEMPLATE_PATH.exists():
    settings.TEMPLATE_PATH.mkdir(parents=True)
