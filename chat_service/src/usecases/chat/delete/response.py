from pydantic import BaseModel

class DeleteChatResponse(BaseModel):
    success: bool