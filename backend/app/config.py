from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = Field(..., env="DATABASE_URL")
    ollama_host: str = Field("http://host.docker.internal:11434", env="OLLAMA_HOST")
    ollama_model: str = Field("llama3", env="OLLAMA_MODEL")
    cors_origins: str = Field("http://localhost:6000", env="CORS_ORIGINS")
    max_file_size_mb: int = Field(50, env="MAX_FILE_SIZE_MB")
    log_level: str = Field("INFO", env="LOG_LEVEL")

    @property
    def cors_origins_list(self) -> list[str]:
        """Parsea CORS_ORIGINS como string CSV → lista."""
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    model_config = {"env_file": ".env", "case_sensitive": False}


settings = Settings()
