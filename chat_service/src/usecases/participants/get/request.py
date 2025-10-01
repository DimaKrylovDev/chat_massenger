from pydantic import BaseModel

class GetChatParticipantsRequest(BaseModel):
    chat_id: str
    user_id: str