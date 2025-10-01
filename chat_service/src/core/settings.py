from pydantic_settings import BaseSettings, SettingsConfigDict
import grpc


class Settings(BaseSettings):
    GRPC_PORT: int
    GRPC_HOST: str
    
    WEBSOCKET_PORT: int
    WEBSOCKET_HOST: str
    
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    
    AUTH_SERVICE_HOST: str
    AUTH_SERVICE_PORT: int
    
    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def GRPC_CHANNEL(self) -> grpc.Channel:
        return grpc.aio.insecure_channel(f"{self.GRPC_HOST}:{self.GRPC_PORT}")

    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")

settings = Settings()