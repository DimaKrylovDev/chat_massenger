from pydantic import BaseModel
from uuid import UUID
import datetime

class Message(BaseModel):
    id: UUID
    chat_id: UUID
    user_id: UUID
    content: str
    message_type: str
    created_at: datetime.datetime

class SendMessageRequest(BaseModel):
    user_id: UUID
    chat_id: UUID
    content: str
    message_type: str

class SendMessageResponse(BaseModel):
    message_id: UUID
    message: str
    success: bool

class GetMessagesRequest(BaseModel):
    user_id: UUID
    chat_id: UUID

class GetMessagesResponse(BaseModel):
    messages: list[Message]
    total_count: int

class DeleteMessageRequest(BaseModel):
    user_id: UUID
    chat_id: UUID
    message_id: UUID

class DeleteMessageResponse(BaseModel):
    success: bool

