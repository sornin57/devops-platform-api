import os

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "DevOps Platform API")
    app_env: str = os.getenv("APP_ENV", "development")


settings = Settings()
