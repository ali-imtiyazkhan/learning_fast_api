from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI CRUD"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./app.db"
    SECRET_KEY: str = "change-this-in-production"
    API_PREFIX: str = "/api/v1"

    class Config:
        env_file = ".env"

settings = Settings()
