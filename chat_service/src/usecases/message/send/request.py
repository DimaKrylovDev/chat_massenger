from pydantic import BaseModel
import uuid

class SendMessageRequest(BaseModel):
    user_id: uuid.UUID
    chat_id: uuid.UUID
    content: str
    message_type: str = "text"
