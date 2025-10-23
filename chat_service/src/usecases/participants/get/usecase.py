from .request import GetChatParticipantsRequest
from .response import GetChatParticipantsResponse

from core.dependencies import get_participant_repository, get_chat_repository
from fastapi import HTTPException

class GetChatParticipantsUsecase:
    async def __call__(self, request: GetChatParticipantsRequest) -> GetChatParticipantsResponse:
        participants = await get_participant_repository().get_all_by_filter(chat_id=request.chat_id)

        is_present = any(str(p.user_id) == str(request.user_id) for p in participants)

        if not is_present:
            raise HTTPException(status_code=404, detail="Can't get other user's chat participants")

        is_exist = await get_chat_repository().get_by_id(id_=request.chat_id)

        if not is_exist:
            raise HTTPException(status_code=404, detail="Chat not found")
            
        return GetChatParticipantsResponse(participants=participants, total_count=len(participants))