from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Event Expert System API"
    app_version: str = "1.0.0"
    knowledge_version: str = "1.0.0"

    debug: bool = True
    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "INFO"


settings = Settings()
