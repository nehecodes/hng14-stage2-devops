from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from pathlib import Path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
        secrets_dir="/run/secrets",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    redis_host: str
    redis_port: int
    redis_password: SecretStr


settings = Settings()
