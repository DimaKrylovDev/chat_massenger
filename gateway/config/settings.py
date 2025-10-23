from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    EE_SECRET_KEY: str

    AUTH_SERVICE_HOST: str
    CHAT_SERVICE_HOST: str

    AUTH_SERVICE_PORT: int
    CHAT_SERVICE_PORT: int    

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()