from pydantic import BaseModel

class DeleteMessageRequest(BaseModel):
    user_id: str
    chat_id: str
    message_id: str