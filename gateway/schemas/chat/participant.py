from pydantic import BaseModel
from uuid import UUID
import datetime
from sdk.enums.user_type import UserType

class Participant(BaseModel):
    user_id: UUID
    chat_id: UUID

class AddParticipantRequest(BaseModel):
    user_id: UUID
    chat_id: UUID
    user_type: UserType

class DeleteParticipantRequest(BaseModel):
    user_id: UUID
    chat_id: UUID
    participant_id: UUID

class GetChatParticipantsRequest(BaseModel):
    chat_id: UUID
    user_id: UUID

class GetChatParticipantsResponse(BaseModel):
    participants: list[Participant]
    total_count: int