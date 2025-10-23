from pydantic import BaseModel
from schemas.participant import Participant

class GetChatParticipantsResponse(BaseModel):
    participants: list[Participant]
    total_count: int