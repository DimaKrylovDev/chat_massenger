from pydantic import BaseModel
import uuid

class SendMessageResponse(BaseModel):
    message_id: uuid.UUID
    message: str
    success: bool