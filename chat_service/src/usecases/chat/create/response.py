from pydantic import BaseModel

class CreateChatResponse(BaseModel):
    chat_id: str 
    message: str
    success: bool = False

    