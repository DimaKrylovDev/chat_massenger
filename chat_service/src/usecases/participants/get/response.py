from pydantic import BaseModel

class GetChatParticipantsResponse(BaseModel):
    participants: list[str]
    total_count: int