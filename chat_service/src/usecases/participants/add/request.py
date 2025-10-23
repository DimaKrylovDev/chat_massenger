from pydantic import BaseModel
import uuid
from sdk.enums.user_type import UserType

class AddParticipantRequest(BaseModel):
    user_id: uuid.UUID
    participant_id: uuid.UUID
    chat_id: uuid.UUID
    user_type: UserType 