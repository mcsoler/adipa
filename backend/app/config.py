from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    database_url: str = Field(..., env="DATABASE_URL")
    ollama_host: str = Field("http://host.docker.internal:11434", env="OLLAMA_HOST")
    ollama_model: str = Field("llama3", env="OLLAMA_MODEL")
    cors_origins: list[str] = Field(["http://localhost:6000"], env="CORS_ORIGINS")
    max_file_size_mb: int = Field(50, env="MAX_FILE_SIZE_MB")
    log_level: str = Field("INFO", env="LOG_LEVEL")

    model_config = {"env_file": ".env", "case_sensitive": False}


settings = Settings()
