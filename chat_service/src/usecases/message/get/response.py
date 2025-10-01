from pydantic import BaseModel
from schemas.message import Message

class GetMessagesResponse(BaseModel):
    messages: list[Message]
    total_count: int