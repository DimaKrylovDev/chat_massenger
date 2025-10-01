from pydantic import BaseModel
import uuid

class AddParticipantRequest(BaseModel):
    user_id: uuid.UUID
    chat_id: uuid.UUID
    participant_id: uuid.UUID