from .request import GetMessagesRequest
from .response import GetMessagesResponse

from core.dependencies import get_message_repository, get_chat_repository
from fastapi import HTTPException

class GetMessagesUsecase:
    async def __call__(self, request: GetMessagesRequest) -> GetMessagesResponse:
        chat = await get_chat_repository().get_by_id(id_=request.chat_id)
        if chat.user_id != request.user_id:
            raise HTTPException(status_code=404, detail="Can't get other user's messages")
        messages = await get_message_repository().get_all_by_filter(chat_id=request.chat_id, user_id=request.user_id)
        return GetMessagesResponse(messages=messages, total_count=len(messages))