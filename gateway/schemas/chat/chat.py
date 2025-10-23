from pydantic import BaseModel
from uuid import UUID
import datetime

class Chat(BaseModel):
    id: UUID
    chat_name: str
    description: str
    created_at: datetime.datetime

class CreateChatRequest(BaseModel):
    user_id: UUID
    chat_name: str
    description: str

class CreateChatResponse(BaseModel):
    chat_id: UUID
    message: str
    success: bool

class GetUserChatsRequest(BaseModel):
    user_id: UUID

class GetUserChatsResponse(BaseModel):
    chats: list[Chat]
    total_count: int

class DeleteChatRequest(BaseModel):
    chat_id: UUID

class DeleteChatResponse(BaseModel):
    success: bool

