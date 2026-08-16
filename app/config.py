import os

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "DevOps Platform API")
    app_env: str = os.getenv("APP_ENV", "development")
    api_key: str = os.getenv("API_KEY", "dev-secret-key")


settings = Settings()
