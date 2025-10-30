from pydantic import BaseModel
from uuid import UUID
import datetime

def SReceiveMessage(BaseModel):
    chat_id: UUID
    user_id: UUID
    content: str

def SSendMessage(BaseModel):
    chat_id: UUID
    user_id: UUID
    content: str
    created_at: datetime.datetime
    message_type: str

def SMessage(BaseModel):
    chat_id: UUID
    user_id: UUID
    content: UUID
    created_at: datetime.datetime
    message_type: str

    