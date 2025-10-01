from pydantic import BaseModel
import datetime
from schemas.chat import Chat

class GetUserChatsResponse(BaseModel):
    chats: list[Chat]
    total_count: int

