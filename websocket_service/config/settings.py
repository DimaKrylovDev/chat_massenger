from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: str

    exchanger: str = "amq.direct"
    queue_name_to_chat_service: str = "add_chat_or_messages" 
    routing_key_to_chat_service: str = "chat.add"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()