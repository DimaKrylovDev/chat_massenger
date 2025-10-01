from pydantic import BaseModel
import uuid
import datetime

class Message(BaseModel):
    id: uuid.UUID
    chat_id: uuid.UUID
    user_id: uuid.UUID
    content: str
    message_type: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True
        from_orm = True