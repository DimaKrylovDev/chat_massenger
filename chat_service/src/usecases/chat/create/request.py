from pydantic import BaseModel

class CreateChatRequest(BaseModel): 
    chat_name: str
    user_id: str
    description: str

