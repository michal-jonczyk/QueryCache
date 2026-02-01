from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "QueryCache"
    APP_VERSION: str = "0.1.0"
    PORT: int = 8000
    BASE_URL: str = "http://localhost:8000"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # Database
    DATABASE_URL: str = "sqlite:///./querycache.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()