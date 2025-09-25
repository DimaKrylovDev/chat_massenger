from pydantic_settings import BaseSettings, SettingsConfigDict
import grpc
from generated import auth_pb2_grpc


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    FASTAPI_PORT: int 

    ACCESS_TOKEN_MINUTES: int 
    REFRESH_TOKEN_DAYS: int
    ALGORITHM: str
    EE_SECRET_KEY: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def GRPC_CHANNEL(self) -> grpc.Channel:
        return grpc.aio.insecure_channel("localhost:50051")

    @property
    def GRPC_STUB(self) -> auth_pb2_grpc.AuthServiceStub:
        return auth_pb2_grpc.AuthServiceStub(self.GRPC_CHANNEL)

    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")



settings = Settings()



