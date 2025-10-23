from .request import GetMessagesRequest
from .response import GetMessagesResponse

from core.dependencies import get_message_repository, get_participant_repository
from fastapi import HTTPException

class GetMessagesUsecase:
    async def __call__(self, request: GetMessagesRequest) -> GetMessagesResponse:
        participants = await get_participant_repository().get_all_by_filter(chat_id=request.chat_id)
        
        is_present = any(p.user_id == request.user_id for p in participants)

        if not is_present:
            raise HTTPException(status_code=404, detail="Can't get other user's messages")

        messages = await get_message_repository().get_all_by_filter(chat_id=request.chat_id, user_id=request.user_id)
        return GetMessagesResponse(messages=messages, total_count=len(messages))