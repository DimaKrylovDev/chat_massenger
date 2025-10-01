from pydantic import BaseModel

class DeleteChatRequest(BaseModel):
    user_id: str
    chat_id: str