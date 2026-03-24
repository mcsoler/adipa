from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = Field(..., env="DATABASE_URL")
    ollama_host: str = Field("http://host.docker.internal:11434", env="OLLAMA_HOST")
    ollama_model: str = Field("llama3", env="OLLAMA_MODEL")
    cors_origins: list[str] = Field(default=["http://localhost:6000"], env="CORS_ORIGINS")
    max_file_size_mb: int = Field(50, env="MAX_FILE_SIZE_MB")
    log_level: str = Field("INFO", env="LOG_LEVEL")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Acepta tanto string simple, comma-separated, o JSON list."""
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            v = v.strip()
            if not v:
                return ["http://localhost:6000"]
            if v.startswith("["):
                import json
                return json.loads(v)
            return [origin.strip() for origin in v.split(",")]
        return v

    model_config = {"env_file": ".env", "case_sensitive": False}


settings = Settings()
