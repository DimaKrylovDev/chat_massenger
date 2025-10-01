from .request import GetChatParticipantsRequest
from .response import GetChatParticipantsResponse

from core.dependencies import get_participant_repository, get_chat_repository
from fastapi import HTTPException

class GetChatParticipantsUsecase:
    async def __call__(self, request: GetChatParticipantsRequest) -> GetChatParticipantsResponse:
        chat = await get_chat_repository().get_by_id(id_=request.chat_id)
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        if chat.user_id != request.user_id:
            raise HTTPException(status_code=404, detail="Can't get other user's chat participants")
        participants = await get_participant_repository().get_all_by_filter(chat_id=request.chat_id)
        return GetChatParticipantsResponse(participants=participants, total_count=len(participants))