from pydantic import BaseModel
import uuid

class GetMessagesRequest(BaseModel):
    user_id: uuid.UUID
    chat_id: uuid.UUID