from pydantic import BaseModel

class DeleteParticipantRequest(BaseModel):
    user_id: str
    chat_id: str
    participant_id: str