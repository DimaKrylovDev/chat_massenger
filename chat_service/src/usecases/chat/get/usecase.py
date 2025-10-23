from .request import GetUserChatsRequest
from .response import GetUserChatsResponse

from core.dependencies import get_chat_repository
from fastapi import HTTPException

class GetUserChatsUsecase:
    async def __call__(self, request: GetUserChatsRequest) -> GetUserChatsResponse:
        chats = await get_chat_repository().get_all_by_filter(user_id=request.user_id)
        return GetUserChatsResponse(chats=chats, total_count=len(chats))
